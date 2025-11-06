from django.contrib import admin
from .models import MissaoEspacial, Astronauta
# Register your models here.
class MissaoEspacialAdmin(admin.ModelAdmin):
    list_display = ['nome', 'agencia', 'status', 'data_lancamento', 'data_termino']
    list_filter = ['status', 'agencia']
    search_fields = ['nome', 'objetivo']
    date_hierarchy = 'data_lancamento'

class AstronautaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nacionalidade', 'idade', 'data_nascimento']
    list_filter = ['nacionalidade']
    search_fields = ['nome', 'biografia']
    filter_horizontal = ['missoes'] 

admin.site.register(MissaoEspacial, MissaoEspacialAdmin)
admin.site.register(Astronauta,AstronautaAdmin)