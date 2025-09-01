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
    if request.method == 'POST':
        try:
            with transaction.atomic():
                tipo_programa_id = request.POST.get('tipoPrograma_id')
                tipo_modalidad = request.POST.get('tipoModalidad')
                nombre_programa_codigo = request.POST.get('nombrePrograma_codigo')
                version_programa = request.POST.get('versionPrograma')
                subsector_economico = request.POST.get('subsectorEconomico')
                fecha_inicio = request.POST.get('fechaInicio')
                fecha_finalizacion = request.POST.get('fechaFinalizacion')
                cupo_aprendices = request.POST.get('cupoAprendices')
                municipio_formacion = request.POST.get('municipioFormacion')
                direccion_formacion = request.POST.get('direccionFormacion')
                tiene_empresa = request.POST.get('tieneEmpresa')
                empresa_solicitante = request.POST.get('empresaSolicitante', '')
                tipo_empresa = request.POST.get('tipoEmpresa', '')
                nombre_responsable = request.POST.get('nombreResponsable', '')
                correo_responsable = request.POST.get('correoResponsable', '')
                nit_empresa = request.POST.get('nitEmpresa', '')
                programa_especial = request.POST.get('programaEspecial')
                convenio = request.POST.get('convenio', '')
                nombre_ambiente = request.POST.get('nombreAmbiente')
                dias_semana = request.POST.getlist('diasSemana[]')
                horario_curso = request.POST.get('horarioCurso')
                fechas_ejecucion_mes1 = request.POST.get('fechasEjecucionMes1')
                fechas_ejecucion_mes2 = request.POST.get('fechasEjecucionMes2', '')

                horario = Horario.objects.create(
                    fechainicio=datetime.strptime(fecha_inicio, '%Y-%m-%d').date(),
                    fechafin=datetime.strptime(fecha_finalizacion, '%Y-%m-%d').date(),
                    mes1=f"{fechas_ejecucion_mes1} - Días: {', '.join(dias_semana)} - Horario: {horario_curso}",
                    mes2=fechas_ejecucion_mes2 or None
                )

                empresa_obj = None
                if tiene_empresa == 'si':
                    empresa_obj = Empresa.objects.filter(nombreempresa=empresa_solicitante).first()
                    if not empresa_obj:
                        tipo_empresa_obj = Tipoempresa.objects.get(idtipoempresa=tipo_empresa)
                        nit_valor = int(nit_empresa) if nit_empresa.isdigit() else 0
                        empresa_obj = Empresa.objects.create(
                            nombreempresa=empresa_solicitante,
                            representanteempresa=nombre_responsable,
                            correoempresa=correo_responsable,
                            nitempresa=nit_valor,
                            idtipoempresa=tipo_empresa_obj
                        )

                programa_formacion = Programaformacion.objects.get(codigoprograma=nombre_programa_codigo)
                modalidad = Modalidad.objects.get(idmodalidad=tipo_modalidad)
                municipio = Municipio.objects.get(codigomunicipio=municipio_formacion)
                programa_especial_obj = Programaespecial.objects.get(idespecial=programa_especial)
                ambiente_obj = Ambiente.objects.filter(idambiente=nombre_ambiente).first() if nombre_ambiente else None
                tipo_solicitud = Tiposolicitud.objects.get(idtiposolicitud=tipo_solicitud_id)

                user_id = request.session.get('user_id')
                if not user_id:
                    messages.error(request, 'Debe iniciar sesión para crear una solicitud.')
                    return redirect('login')

                usuario = Usuario.objects.get(idusuario=user_id)

                ultimo_codigo = Solicitud.objects.aggregate(max_codigo=models.Max('codigosolicitud'))['max_codigo']
                nuevo_codigo = (ultimo_codigo or 0) + 1

                Solicitud.objects.create(
                    idtiposolicitud=tipo_solicitud,
                    codigoprograma=programa_formacion,
                    idhorario=horario,
                    cupo=int(cupo_aprendices),
                    idmodalidad=modalidad,
                    codigomunicipio=municipio,
                    direccion=direccion_formacion,
                    idusuario=usuario,
                    idempresa=empresa_obj,
                    subsectoreconomico=subsector_economico,
                    idespecial=programa_especial_obj,
                    convenio=convenio or None,
                    ambiente=ambiente_obj,
                    fechasolicitud=timezone.now().date()
                )

                messages.success(request, mensaje_exito)
                return redirect('consultarsolicitudinstru')

        except Exception as e:
            messages.error(request, f'Error al crear la solicitud: {str(e)}')

    context = _get_common_context(usuario_tipo, request.session.get('name'))
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
