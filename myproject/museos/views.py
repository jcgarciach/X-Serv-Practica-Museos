from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Museo, Comentario, Preferencia, Registro
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader
import urllib






@csrf_exempt
def Principal(request):
    if request.method == 'GET':
        
    else:
               
    return HttpResponse()
        
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
    

    
        
