from django.contrib import admin
from .models import Estrela, Planeta, SateliteNatural
# Register your models here.

class EstrelaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'massa', 'temperatura', 'sistema_planetario']
    list_filter = ['tipo']
    search_fields = ['nome']
    raw_id_fields = ['sistema_planetario']

class PlanetaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'diametro', 'temperatura_media', 'possui_agua', 'sistema_planetario']
    list_filter = ['tipo', 'possui_agua']
    search_fields = ['nome', 'curiosidades']
    raw_id_fields = ['sistema_planetario']

class SateliteNaturalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'planeta', 'diametro']
    search_fields = ['nome']
    raw_id_fields = ['planeta']

admin.site.register(Estrela, EstrelaAdmin)
admin.site.register(Planeta, PlanetaAdmin)
admin.site.register(SateliteNatural, SateliteNaturalAdmin)