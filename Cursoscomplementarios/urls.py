"""
URL configuration for Cursoscomplementarios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Vistas principales
from inicio import views
# crear solicitudes
from crearsolicitud import views as viewsfichacrear
# Consultar solicitudes
from consultarsolicitud import views as viewsconsultarsoli 
# consultar fichas (Solo admin)
from consultarfichas import views as viewsconsultarficha
# Formularios de solicitud
from formulariosolicitud import views as fromwiews

# Permitir acceder a las funciones de la vista
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # Inicio de quien se logue
    path('login/', views.login_view, name='login'),
    # Parte ADMIN
    path('inicio/',views.admin, name='inicio'),
    path('crearficha/',viewsfichacrear.crear, name='crearficha'),
    path('crearfichacampesina/', fromwiews.formulariocampesina, name='crearfichacampesina'),
    path('crearficharegular/', fromwiews.formularioregular, name='crearficharegular'),
    path('consultarsolicitud/', viewsconsultarsoli.consultarsolicitud, name='consultarsolicitud'),
    path('consultarficha/', viewsconsultarficha.consultarficha, name='consultarficha'),
    # Parte INSTRUCTOR
    path('crearfichainstructor/', viewsfichacrear.crearinstructor, name='crearfichainstructor'),
    path("crearfichacampesinainstru/", fromwiews.formulariocampesinainstru, name="crearfichacampesinainstru"),
    path("crearficharegularinstru/", fromwiews.formularioregularinstru, name="crearficharegularinstru"),
    path('consultarsolicitudinstru/', viewsconsultarsoli.consultarsolicitudinstru, name='consultarsolicitudinstru'),
    path('instructor/', views.instru, name='instructor'),
    # Parte FUNCIONARIO
    path('consultarsolicitudfuncionario/', viewsconsultarsoli.consultarsolicitudfuncionario, name='consultarsolicitudfuncionario'),
    path('funcionario/', views.funcionario, name='funcionario'),

]
