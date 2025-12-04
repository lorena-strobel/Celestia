from django.db import models
from django.core.exceptions import ValidationError
from universo.models import SistemaPlanetario
# Create your models here.

class Estrela(models.Model):

    # ----- CLASSIFICAÇÃO ESPECTRAL -----
    ESPECTRAL_CHOICES = [
        ('O', 'Azul muito quente'),
        ('B', 'Azul'),
        ('A', 'Branco-azulada'),
        ('F', 'Branca'),
        ('G', 'Amarela'),
        ('K', 'Laranja'),
        ('M', 'Vermelha'),
    ]

    # ----- ESTÁGIO EVOLUTIVO -----
    EVOLUCAO_CHOICES = [
        ('protoestrela', 'Protoestrela'),
        ('sequencia_principal', 'Sequência Principal'),
        ('ana_vermelha', 'Anã Vermelha'),
        ('ana_laranja', 'Anã Laranja'),
        ('ana_amarela', 'Anã Amarela'),
        ('ana_branca', 'Anã Branca'),
        ('gigante_vermelha', 'Gigante Vermelha'),
        ('gigante_azul', 'Gigante Azul'),
        ('supergigante_vermelha', 'Supergigante Vermelha'),
        ('supergigante_azul', 'Supergigante Azul'),
        ('hipergigante', 'Hipergigante'),
        ('estrela_neutrons', 'Estrela de Nêutrons'),
        ('pulsar', 'Pulsar'),
        ('magnetar', 'Magnetar'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    sistema_planetario = models.ForeignKey(
    SistemaPlanetario,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )
    
    classificacao_espectral = models.CharField(
    max_length=1,
    choices=ESPECTRAL_CHOICES,
    null=True,
    blank=True
    )

    estagio_evolutivo = models.CharField(
        max_length=50,
        choices=EVOLUCAO_CHOICES
    )

    massa = models.FloatField(
        help_text="1.0 = massa do Sol (1.989 × 10³⁰ kg)"
    )

    temperatura = models.IntegerField(
        help_text="Em Kelvin (ex: Sol = 5778 K)",
        null=True,
        blank=True
    )

    imagem = models.ImageField(upload_to='estrelas/', null=True, blank=True)

    descricao = models.TextField(
        blank=True,
        null=True
    )
    # VALIDAÇÕES
    def clean(self):
        errors = {}

        if self.massa < 0.075:
            errors['massa'] = 'Massa muito baixa para ser estrela (mínimo 0.08 massas solares).'

        if self.massa > 150:
             errors['massa'] = 'Massa acima do limite conhecido para estrelas (máximo 150 massas solares).'
        
        # validações para temperatura
        if self.temperatura and self.temperatura < 0:
            errors['temperatura'] = 'Temperatura deve ser em Kelvin (não pode ser negativa).'

        if self.temperatura and self.temperatura > 50000:
            errors['temperatura'] = 'Temperatura muito alta para uma estrela.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Estrela"           
        verbose_name_plural = "Estrelas"   
        ordering = ['nome']

class Planeta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    sistema_planetario = models.ForeignKey(
    SistemaPlanetario,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )
    tipo = models.CharField(max_length=20, choices=[
        ('rochoso', 'Rochoso'),
        ('gasoso', 'Gasoso'),
        ('gelado', 'Gelado'),
        ('anao', 'Anão'),
        ('superterra', 'Superterra'),
        ('mininetuno', 'Mini-Netuno'),
    ])
    diametro = models.FloatField(help_text="Em km")
    massa = models.FloatField(
        help_text="Massa em massas terrestres (1.0 = Terra)",
        null=True,
        blank=True
    )
    temperatura_media = models.IntegerField(
        help_text="Temperatura em Kelvin", 
        null=True, 
        blank=True
    )
    periodo_orbital = models.FloatField(
        help_text="Período orbital em dias terrestres",
        null=True,
        blank=True
    )

    possui_agua = models.BooleanField(default=False)
    possui_atmosfera = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='planetas/', null=True, blank=True)
    descricao = models.TextField(
        blank=True,
        null=True
    )
    
    def clean(self):
        errors = {}
        
        # REGRA: Diâmetro mínimo para planeta
        if self.diametro < 500:
            errors['diametro'] = 'Diâmetro muito pequeno para ser considerado planeta'
        
        # REGRA: Temperatura em Kelvin
        if self.temperatura_media and self.temperatura_media < 0:
            errors['temperatura_media'] = 'Temperatura não pode ser negativa (use Kelvin)'
        
        # Validação de massa
        if self.massa and self.massa < 0:
            errors['massa'] = 'Massa não pode ser negativa'

        if not self.nome or self.nome.strip() == "":
            errors['nome'] = 'Nome não pode ser vazio'

        if self.sistema_planetario_id:
            try:
                SistemaPlanetario.objects.get(id=self.sistema_planetario_id)
            except SistemaPlanetario.DoesNotExist:
                errors['sistema_planetario'] = 'Sistema planetário não existe'
                
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.clean() # chama a validação 
        super().save(*args, **kwargs) # salva no banco de dados
    
    def __str__(self):
        if self.sistema_planetario:
            return f"{self.nome} ({self.sistema_planetario.nome})"
        return self.nome
    
    class Meta:
        verbose_name = "Planeta"           
        verbose_name_plural = "Planetas"   
        ordering = ['nome']

class SateliteNatural(models.Model):
    nome = models.CharField(max_length=100)
    planeta = models.ForeignKey(Planeta, on_delete=models.CASCADE, related_name='satelites')
    diametro = models.FloatField(help_text="Em km")
    massa = models.FloatField(  
        help_text="Massa em kg",
        null=True,
        blank=True
    )
    imagem = models.ImageField(upload_to='satelites/', null=True, blank=True)
    
    descricao = models.TextField(
        blank=True,
        null=True
    )
    def clean(self):
        errors = {}
        
        if self.diametro < 1:
            errors['diametro'] = 'Diâmetro muito pequeno'
            
        if self.massa and self.massa < 0:
            errors['massa'] = 'Massa não pode ser negativa'
            
        if errors:
            raise ValidationError(errors)
        
    def __str__(self):
        return f"{self.nome} (lua de {self.planeta.nome})"
    
    class Meta:
        verbose_name = "Satélite Natural"
        verbose_name_plural = "Satélites Naturais"
        ordering = ['nome']