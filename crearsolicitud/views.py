from django.shortcuts import render

# Create your views here.

# Crearsolicitud
def crear(request):
    return render(request, 'administrador/crearficha.html',{
        'usuario': 'Administrador',

    })


def crearinstructor(request):
    return render(request, 'instructor/crearficha.html',{
        'usuario': 'Instructor',

    })
