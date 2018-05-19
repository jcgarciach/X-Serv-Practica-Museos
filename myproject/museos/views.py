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
def pagprincipal(request):
    plantilla = loader.get_template('principio.html')
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
               
    context = RequestContext(request, {'listusuarios': listpreferencias, 'accesibilidad': accesibilidad, 'bestmuseos': bestmuseos, 'load': load})
    return(plantilla.render(context))

@csrf_exempt
 
def idmuseo(request, idm)
    if request.method == "GET":
# Queremos la id del museo y sus comentarios si tiene
        try: 
            museoid = Museo.objects.get(number = idm)
            comentarios = Comentario.objects.filter(museo_number = idm)
        
        except Museo.DoesNotExist:
        plantilla = loader.get_template('error.html')
            return HttpResponse(plantilla.render(), status=404) 
# En caso de no tener accederemos a hacer un comentario de dicho museo si asi lo queremos              
    else: 
        
        respuesta =  request.Post('text')
        museoid = Museo.objects.get(number = idm)
        newcoment = Comentario(texto = comentario, museo = museo)
        newcoment.save()
        plantilla = loader.get_template('museoid.html')
        comentarios = Comentario.object.filter(museo=museo)
        context = RequestContext(request, {'museo': museo, 'comentarios': comentarios})
        return(plantilla.render(context)
        
@csrf_exempt

def pagmuseos (request):
    plantilla = loader.get_template('pagsmuseos.html')
    if request.method == "POST":
#diferenciar lo del distrito
        if "opciones" in request.POST:
            distrito = request.POST['opciones']
            if distrito == "Todos"
                listmuseos = Museo.object.all()
            else:
                listmuseos = Museo.object.filter(distrito = distrito)
        else:
            if "Activar" in request.POST:
                auxm = request.POST['Activar']
                #troceamos
                idm = auxm.split(',')[0]
                nick = auxm.split(',')[1]
                museo = Museo.object.get(idm=idm)
                usuario = User.object.get(username=nick)
#para poner hora y fecha
#https://es.stackoverflow.com/questions/121867/implementación-hora-y-fecha-en-django

                hora = timezone()
                nuevaseleccion = Registro(usuario=usuario, museo=museo, fecha=hora)
                nuevaseleccion.save()
            else:
                auxm = request.POST['Desactivar']
                #trocear
                idm = auxm.split(',')[0]
                nick = auxm.split(',')[1]
                museo = Museo.object.get(idm=idm)
                usuario = User.object.get(username=nick)
                #debemos borrar esa seleccion
                borrarseleccion = Registro.object.get(usuario=usuario, museo=museo)
                borrarseleccion.delete()
        if request.method == "GET" or "opciones"not in  request.POST:
            listmuseos = Museo.object.all()
            distrito = "Todos"
"""
#obtener valores database de la lista de distritos para 
chat_messages.objects.all().values_list('name')
#obtener los valores lista
mynewlist = list(myset)
#lista->tupla
[i[0] for i in e]
"""    
        listmuseos = Museo.object.all().values_list('museo')
        listmuseo = list(set(listmuseos))
        listmuseo = [museo[0]ofr museo in listmuseo]
        if request.user.is_authenticated():
            registros = Registro.objects.all().values_list('museo').filter(usuario=request.user)
            listregistros = [registros[0]ofr registros in registros]
        else:
            registros = ""
        context = RequestContext(request, {'listdistrito': listdistrito, 'museos': listmuseos, 'distrito': distrito, 'registros': listregistros})
        return HttpResponse(plantilla.render(context))
        
def pagUser(request, nick):
    plantilla = loader.get_template('perfil.html')
    if request.method == "GET":
        try:
            usuario = User.objects.get(username=nick)
        except User.DoesNotExist:
            plantilla = loader.get_template('error.html')
            return HttpResponse(plantilla.render(),status = 404)
        qstring = request.META['Query_String']
    else:
        qstring = ""
        if request.user.is_authenticated():
            usuario = User.objects.get(username=request.user.username)
            try:
                usuario = Preferencias.objects.get(usuario=usuario)
            except:
                otherus = User.objects.get(username=request.user.username)
                usuario = Preferencia(usuario=otherus)
            if 'titulo' in request.POST:
                usuario.titulo = request.POST['titulo']
            else:
                usuario.tamLetra = request.POST['tamLetra']
                usuario.color = request.POST['color']
            usuario.save()
            
    usuario = User.objects.get(username=nick)
    if qs == "":
        registros = Registro.objects.filter(usuario=usuario)
    else:
        selecuser = Registro.objects.filter(id_gt=(int(qs)))
        registros = Registro.filter(usuario=usuario)
    
    if len(registros) <= 5:
        fin = True
    else:
        fin = False
    
    try:
        usuario = Prefencia.object.get(usuario=usuario)
    except:
        usuario = ""
    
    context = RequestContext(request, {'usuario': usuario, 'nick': nick, 'preferencias': preferencias, 'end': end})
        return HttpResponse(plantilla.render(context))



@csrf_exempt

def Login(request):
    if request.method == "POST":
        nick = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username = nombre, password = contrasenia)
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                
    return HttpResponseRedirect('/')
    
@csrf_exempt
  
def Logout(request):
    if request.method == "POST":
        logout(request)
        
    return HttpResponseRedirect('/')
    
def rss(request):
    plantilla = loader.get_template('rss/museo_comentarios.rss')
    comentarios = Comentario.objects.all()
    contexto = RequestContext(request, {'comentarios': comentarios})
    #https://stackoverflow.com/questions/595616/what-is-the-correct-mime-type-to-use-for-an-rss-feed
    return HttpResponse(plantilla.render(contexto),content_type="text/rss+xml")
    
def xml(request, nick):
    try:
        usuario = User.objects.get(username=nick)
    except User.DoesNotExist:
        plantilla = loader.get_template('error.html')

        return HttpResponse(plantilla.render(), status=404)

    plantilla = loader.get_template('xml/canal_usuario.xml')
    registros = Registro.objects.filter(usuario=usuario)
    context = RequestContext(request, {'usuario': usuario,
                              'registros': registros})

    return HttpResponse(plantilla.render(context), content_type="text/xml")    
 

def about(request):
    plantilla = loader.get_template('about.html')
    context = RequestContext(request)

    return HttpResponse(plantilla.render(context))       
