from django.contrib import admin

from museos.models import Museo
from museos.models import Comentario
from museos.models import Registro
from museos.models import Preferencia


admin.site.register(Museo)
admin.site.register(Comentario)
admin.site.register(Registro)
admin.site.register(Preferencia)
