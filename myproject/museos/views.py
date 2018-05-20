from django.shortcuts import render, render_to_response
from museos.models import Museo, Comentario
from museos.models import Preferencia, Registro
from django.contrib.auth import authenticate, login, logout
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from django.utils import timezone
from urllib.request import urlopen
# Create your views here.

direccion = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
@csrf_exempt
def pagprincipal(request):
    plantilla = get_template('principal.html')

    if request.method == "POST":
        if "boton" in request.POST:
            opcion = request.POST['boton']
            if opcion == "Activar":
            
# https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending


                masComentados = Museo.objects.annotate(
                                num_com=Count('comentario')).filter(
                                accesibilidad=1).order_by('-num_com')[:5]
                accesibilidad = True
        else:
            opcion = ""
            xmlfile = urlopen(direccion)
            arbol = ET.parse(xmlarchivo)
            raiz = arbol.getroot()

            for elem in arbol.iter():
                if "ID-ENTIDAD" in elem.attrib.values():   # Es un diccionario
                    nuevoMuseo = Museo(idEntidad=elem.text)
                elif "NOMBRE" in elem.attrib.values():
                    nuevoMuseo.nombre = elem.text
                elif "DESCRIPCION" in elem.attrib.values():
                    nuevoMuseo.descripcion = elem.text
                elif "ACCESIBILIDAD" in elem.attrib.values():
                    nuevoMuseo.accesibilidad = elem.text
                elif "CONTENT-URL" in elem.attrib.values():
                    nuevoMuseo.url = elem.text
                elif "NOMBRE-VIA" in elem.attrib.values():
                    nuevoMuseo.via = elem.text
                elif "LOCALIDAD" in elem.attrib.values():
                    nuevoMuseo.localidad = elem.text
                elif "PROVINCIA" in elem.attrib.values():
                    nuevoMuseo.provincia = elem.text
                elif "CODIGO-POSTAL" in elem.attrib.values():
                    nuevoMuseo.codigo_postal = elem.text
                elif "BARRIO" in elem.attrib.values():
                    nuevoMuseo.barrio = elem.text
                elif "LATITUD" in elem.attrib.values():
                    nuevoMuseo.latitud = elem.text
                elif "LONGITUD" in elem.attrib.values():
                    nuevoMuseo.longitud = elem.text
                elif "TELEFONO" in elem.attrib.values():
                    nuevoMuseo.telefono = elem.text
                elif "TIPO" in elem.attrib.values():
                    nuevoMuseo.save()
                else:
                    pass

    if request.method == "GET" or opcion == "Desactivar" or opcion == "":
        masComentados = Museo.objects.annotate(
                        num_com=Count('comentario')).order_by('-num_com')[:5]
        accesibilidad = False

    listaPreferencias = Preferencia.objects.all()
    listaUsuarios = User.objects.all()
    if len(listaPreferencias) != len(listaUsuarios):
        for usuario in listaUsuarios:
            try:
                user = Preferencia.objects.get(usuario=usuario)
            except Preferencia.DoesNotExist:
                user = Preferencia(usuario=usuario)
                user.save()

        listaPreferencias = Preferencia.objects.all()

    listaMuseos = Museo.objects.all()
    if len(listaMuseos) == 0:
        cargar = True
    else:
        cargar = False

    contexto = RequestContext(request, {'listaUsuarios': listaPreferencias,
                                        'accesibilidad': accesibilidad,
                                        'masComentados': masComentados,
                                        'cargar': cargar})

    return HttpResponse(plantilla.render(contexto))


def css(request):
    plantilla = get_template('css/style.css')
    if request.user.is_authenticated():
        usuario = User.objects.get(username=request.user.username)
        try:
            usuario = Preferencia.objects.get(usuario=usuario)
        except:
            return HttpResponse(plantilla.render(), content_type="text/css")

        contexto = Context({'color': usuario.colorFondo,
                            'tamanio': usuario.tamanioLetra})

        return HttpResponse(plantilla.render(contexto),
                            content_type="text/css")

    else:
        return HttpResponse(plantilla.render(), content_type="text/css")

@csrf_exempt
def paguser(request, nick):
    if request.method == "GET":
        try:
            usuario = User.objects.get(username=nick)
        except User.DoesNotExist:
            plantilla = get_template('error.html')

            return HttpResponse(plantilla.render(), status=404)
# Como obtener una query string:
        # https://docs.djangoproject.com/en/1.8/ref/request-response/#django.http.HttpRequest.META
        queri = request.META['QUERY_STRING']

    else:
        queri = ""
        if request.user.is_authenticated():
            usuario = User.objects.get(username=request.user.username)
            try:
                usuario = Preferencia.objects.get(usuario=usuario)
            except:
                user = User.objects.get(username=request.user.username)
                usuario = Preferencia(usuario=user)

            if 'titulo' in request.POST:
                usuario.titulo = request.POST['titulo']
            else:
                usuario.tamanioLetra = request.POST['tamanioLetra']
                usuario.colorFondo = request.POST['colorFondo']
            usuario.save()

    plantilla = get_template('perfil.html')
    usuario = User.objects.get(username=nick)
    if queri == "":
        seleccionados = Registro.objects.filter(usuario=usuario)
    else:
