"""
https://docs.djangoproject.com/en/1.8/topics/http/urls/
# Examples:
# url(r'^$', 'myproject.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
"""

from django.conf.urls import include, url
from django.contrib import admin
from museos import views
from django.contrib.auth.views import login, logout

urlpatterns = [
	url(r'^/?$',views.pagprincipal, name='pagina principal'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^css/style.css$',views.css, name='css'),
    url(r'^login/?$',views.loginUser, name=' Login de usuario'),
    url(r'^logout/?$',views.logoutUser, name=' Logout de usuario'),
    url(r'^museos/?$',views.pagsmuseos, name='Pagina de todos los museos'),
    url(r'^museos/(.*)/?$',views.pagmuseo, name='Pag de un museo'),
    url(r'^(.*)/xml/?$',views.xml, name='canal xml'),
    url(r'^about/?$',views.about, name='info en html autoria'),
	url(r'^rss/?$',views.rss, name='comentarios'),
	url(r'(.*)',views.paguser, name='Pagina del usuario'),
]
