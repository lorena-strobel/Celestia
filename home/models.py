from django.db import models

# Create your models here.

class Destaque(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='destaques/')
    link = models.CharField(max_length=200, blank=True)
    ativo = models.BooleanField(default=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-data_publicacao']  # Regra: mais recentes primeiro
    
    def __str__(self):
        return self.titulo