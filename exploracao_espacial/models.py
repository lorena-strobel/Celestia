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
        ('falhou', 'Falhou'),
        ('cancelada', 'Cancelada'),
    ]

    TIPO_CHOICES = [
        ('orbital', 'Orbital'),
        ('lunar', 'Lunar'),
        ('planetaria', 'Planetária'),
        ('solar', 'Sistema Solar'),
        ('interestelar', 'Interestelar'),
        ('observacao', 'Observação'),
        ('comunicacao', 'Comunicação'),
        ('ciencia', 'Ciência')
    ]
    
    nome = models.CharField(max_length=200, unique=True)
    agencia = models.CharField(max_length=100)
    data_lancamento = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    objetivo = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='orbital')
    orcamento = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Orçamento em milhões de dólares"
    )
    imagem = models.ImageField(upload_to='missoes/', null=True, blank=True)
    curiosidades = models.TextField()
    
    def clean(self):
        errors = {}

        # Data de término não pode ser antes do lançamento
        if self.data_termino and self.data_termino < self.data_lancamento:
            errors['data_termino'] = 'Data de término não pode ser anterior ao lançamento'

        # Missões concluídas e falhas DEVEM ter data de término
        if self.status in ['concluida', 'falhou'] and not self.data_termino:
            errors['data_termino'] = 'Missões concluídas ou falhas devem ter data de término'

        # Missão ATIVA não pode ter data de término no passado
        if self.status == 'ativa' and self.data_termino and self.data_termino < date.today():
            errors['data_termino'] = 'Missão ativa não pode ter data de término no passado'

        # Missão CONCLUÍDA não pode ter término no futuro
        if self.status == 'concluida' and self.data_termino and self.data_termino > date.today():
            errors['data_termino'] = 'Missão concluída não pode ter data de término no futuro'

        if errors:
            raise ValidationError(errors)
    
    @property
    def duracao_dias(self):
        if self.data_termino:
            return (self.data_termino - self.data_lancamento).days
        elif self.status == 'ativa':
            return (date.today() - self.data_lancamento).days
        return None
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = "Missão Espacial"
        verbose_name_plural = "Missões Espaciais"
        ordering = ['-data_lancamento']

class Astronauta(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('aposentado', 'Aposentado'),
        ('falecido', 'Falecido')
    ]
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    ]
    
    nome = models.CharField(max_length=200, unique=True)
    nacionalidade = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    data_falecimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='M')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    foto = models.ImageField(upload_to='astronautas/', null=True, blank=True)
    biografia = models.TextField()
    missoes = models.ManyToManyField(MissaoEspacial, blank=True, related_name='tripulantes')
    
    @property
    def idade(self):
        today = date.today()
        if self.data_falecimento:
            return relativedelta(self.data_falecimento, self.data_nascimento).years
        return relativedelta(today, self.data_nascimento).years
    
    @property
    def esta_vivo(self):
        return not self.data_falecimento
    
    @property
    def total_missoes(self):
        return self.missoes.count()
    
    def clean(self):
        errors = {}
        
        # Idade mínima para astronauta
        if self.idade < 18:
            errors['data_nascimento'] = 'Astronauta deve ter pelo menos 18 anos'
        
        # Idade máxima realista
        if self.idade > 80 and self.status == 'ativo':
            errors['data_nascimento'] = 'Idade muito avançada para atividades espaciais ativas'
        
        # Validação de data de falecimento
        if self.data_falecimento and self.data_falecimento < self.data_nascimento:
            errors['data_falecimento'] = 'Data de falecimento não pode ser anterior ao nascimento'
        
        if self.data_falecimento and self.data_falecimento > date.today():
            errors['data_falecimento'] = 'Data de falecimento não pode ser no futuro'
        
         # Consistência entre vida e status
        if self.data_falecimento and self.status != 'falecido':
            errors['status'] = 'Astronauta com data de falecimento deve ter status "Falecido"'

        if not self.data_falecimento and self.status == 'falecido':
            errors['status'] = 'Astronauta marcado como falecido deve ter data de falecimento'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Astronauta"
        verbose_name_plural = "Astronautas"
        ordering = ['nome']