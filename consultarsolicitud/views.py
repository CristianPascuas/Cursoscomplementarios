from django.shortcuts import render

# Create your views here.

def consultarsolicitud(request):
    return render(request, 'administrador/consultarsolicitudes.html',{
        'title': 'consultar-solicitudes',
        'usuario': 'Administrador',
    })

def consultarsolicitudinstru(request):
    return render(request, 'instructor/consultarsolicitudesinstru.html',{
        'title': 'consultar-solicitudes',
        'usuario': 'Instructor',  
    })

def consultarsolicitudfuncionario(request):
    return render(request, 'funcionario/consultarsolicitudfuncionario.html',{
        'title': 'consultar-solicitudes',
        'usuario': 'Funcionario',
    })