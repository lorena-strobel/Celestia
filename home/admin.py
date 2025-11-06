from django.contrib import admin
from .models import Destaque
# Register your models here.

class DestaqueAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ativo', 'data_publicacao']
    list_filter = ['ativo']
    list_editable = ['ativo']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_publicacao'

admin.site.register(Destaque, DestaqueAdmin)