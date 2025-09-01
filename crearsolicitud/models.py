from django.db import models


class Tiposolicitud(models.Model):
    idtiposolicitud = models.AutoField(primary_key=True)
    tiposolicitud = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tiposolicitud'


class Programaespecial(models.Model):
    idespecial = models.AutoField(primary_key=True)
    programaespecial = models.CharField(max_length=100)

    def __str__(self):
        return self.programaespecial

    class Meta:
        managed = False
        db_table = 'programaespecial'


class Area(models.Model):
    idarea = models.AutoField(primary_key=True)
    area = models.CharField(max_length=150)

    def __str__(self):
        return self.area

    class Meta:
        managed = False
        db_table = 'area'


class Modalidad(models.Model):
    idmodalidad = models.AutoField(primary_key=True)
    modalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.modalidad

    class Meta:
        managed = False
        db_table = 'modalidad'


class Programaformacion(models.Model):
    codigoprograma = models.AutoField(primary_key=True)
    verision = models.CharField(max_length=250)
    nombreprograma = models.TextField(blank=True, null=True)
    horas = models.IntegerField()
    idarea = models.ForeignKey(Area, models.DO_NOTHING, db_column='idarea')
    idmodalidad = models.ForeignKey(Modalidad, models.DO_NOTHING, db_column='idmodalidad')

    def __str__(self):
        return self.nombreprograma or f"Programa {self.codigoprograma}"

    class Meta:
        managed = False
        db_table = 'programaformacion'


class Horario(models.Model):
    idhorario = models.AutoField(primary_key=True)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    mes1 = models.TextField(blank=True, null=True)
    mes2 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horario'


class Jornada(models.Model):
    idjornada = models.AutoField(primary_key=True)
    jornada = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'jornada'


class Departamentos(models.Model):
    codigodepartamentos = models.AutoField(primary_key=True)
    departamentos = models.CharField(max_length=200)

    def __str__(self):
        return self.departamentos

    class Meta:
        managed = False
        db_table = 'departamentos'


class Municipio(models.Model):
    codigomunicipio = models.AutoField(primary_key=True)
    municipio = models.CharField(max_length=255)
    codigodepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='codigodepartamento', to_field='codigodepartamentos')

    def __str__(self):
        return self.municipio

    class Meta:
        managed = False
        db_table = 'municipio'


class Tipoempresa(models.Model):
    idtipoempresa = models.AutoField(primary_key=True)
    tipoempresa = models.CharField(max_length=100)

    def __str__(self):
        return self.tipoempresa

    class Meta:
        managed = False
        db_table = 'tipoempresa'


class Empresa(models.Model):
    idempresa = models.AutoField(primary_key=True)
    nombreempresa = models.CharField(unique=True, max_length=255)
    representanteempresa = models.CharField(max_length=50)
    correoempresa = models.CharField(unique=True, max_length=200)
    nitempresa = models.IntegerField(unique=True)
    idtipoempresa = models.ForeignKey(Tipoempresa, models.DO_NOTHING, db_column='idtipoempresa')

    class Meta:
        managed = False
        db_table = 'empresa'


class Rol(models.Model):
    idrol = models.AutoField(primary_key=True)
    nombrerol = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'rol'


class Tipoidentificacion(models.Model):
    idtipoidentificacion = models.AutoField(primary_key=True)
    tipoidentificacion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipoidentificacion'


class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='rol')
    tipoidentificacion = models.ForeignKey(Tipoidentificacion, models.DO_NOTHING, db_column='tipoidentificacion')
    numeroidentificacion = models.IntegerField(unique=True)
    correo = models.CharField(unique=True, max_length=255)
    clave = models.CharField(max_length=255)
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'usuario'


class Ambiente(models.Model):
    idambiente = models.AutoField(primary_key=True)
    ambiente = models.CharField(max_length=250)

    def __str__(self):
        return self.ambiente

    class Meta:
        managed = False
        db_table = 'ambiente'


class Solicitud(models.Model):
    idsolicitud = models.AutoField(primary_key=True)
    idtiposolicitud = models.ForeignKey(Tiposolicitud, models.DO_NOTHING, db_column='idtiposolicitud')
    codigosolicitud = models.IntegerField()
    codigoprograma = models.ForeignKey(Programaformacion, models.DO_NOTHING, db_column='codigoprograma')
    idhorario = models.ForeignKey(Horario, models.DO_NOTHING, db_column='idhorario')
    cupo = models.IntegerField()
    idmodalidad = models.ForeignKey(Modalidad, models.DO_NOTHING, db_column='idmodalidad')
    codigomunicipio = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='codigomunicipio')
    direccion = models.CharField(max_length=255)
    idusuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='idusuario')
    idempresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='idempresa', blank=True, null=True)
    subsectoreconomico = models.CharField(max_length=100, blank=True, null=True)
    idespecial = models.ForeignKey(Programaespecial, models.DO_NOTHING, db_column='idespecial')
    convenio = models.CharField(max_length=20, blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, models.DO_NOTHING, db_column='ambiente', blank=True, null=True)
    fechasolicitud = models.DateField()

    class Meta:
        managed = False
        db_table = 'solicitud'
