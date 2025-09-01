from django.db import models
# Importar el modelo de la solicitud a esta app
from crearsolicitud.models import Solicitud

# Create your models here.

class Estados(models.Model):
    idestado = models.AutoField(primary_key=True)
    estados = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estados'