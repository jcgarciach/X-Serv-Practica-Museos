from django.contrib import admin

# Register your models here.

from museos.models import Museo
from museos.models import Comentario
from museos.models import Preferencia
from museos.models import Registro


admin.site.register(Museo)
admin.site.register(Comentario)
admin.site.register(Preferencia)
admin.site.register(Registro)
