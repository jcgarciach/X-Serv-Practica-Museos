from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Museo, Comentario, Preferencia, Registro
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader
import urllib
from django.db.models import Count
# Para parsear y meterlos en listas importamos esto
import xml.sax
import xml.parsers.expat

import xmltodict

direcxml = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

@csrf_exempt
def Principal(request):

    if request.method == 'POST':
        if "button" in request.POST:
            option = request.POST("button")
            if option == "push on":
"""
https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending
"""
                bestmuseos = Museo.objects.annotate(num_coment=Count('comentario')).filter(accesibilidad=1).order_by('-num_comentarios')[:5]
                accesibilidad = True
            else:
                option == ""
                
                arch = urllib.request.urlopen (direcxml)
                datos = arch.read()
                datos = xmltodict.parse(datos)
                
                # Se inicializan las variables del modelo como listas
                idm_parseador = []
                nombre_parseador = []
                descripcion_parseador = []
                accesibilidad_parseador = []
                url_parseador = []
                via_parseador = []
                localidad_parseador = []
                provincia_parseador = []
                codigo_parseador = []
                barrio_parseador = []
                distrito_parseador = []
                latitud_parseador = []
                longitud_parseador = []
                telefono_parseador = []
                
                # Recorremos los datos para agregarlos a la lista desde la primera fila
                for idxmu, _ in enumerate(datos[['Contenidos']['contenido'][0:67], 0]):
                # Aqui vemos en que lugar se encuentra cada cosa dentro de los atributos para coger cada atributo correctamente
                    idm_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][0]['#text'])
                    nombre_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][1]['#text'])
                    descripcion_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][2]['#text'])
                    accesibilidad_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][3]['#text'])
                    url_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][4]['#text'])
                    via_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][0]['#text'])
                    localidad_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][4]['#text'])
                    provincia_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][5]['#text'])
                    codigo_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][6]['#text'])
                    barrio_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][7]['#text'])
                    distrito_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][8]['#text'])
                    latitud_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][-2]['#text'])
                    longitud_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][5]['atributo'][-1]['#text'])
                    telefono_parseador.append (datos['Contenidos']['contenido'][idxmu]['atributos']['atributo'][6]['atributo'][1]['#text'])
                    
                    print(idxmu)
                
                for indice, _ in enumerate(idm_parseador):
                    idm = idm_parseador[indice]
                    nombre = nombre_parseador[indice]
                    descripcion = descripcion_parseador[indice]
                    accesibilidad = accesibilidad_parseador[indice]
                    url = url_parseador[indice]
                    via = via_parseador[indice]
                    localidad = localidad_parseador[indice]
                    provincia = provincia_parseador[indice]
                    cp = codigo_parseador[indice]
                    barrio = barrio_parseador[indice]
                    distrito = distrito_parseador[indice]
                    latitud = latitud_parseador[indice]
                    longitud = longitud_parseador[indice]
                    telefono = telefono_parseador[indice]

        #guardamos los datos
                    new = Museo(
                        idm= idm,
                        nombre = nombre,
                        descripcion = descripcion,
                        accesibilidad = accesibilidad,
                        url = url,
                        via = via,
                        localidad = localidad,
                        provincia = provincia,
                        codigo_postal = cp,
                        barrio = barrio,
                        distrito = distrito,
                        latitud = latitud,
                        longitud = longitud,
                        telefono = telefono
                    )
                    new.save()

    if request.method == 'GET' or option == "push off" or option == "":
        bestmuseos = Museo.objects.annotate(num_coment=Count('comentario')).order_by('-num_comentarios')[:5]
        accesibilidad = False
    listpreferencias = Preferencia.object.all()
    listusuarios = User.object.all()
    if len(listpreferencias) != len(listusuarios)
        for usuario in listusuarios:
            try:
                user = Preferencia.object.all(usuario = usuario)
                except Preferencia.DoesNotExist:
                    user = Preferencia(usuario = usuario)
                    user.save()
        listpreferencias = Preferencia.object.all()
    listmuseos = Museo.object.all()
    if len(listmuseos) == 0:
        load = True    
    else:
        load = False
               
    return HttpResponse(request)
    
def idmuseo(request, idm)
    if request.method == "GET":
# Queremos la id del museo y sus comentarios si tiene
        try: 
            museoid = Museo.objects.get(number = idm)
            comentarios = Comentario.objects.filter(museo_number = idm)
        
        except Museo.DoesNotExist:
            return ("404")   
# En caso de no tener accederemos a hacer un comentario de dicho museo si asi lo queremos              
    else: 
        
        respuesta =  request.Post('text')
        museoid = Museo.objects.get(number = idm)
        newcoment = Comentario(texto = comentario, museo = museo)
        newcoment.save()
        
        respuesta = request       
        return (respuesta)
        
        
def Login(request):
    if request.method == "POST":
        nick = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username = nombre, password = contrasenia)
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                
    return HttpResponseRedirect('/')
    
    
def Logout(request):
    if request.method == "POST":
        logout(request)
        
    return HttpResponseRedirect('/')
    
    

    
        
