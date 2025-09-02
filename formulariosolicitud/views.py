from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import transaction, models
from datetime import datetime
from crearsolicitud.models import (
    Area, Modalidad, Programaformacion, Departamentos, 
    Municipio, Tipoempresa, Programaespecial, Ambiente,
    Solicitud, Empresa, Horario, Usuario, Tiposolicitud
)

def _get_common_context(usuario_tipo, nombre_usuario=None):
    context = {
        'usuario': usuario_tipo,
        'areas': Area.objects.all(),
        'modalidades': Modalidad.objects.all(),
        'tipos_empresa': Tipoempresa.objects.all(),
        'programas_especiales': Programaespecial.objects.all(),
        'ambientes': Ambiente.objects.all(),
        'nombre': nombre_usuario or 'Usuario',
        'programas_formacion': Programaformacion.objects.select_related('idarea', 'idmodalidad').all(),
        'departamentos': Departamentos.objects.all(),
        'municipios': Municipio.objects.select_related('codigodepartamento').all(), 
    }
    return context

def _crear_solicitud(request, tipo_solicitud_id, template_name, mensaje_exito, usuario_tipo='Instructor'):
    # Contexto común para GET request
    context = _get_common_context(usuario_tipo)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Capturar todos los datos del formulario
                datos_formulario = {
                    'tiene_empresa': request.POST.get('tieneEmpresa'),
                    'nombre_programa_codigo': request.POST.get('nombrePrograma_codigo'),
                    'subsector_economico': request.POST.get('subsectorEconomico'),
                    'fecha_inicio': request.POST.get('fechaInicio'),
                    'fecha_finalizacion': request.POST.get('fechaFinalizacion'),
                    'cupo_aprendices': request.POST.get('cupoAprendices'),
                    'municipio_formacion': request.POST.get('municipioFormacion'),
                    'direccion_formacion': request.POST.get('direccionFormacion'),
                    'programa_especial': request.POST.get('programaEspecial'),
                    'convenio': request.POST.get('convenio', ''),
                    'nombre_ambiente': request.POST.get('nombreAmbiente'),
                    'dias_semana': request.POST.getlist('diasSemana[]'),
                    'horario_curso': request.POST.get('horarioCurso'),
                    'fechas_ejecucion_mes1': request.POST.get('fechasEjecucionMes1'),
                    'fechas_ejecucion_mes2': request.POST.get('fechasEjecucionMes2', ''),
                    # Datos de empresa
                    'empresa_solicitante': request.POST.get('empresaSolicitante', ''),
                    'tipo_empresa': request.POST.get('tipoEmpresa', ''),
                    'nombre_responsable': request.POST.get('nombreResponsable', ''),
                    'correo_responsable': request.POST.get('correoResponsable', ''),
                    'nit_empresa': request.POST.get('nitEmpresa', ''),
                }

                # Validaciones centralizadas
                campos_requeridos = [
                    ('nombre_programa_codigo', "Debe seleccionar un programa de formación"),
                    ('municipio_formacion', "Debe seleccionar un municipio de formación"),
                    ('programa_especial', "Debe seleccionar un programa especial"),
                    ('nombre_ambiente', "Debe seleccionar un ambiente de formación"),
                    ('cupo_aprendices', "Debe seleccionar un cupo de aprendices"),
                ]
                
                for campo, mensaje in campos_requeridos:
                    if not datos_formulario[campo]:
                        raise ValueError(mensaje)
                
                if not datos_formulario['fecha_inicio'] or not datos_formulario['fecha_finalizacion']:
                    raise ValueError("Las fechas de inicio y finalización son obligatorias")

                # Crear horario
                horario = Horario.objects.create(
                    fechainicio=datetime.strptime(datos_formulario['fecha_inicio'], '%Y-%m-%d').date(),
                    fechafin=datetime.strptime(datos_formulario['fecha_finalizacion'], '%Y-%m-%d').date(),
                    mes1=f"{datos_formulario['fechas_ejecucion_mes1']} - Días: {', '.join(datos_formulario['dias_semana'])} - Horario: {datos_formulario['horario_curso']}",
                    mes2=datos_formulario['fechas_ejecucion_mes2'] or None
                )

                # Manejar empresa
                empresa_obj = None
                if datos_formulario['tiene_empresa'] == 'si' and datos_formulario['empresa_solicitante']:
                    empresa_obj = Empresa.objects.filter(nombreempresa=datos_formulario['empresa_solicitante']).first()
                    if not empresa_obj and datos_formulario['tipo_empresa']:
                        tipo_empresa_obj = Tipoempresa.objects.get(idtipoempresa=datos_formulario['tipo_empresa'])
                        nit_valor = int(datos_formulario['nit_empresa']) if datos_formulario['nit_empresa'].isdigit() else 0
                        empresa_obj = Empresa.objects.create(
                            nombreempresa=datos_formulario['empresa_solicitante'],
                            representanteempresa=datos_formulario['nombre_responsable'],
                            correoempresa=datos_formulario['correo_responsable'],
                            nitempresa=nit_valor,
                            idtipoempresa=tipo_empresa_obj
                        )

                # Obtener objetos relacionados con una sola consulta cada uno
                objetos_relacionados = {
                    'programa_formacion': Programaformacion.objects.get(codigoprograma=datos_formulario['nombre_programa_codigo']),
                    'modalidad': Modalidad.objects.get(idmodalidad=1),
                    'municipio': Municipio.objects.get(codigomunicipio=datos_formulario['municipio_formacion']),
                    'programa_especial_obj': Programaespecial.objects.get(idespecial=datos_formulario['programa_especial']),
                    'ambiente_obj': Ambiente.objects.get(idambiente=datos_formulario['nombre_ambiente']),
                    'tipo_solicitud': Tiposolicitud.objects.get(idtiposolicitud=tipo_solicitud_id),
                }

                # Verificar usuario en sesión
                user_id = request.session.get('user_id')
                if not user_id:
                    messages.error(request, 'Debe iniciar sesión para crear una solicitud.')
                    return redirect('login')

                usuario = Usuario.objects.get(idusuario=user_id)

                # Crear solicitud
                solicitud = Solicitud.objects.create(
                    idtiposolicitud=objetos_relacionados['tipo_solicitud'],
                    codigosolicitud=None,
                    codigoprograma=objetos_relacionados['programa_formacion'],
                    idhorario=horario,
                    cupo=int(datos_formulario['cupo_aprendices']),
                    idmodalidad=objetos_relacionados['modalidad'],
                    codigomunicipio=objetos_relacionados['municipio'],
                    direccion=datos_formulario['direccion_formacion'],
                    idusuario=usuario,
                    idempresa=empresa_obj,
                    subsectoreconomico=datos_formulario['subsector_economico'],
                    idespecial=objetos_relacionados['programa_especial_obj'],
                    convenio=datos_formulario['convenio'] or None,
                    ambiente=objetos_relacionados['ambiente_obj'],
                    fechasolicitud=timezone.now().date()
                )

                messages.success(request, mensaje_exito)
                return redirect('consultarsolicitudinstru')

        except Exception as e:
            messages.error(request, f'Error al crear la solicitud: {str(e)}')
    
    return render(request, template_name, context)

# Formularios ADMIN
def formularioregular(request):
    return _crear_solicitud(
        request,
        tipo_solicitud_id=1,
        template_name='admin/crearficharegular.html',
        mensaje_exito='Solicitud de ficha regular creada exitosamente.',
        usuario_tipo='Administrador'
    )

def formulariocampesina(request):
    return _crear_solicitud(
        request,
        tipo_solicitud_id=2,
        template_name='admin/crearfichacampesina.html',
        mensaje_exito='Solicitud de ficha campesina creada exitosamente.',
        usuario_tipo='Administrador'
    )

# Formularios INSTRUCTOR
def formularioregularinstru(request):
    return _crear_solicitud(
        request,
        tipo_solicitud_id=1,
        template_name='instructor/crearficharegularinstru.html',
        mensaje_exito='Solicitud regular creada exitosamente.',
        usuario_tipo='Instructor'
    )

def formulariocampesinainstru(request):
    return _crear_solicitud(
        request,
        tipo_solicitud_id=2,
        template_name='instructor/crearfichacampeinstru.html',
        mensaje_exito='Solicitud de ficha campesina creada exitosamente.',
        usuario_tipo='Instructor'
    )