# Como extraer entradas utilizando los operadores de desigualdad:
        # http://stackoverflow.com/questions/10040143/how-to-do-a-less-than-or-equal-to-filter-in-django-queryset
        restantes = Registro.objects.filter(id__gt=(int(queri)))
        seleccionados = restantes.filter(usuario=usuario)

    if len(seleccionados) <= 5:
        fin = True
    else:
        fin = False

    try:
        usuario = Preferencia.objects.get(usuario=usuario)
    except:
        usuario = ""

    contexto = RequestContext(request, {'usuario': usuario,
                                        'nick': nick,
                                        'seleccionados': seleccionados,
                                        'fin': fin})

    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def loginUser(request):
    if request.method == "POST":
        nick = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username=nick, password=password)
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)

    return HttpResponseRedirect('/')

@csrf_exempt
def logoutUser(request):
    if request.method == "POST":
        logout(request)

    return HttpResponseRedirect('/')

@csrf_exempt
def pagsmuseos(request):
    plantilla = get_template('pagsmuseos.html')
    if request.method == "POST":

#diferenciar lo del distrito

        if "opciones" in request.POST:
            distrito = request.POST['opciones']
            if distrito == "Todos":
                listaMuseos = Museo.objects.all()
            else:
                listaMuseos = Museo.objects.filter(
                                     distrito=distrito)
        else:
            if "marcar" in request.POST:
                recibido = request.POST['marcar']
                #troceamos
                idEntidad = recibido.split(',')[0]
                nick = recibido.split(',')[1]
                museo = Museo.objects.get(idEntidad=idEntidad)
                usuario = User.objects.get(username=nick)
#para poner hora y fecha
#https://es.stackoverflow.com/questions/121867/implementación-hora-y-fecha-en-django

                fechaHora = timezone.now()
                newSeleccion = Registro(museo=museo,
                                            usuario=usuario,
                                            fechaHora=fechaHora)
                newSeleccion.save()
            else:
                recibido = request.POST['desmarcar']
                #troceamos
                idEntidad = recibido.split(',')[0]
                nick = recibido.split(',')[1]
                museo = Museo.objects.get(idEntidad=idEntidad)
                usuario = User.objects.get(username=nick)
                #debemos borrar esa seleccion
                deleteSeleccion = Registro.objects.get(
                                  museo=museo, usuario=usuario)
                deleteSeleccion.delete()

    if request.method == "GET" or "opciones" not in request.POST:
        listaMuseos = Museo.objects.all()
        distrito = "Todos"

#obtener valores database de la lista de distritos para 
#chat_messages.objects.all().values_list('name')
#obtener los valores lista
#mynewlist = list(myset)
#lista->tupla
#[i[0] for i in e]


    listaDistritos = Museo.objects.all().values_list('distrito')
    listaDistritosUnicos = list(set(listaDistritos))
    listaDistritosUnicos = [distrito[0] for distrito in listaDistritosUnicos]

    if request.user.is_authenticated():
        seleccionados = Registro.objects.all().values_list(
                        'museo').filter(usuario=request.user)
        listaSeleccionados = [seleccionado[0] for seleccionado
                              in seleccionados]
    else:
        listaSeleccionados = ""

    contexto = RequestContext(request, {'listaDistritos': listaDistritosUnicos,
                                        'museos': listaMuseos,
                                        'distrito': distrito,
                                        'seleccionados': listaSeleccionados})

    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def pagmuseo(request, idEntidad):
    if request.method == "GET":
    # Queremos la id del museo y sus comentarios si tiene
        try:
            museo = Museo.objects.get(idEntidad=idEntidad)
        except Museo.DoesNotExist:
            plantilla = get_template('error.html')

            return HttpResponse(plantilla.render(), status=404)
# En caso de no tener accederemos a hacer un comentario de dicho museo si asi lo queremos 
    else: 
        comentario = request.POST['texto']
        museo = Museo.objects.get(idEntidad=idEntidad)
        newComentario = Comentario(texto=comentario,
                                     museo=museo)
        newComentario.save()

    plantilla = get_template('pagmuseo.html')
    comentarios = Comentario.objects.filter(museo=museo)
    contexto = RequestContext(request, {'museo': museo,
                              'comentarios': comentarios})

    return HttpResponse(plantilla.render(contexto))

def about(request):
    plantilla = get_template('about.html')
    contexto = RequestContext(request)

    return HttpResponse(plantilla.render(contexto))    

def xml(request, nick):
    try:
        usuario = User.objects.get(username=nick)
    except User.DoesNotExist:
        plantilla = get_template('error.html')

        return HttpResponse(plantilla.render(), status=404)

    plantilla = get_template('xml/museos.xml')
    seleccionados = Registro.objects.filter(usuario=usuario)
    contexto = RequestContext(request, {'usuario': usuario,
                              'seleccionados': seleccionados})

    return HttpResponse(plantilla.render(contexto), content_type="text/xml")


def rss(request):
    plantilla = get_template('rss/comentarios.rss')
    comentarios = Comentario.objects.all()
    contexto = RequestContext(request, {'comentarios': comentarios})
 #https://stackoverflow.com/questions/595616/what-is-the-correct-mime-type-to-use-for-an-rss-feed
    return HttpResponse(plantilla.render(contexto),
                        content_type="text/rss+xml")

