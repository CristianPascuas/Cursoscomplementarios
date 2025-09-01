from django.shortcuts import render, redirect
# Mostrar mensajes
from django.contrib import messages
# Importar modelo requerido
from crearsolicitud.models import Usuario
# from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'inicio/index.html', {
        'title': 'Inicio sesión',
    })

def login_view(request):
    # Comprobar que los datos se recibieron desde le formulario
    if request.method == 'POST':
        numero_cedula = request.POST.get('numeroCedula')
        contrasena = request.POST.get('contrasena')
        tipo_usuario = int(request.POST.get('tipoUsuario'))

        # Buscar en la base de datos si existe un usuario con esos datos
        try:
            usuario = Usuario.objects.get(
                numeroidentificacion=numero_cedula,
                clave=contrasena,
                rol=tipo_usuario
            )

            # Guardar el ID del usuario en la sesión
            request.session['user_id'] = usuario.idusuario
            request.session['name'] = usuario.nombre

            # Redirigir según el rol
            if tipo_usuario == 1:
                return render(request, 'user/instructor.html', {
                    'title': 'Portal Instructor',
                    'usuario': 'Instructor',
                    'user_id': request.session.get('user_id'),
                    'nombre': request.session.get('name')
                })
            elif tipo_usuario == 2:
                return render(request, 'user/coordinador.html',{
                    'title': 'Portal Coordinador',
                    'usuario': 'Coordinador',
                    'user_id': request.session.get('user_id'),
                    'nombre': request.session.get('name')
                })
            elif tipo_usuario == 3:
                return render(request, 'user/funcionario.html',{
                    'title': 'Portal Funcionario',
                    'usuario': 'Funcionario',
                    'user_id': request.session.get('user_id'),
                    'nombre': request.session.get('name')
                })
            elif tipo_usuario == 4:
                return render(request, 'user/administrador.html', {
                    'title': 'Portal Administrador',
                    'usuario': 'Administrador',
                    'user_id': request.session.get('user_id'),
                    'nombre': request.session.get('name')
                })

        except Usuario.DoesNotExist:
            return render(request, 'inicio/index.html', {
                'error': 'Usuario no encontrado o credenciales incorrectas'
            })
            # return render(request,'inicio/index.html')
    
    return render(request, 'inicio/index.html')

# Estas funciones se encargan de redirigir al inicio de cada uno
def admin(request):
# Datos coinciden, puedes redirigir o iniciar sesión
    return render(request, 'user/administrador.html',{
        'title': 'Portal Administrador - crear ficha',
        'usuario':'Administrador',
        'nombre': request.session.get('name'),
    })

def instru(request):
# Datos coinciden, puedes redirigir o iniciar sesión
    return render(request, 'user/instructor.html',{
        'title': 'Portal instructor - crear ficha',
        'usuario':'Instructor',
        'nombre': request.session.get('name'),
    })

def funcionario(request):
# Datos coinciden, puedes redirigir o iniciar sesión
    return render(request, 'user/funcionario.html',{
        'title': 'Portal Funcionario - crear ficha',
        'usuario':'Funcionario',
        'nombre': request.session.get('name'),
    })