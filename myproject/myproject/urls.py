from django.conf.urls import include, url
from django.contrib import admin
from museos import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^/?$' , views.pagprincipal, name = 'Muestra la página principal'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^css/style.css$', views.css, name =  'Nos sirve el CSS'),
    url(r'^museos/?$', views.pagmuseos, name = 'Muestra la página con todos los museos'),
    url(r'^museos/(.*)/?$', views.idmuseo, name = 'Muestra la página de un museo'),
    url(r'^(.*)/xml/?$', views.xml, name = 'Canal XML'),
    url(r'^rss/?$', views.rss, name = 'Canal RSS para comentarios'),
    url(r'^login/?$', views.login, name = 'Login de los usuarios'),
    url(r'^logout/?$', views.logout, name = 'Logout de los usuarios'),
    url(r'^about/?$', views.about, name = 'Muestra la página about'),
    url(r'(.*)', views.pagUser, name = 'Muestra la pagina personal de un usuario'),
]
