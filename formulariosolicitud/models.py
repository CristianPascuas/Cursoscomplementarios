from django.db import models
# Importar desde crearsolicitud el modelo solicitud
from crearsolicitud.models import Solicitud

# Create your models here.

class Aspirantes(models.Model):
    idaspirante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    idcaracterizacion = models.ForeignKey('Caracterizacion', models.DO_NOTHING, db_column='idcaracterizacion')
    telefono = models.CharField(unique=True, max_length=50)
    pdf = models.TextField(blank=True, null=True)
    tipoidentificacion = models.ForeignKey('Tipoidentificacion', models.DO_NOTHING, db_column='tipoidentificacion')
    numeroidentificacion = models.IntegerField(unique=True)
    correo = models.CharField(unique=True, max_length=255)
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'aspirantes'

class Caracterizacion(models.Model):
    idcaracterizacion = models.AutoField(primary_key=True)
    caracterizacion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'caracterizacion'

class Tipoidentificacion(models.Model):
    idtipoidentificacion = models.AutoField(primary_key=True)
    tipoidentificacion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipoidentificacion'