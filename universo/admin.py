from django.contrib import admin
from .models import Galaxia, SistemaPlanetario

# Register your models here.
class GalaxiaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'diametro']
    list_filter = ['tipo']
    search_fields = ['nome', 'descricao']

class SistemaPlanetarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'estrela_principal', 'galaxia', 'idade']
    list_filter = ['galaxia']
    search_fields = ['nome', 'estrela_principal']
    raw_id_fields = ['galaxia']

admin.site.register(Galaxia, GalaxiaAdmin)
admin.site.register(SistemaPlanetario, SistemaPlanetarioAdmin)