from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Galaxia(models.Model):
    nome = models.CharField(max_length=100, unique=True)  # REGRA 1: Nome único
    tipo = models.CharField(max_length=50)
    diametro = models.FloatField(help_text="Em anos-luz", null=True, blank=True)
    imagem = models.ImageField(upload_to='galaxias/', null=True, blank=True)
    descricao = models.TextField()
    
    def clean(self):
        # REGRA: Diâmetro não pode ser negativo
        if self.diametro and self.diametro < 0:
            raise ValidationError({'diametro': 'Diâmetro não pode ser negativo'})
        
        # REGRA 3: Diâmetro máximo realista para galáxias
        if self.diametro and self.diametro > 1000000:  # 1 milhão de anos-luz
            raise ValidationError({'diametro': 'Diâmetro muito grande para uma galáxia'})
    
    def save(self, *args, **kwargs):
        self.clean() # chama a validação 
        super().save(*args, **kwargs) # salva no banco de dados
    
    def __str__(self):
        return self.nome

class SistemaPlanetario(models.Model):
    nome = models.CharField(max_length=100, unique=True)  # Nome único
    estrela_principal = models.CharField(max_length=100)
    galaxia = models.ForeignKey(Galaxia, on_delete=models.CASCADE)
    idade = models.FloatField(help_text="Em bilhões de anos", null=True, blank=True)
    imagem = models.ImageField(upload_to='sistemas/', null=True, blank=True)
    descricao = models.TextField()
    
    def clean(self):
        errors = {}
        
        # REGRA: Idade não pode ser maior que a idade do universo
        if self.idade and self.idade > 13.8:
            errors['idade'] = 'Idade não pode ser maior que a idade do universo (13.8 bilhões de anos)'
        
        # REGRA: Idade não pode ser negativa
        if self.idade and self.idade < 0:
            errors['idade'] = 'Idade não pode ser negativa'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean() # chama a validação 
        super().save(*args, **kwargs) # salva no banco de dados
    
    def __str__(self):
        return f"{self.nome} ({self.galaxia.nome})"
    

