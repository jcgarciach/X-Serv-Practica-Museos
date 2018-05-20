from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 

class Museo (models.Model):
    idEntidad = models.IntegerField()
    nombre = models.CharField(max_length=200, default='')
    descripcion = models.TextField(default = '', blank = True)
    accesibilidad = models.IntegerField(choices=((0, '0'), (1, '1')))
    url = models.CharField(max_length=200, default='', blank = True)
    via = models.CharField(max_length=100, default='', blank=True)
    localidad = models.CharField(max_length=100, default='', blank=True)
    provincia = models.CharField(max_length=30, default='', blank = True)
    codigo_postal = models.PositiveSmallIntegerField(null=True, blank = True)
    barrio = models.CharField(max_length=200, default='', blank = True)
    distrito = models.CharField(max_length=200, default='', blank = True)
    latitud = models.FloatField(null = True, blank = True)
    longitud = models.FloatField(null = True, blank = True)
    telefono = models.CharField(max_length=40, default="S/T")

    	
class Comentario (models.Model):
    texto = models.TextField()
    museo = models.ForeignKey('Museo')

     
class Preferencia (models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50, blank=True)
    tamanioLetra = models.CharField(max_length=50, blank=True)
    colorFondo = models.CharField(max_length=20, blank=True)


class Registro (models.Model):
    museo = models.ForeignKey('Museo')
    usuario = models.ForeignKey(User)
    fechaHora = models.DateTimeField()
