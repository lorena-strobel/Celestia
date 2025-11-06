from django.db import models
from django.core.exceptions import ValidationError
from universo.models import SistemaPlanetario
# Create your models here.

class Estrela(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    sistema_planetario = models.ForeignKey(SistemaPlanetario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[
        ('ana_amarela', 'Anã Amarela'),
        ('ana_vermelha', 'Anã Vermelha'),
        ('gigante_vermelha', 'Gigante Vermelha'),
        ('gigante_azul', 'Gigante Azul'),
    ])
    massa = models.FloatField(
        help_text="1.0 = massa do Sol (1.989 × 10³⁰ kg)"
    )
    temperatura = models.IntegerField(
        help_text="Em Kelvin. Ex: Sol = 5778 K", 
        null=True, 
        blank=True
    )
    imagem = models.ImageField(upload_to='estrelas/', null=True, blank=True)
    
    def clean(self):
        errors = {}
        
        # REGRA: Massa mínima para ser estrela
        if self.massa < 0.08:
            errors['massa'] = 'Massa muito baixa para ser uma estrela (mínimo 0.08 massas solares)'
        
        # REGRA: Temperatura em Kelvin (não pode ser negativa)
        if self.temperatura and self.temperatura < 0:
            errors['temperatura'] = 'Temperatura não pode ser negativa (use Kelvin)'
        
        # REGRA: Temperatura realista para estrelas
        if self.temperatura and self.temperatura > 50000:
            errors['temperatura'] = 'Temperatura muito alta para uma estrela'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome

class Planeta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    sistema_planetario = models.ForeignKey(SistemaPlanetario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=[
        ('rochoso', 'Rochoso'),
        ('gasoso', 'Gasoso'),
        ('gelado', 'Gelado'),
        ('anao', 'Anão')
    ])
    diametro = models.FloatField(help_text="Em km")
    temperatura_media = models.IntegerField(
        help_text="Temperatura em Kelvin", 
        null=True, 
        blank=True
    )
    possui_agua = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='planetas/', null=True, blank=True)
    curiosidades = models.TextField()
    
    def clean(self):
        errors = {}
        
        # REGRA: Diâmetro mínimo para planeta
        if self.diametro < 100:
            errors['diametro'] = 'Diâmetro muito pequeno para ser considerado planeta'
        
        # REGRA: Temperatura em Kelvin
        if self.temperatura_media and self.temperatura_media < 0:
            errors['temperatura_media'] = 'Temperatura não pode ser negativa (use Kelvin)'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean() # chama a validação 
        super().save(*args, **kwargs) # salva no banco de dados
    
    def __str__(self):
        return f"{self.nome} ({self.sistema_planetario.nome})"

class SateliteNatural(models.Model):
    nome = models.CharField(max_length=100)
    planeta = models.ForeignKey(Planeta, on_delete=models.CASCADE)
    diametro = models.FloatField(help_text="Em km")
    imagem = models.ImageField(upload_to='satelites/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nome} (lua de {self.planeta.nome})"