from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Museo(models.Model):
    idm = models.IntegerField()
    nombre = models.CharField(max_length = 100)
    descripcion = models.TextField()
    accesibilidad = models.IntegerField(choices = ((0, '0'), (1, '1'))
    url = models.URLField(max_length = 300)
    via = models.CharField(max_length=100)
    localidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    codigo_postal = models.PositiveSmallIntegerField(null = True, blank = True)
    barrio = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50, blank = True)
    latitud = models.FloatField(null = True, blank = True)
    longitud = models.FloatField(null = True, blank = True)
    telefono = models.CharField(max_length=50, default='S/T')

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, null = True)
    museo = models.ForeignKey(Museo, null = True)
    texto = models.TextField()
    fecha = models.DateTimeField()
    def __str__(self):
        return (self.texto)

class Registro(models.Model):
    usuario = models.ForeignKey('Usuario')
    museo = models.ForeignKey('Museo')
    fecha = models.DateTimeField()
    def __str__(self):
        return str(self.id)
        
class Preferencia(models.Model):
    usuario = models.ForeignKey('Usuario')
    tamLetra = models.IntegerField(max_length=50, blank = True)
    titulo = models.CharField(max_length=50, blank = True)
    color = models.CharField(max_length=50, blank = True)
    def __str__(self):
        return self.usuario
    

