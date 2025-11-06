from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
# Create your models here.

class MissaoEspacial(models.Model):
    STATUS_CHOICES = [
        ('planejada', 'Planejada'),
        ('ativa', 'Ativa'),
        ('concluida', 'Concluída'),
        ('falhou', 'Falhou')
    ]
    
    nome = models.CharField(max_length=200, unique=True)  # REGRA: Nome único
    agencia = models.CharField(max_length=100)
    data_lancamento = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    objetivo = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    imagem = models.ImageField(upload_to='missoes/', null=True, blank=True)
    curiosidades = models.TextField()
    
    def clean(self):
        errors = {}
        
        # REGRA: Data de término deve ser após lançamento
        if self.data_termino and self.data_termino < self.data_lancamento:
            errors['data_termino'] = 'Data de término não pode ser anterior ao lançamento'
        
        # REGRA: Missões concluídas devem ter data de término
        if self.status in ['concluida', 'falhou'] and not self.data_termino:
            errors['data_termino'] = 'Missões concluídas ou falhas devem ter data de término'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean() # chama validação 
        super().save(*args, **kwargs) # salva no banco
    
    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})" # exibe nome da missao e seu status

class Astronauta(models.Model):
    nome = models.CharField(max_length=200, unique=True)  # REGRA: Nome único
    nacionalidade = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    foto = models.ImageField(upload_to='astronautas/', null=True, blank=True)
    biografia = models.TextField()
    missoes = models.ManyToManyField(MissaoEspacial, blank=True)
    
    @property
    def idade(self):
        today = date.today()
        return relativedelta(today, self.data_nascimento).years
    
    def clean(self):
        errors = {}
        
        # REGRA: Idade mínima para astronauta
        if self.idade < 18:
            errors['data_nascimento'] = 'Astronauta deve ter pelo menos 18 anos'
        
        # REGRA: Idade máxima realista
        if self.idade > 80:
            errors['data_nascimento'] = 'Idade muito avançada para atividades espaciais'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome