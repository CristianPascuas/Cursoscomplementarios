from django.db import models
# Importar modelos de crearsolicitud
from crearsolicitud.models import Solicitud, Usuario, Rol
# Importar modelos de consultarsolicitud
from consultarsolicitud.models import Estados

# Create your models here.

class Ficha(models.Model):
    idficha = models.AutoField(primary_key=True)
    codigoficha = models.IntegerField(unique=True)
    idsolicitud = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='idsolicitud')
    idestado = models.ForeignKey(Estados, models.DO_NOTHING, db_column='idestado')
    observacion = models.TextField()

    class Meta:
        managed = False
        db_table = 'ficha'