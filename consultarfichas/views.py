from django.shortcuts import render

# Create your views here.

def consultarficha(request):
    return render(request, 'administrador/consultarficha.html',{
        'title': 'Consultar fichas',
        'usuario': 'Administrador',
    })