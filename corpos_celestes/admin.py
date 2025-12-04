from django.contrib import admin
from .models import Estrela, Planeta, SateliteNatural

class EstrelaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'classificacao_espectral', 'estagio_evolutivo', 'get_sistema_planetario')
    list_filter = ('classificacao_espectral', 'estagio_evolutivo')
    
    def get_sistema_planetario(self, obj):
        return obj.sistema_planetario.nome if obj.sistema_planetario else "-"
    get_sistema_planetario.short_description = 'Sistema Planetario'

class PlanetaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'diametro', 'temperatura_media', 'possui_agua', 'get_sistema_planetario']
    list_filter = ['tipo', 'possui_agua']
    search_fields = ['nome', 'curiosidades']
    raw_id_fields = ['sistema_planetario']
    
    def get_sistema_planetario(self, obj):
        return obj.sistema_planetario.nome if obj.sistema_planetario else "-"
    get_sistema_planetario.short_description = 'Sistema Planetario'

class SateliteNaturalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_planeta', 'diametro']
    search_fields = ['nome']
    raw_id_fields = ['planeta']
    
    def get_planeta(self, obj):
        return obj.planeta.nome
    get_planeta.short_description = 'Planeta'

admin.site.register(Estrela, EstrelaAdmin)
admin.site.register(Planeta, PlanetaAdmin)
admin.site.register(SateliteNatural, SateliteNaturalAdmin)