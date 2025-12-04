from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Galaxia(models.Model):
    TIPO_CHOICES = [
        ('espiral', 'Espiral'),
        ('eliptica', 'Elíptica'),
        ('irregular', 'Irregular'),
        ('lenticular', 'Lenticular'),
        ('anã', 'Galáxia Anã'),
    ]
    nome = models.CharField(max_length=100, unique=True)  # Nome único
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    diametro = models.FloatField(help_text="Em anos-luz", null=True, blank=True)
    massa = models.FloatField(
        help_text="Massa em massas solares",
        null=True, 
        blank=True
    )
    distancia_terra = models.FloatField(
        help_text="Distância da Terra em anos-luz",
        null=True,
        blank=True
    )
    imagem = models.ImageField(upload_to='galaxias/', null=True, blank=True)
    descricao = models.TextField()
    
    def clean(self):
        errors = {}
        # Diâmetro não pode ser negativo
        if self.diametro and self.diametro < 0:
            errors['diametro'] = 'Diâmetro não pode ser negativo'
        
        if self.diametro and self.diametro > 1000000:
            errors['diametro'] = 'Diâmetro muito grande para uma galáxia'
            
        if self.massa and self.massa < 0:
            errors['massa'] = 'Massa não pode ser negativa'
            
        if self.distancia_terra and self.distancia_terra < 0:
            errors['distancia_terra'] = 'Distância não pode ser negativa'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Galáxia"
        verbose_name_plural = "Galáxias"
        ordering = ['nome']

class SistemaPlanetario(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    estrela_principal = models.CharField(max_length=100)
    
    galaxia = models.ForeignKey(
        Galaxia, 
        on_delete=models.PROTECT,  
        related_name='sistemas_planetarios'
    )
    
    idade = models.FloatField(help_text="Em bilhões de anos", null=True, blank=True)
    numero_planetas = models.IntegerField(
        help_text="Número de planetas confirmados",
        null=True,
        blank=True
    )
    imagem = models.ImageField(upload_to='sistemas/', null=True, blank=True)
    descricao = models.TextField()
    
    def clean(self):
        errors = {}
        
        if self.idade and self.idade > 13.8:
            errors['idade'] = 'Idade não pode ser maior que a idade do universo (13.8 bilhões de anos)'
        
        if self.idade and self.idade < 0:
            errors['idade'] = 'Idade não pode ser negativa'
            
        if self.numero_planetas and self.numero_planetas < 0:
            errors['numero_planetas'] = 'Número de planetas não pode ser negativo'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome} ({self.galaxia.nome})"
    
    class Meta:
        verbose_name = "Sistema Planetário"
        verbose_name_plural = "Sistemas Planetários"
        ordering = ['nome']


class Nebulosa(models.Model):
    TIPO_CHOICES = [
        ('emissao', 'Nebulosa de Emissão'),
        ('reflexao', 'Nebulosa de Reflexão'),
        ('negra', 'Nebulosa Escura'),
        ('planetaria', 'Nebulosa Planetária'),
        ('supernova', 'Remanescente de Supernova'),
    ]
    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    distancia = models.FloatField(help_text="Em anos-luz",null=True,blank=True)
    diametro = models.FloatField(
        help_text="Diâmetro em anos-luz",
        null=True,
        blank=True
    )
    magnitude = models.FloatField(
        help_text="Magnitude aparente",
        null=True,
        blank=True
    )
    descricao = models.TextField()
    imagem = models.ImageField(upload_to="nebulosas/", null=True, blank=True)
    
    def clean(self):
        errors = {}

        if self.distancia is not None and self.distancia < 0:
            errors['distancia'] = 'A distância não pode ser negativa.'

        if self.distancia is not None and self.distancia > 100000:
            errors['distancia'] = 'Distância muito grande para uma nebulosa dentro de uma galáxia.'
            
        if self.diametro is not None and self.diametro < 0:
            errors['diametro'] = 'Diâmetro não pode ser negativo'
            
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Nebulosa"
        verbose_name_plural = "Nebulosas"
        ordering = ['nome']