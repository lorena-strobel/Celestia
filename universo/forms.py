from django import forms
from django.core.exceptions import ValidationError
from .models import Galaxia, Nebulosa, SistemaPlanetario

class GalaxiaForm(forms.ModelForm):
    class Meta:
        model = Galaxia
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: Galáxia espiral localizada no Grupo Local...',
                'required': True
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex: Via Láctea, Andrômeda...'
            }),
            'diametro': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '100000',
                'min': '0'
            }),
            'massa': forms.NumberInput(attrs={
                'step': '0.001',
                'placeholder': '1000',
                'min': '0'
            }),
            'distancia_terra': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '2.5',
                'min': '0'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'diametro': 'Em anos-luz. Ex: Via Láctea tem ~100.000 anos-luz',
            'massa': 'Em massas solares (1 = massa do Sol)',
            'distancia_terra': 'Em milhões de anos-luz',
        }
    
    def clean_diametro(self):
        diametro = self.cleaned_data.get('diametro')
        if diametro and diametro > 1000000:
            raise ValidationError('Diâmetro muito grande para uma galáxia (máximo: 1.000.000 anos-luz)')
        return diametro
    
    def clean_massa(self):
        massa = self.cleaned_data.get('massa')
        if massa and massa > 10000000:  # 10 milhões de massas solares
            raise ValidationError('Massa muito grande (máximo: 10.000.000 massas solares)')
        return massa

class SistemaPlanetarioForm(forms.ModelForm):
    class Meta:
        model = SistemaPlanetario
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: Sistema com 8 planetas orbitando uma estrela tipo G...',
                'required': True
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex: Sistema Solar, TRAPPIST-1...'
            }),
            'estrela_principal': forms.TextInput(attrs={
                'placeholder': 'Ex: Sol, TRAPPIST-1...'
            }),
            'idade': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '4.6',
                'min': '0',
                'max': '13.8'
            }),
            'numero_planetas': forms.NumberInput(attrs={
                'min': '0',
                'max': '100',
                'placeholder': '8'
            }),
            'galaxia': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'idade': 'Em bilhões de anos (Universo tem 13.8 bilhões)',
            'numero_planetas': 'Planetas confirmados (0-100)',
        }
    
    def clean_numero_planetas(self):
        num = self.cleaned_data.get('numero_planetas')
        if num is not None and num < 0:
            raise ValidationError('Número de planetas não pode ser negativo')
        if num and num > 100:
            raise ValidationError('Número muito alto de planetas (máximo: 100)')
        return num

class NebulosaForm(forms.ModelForm):
    class Meta:
        model = Nebulosa
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: Nebulosa formada por remanescente de supernova...',
                'required': True
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex: Nebulosa do Caranguejo, Orion...'
            }),
            'distancia': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '1344',
                'min': '0'
            }),
            'diametro': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': '3.0',
                'min': '0'
            }),
            'magnitude': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '8.3'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'distancia': 'Em anos-luz (máximo: 100.000)',
            'diametro': 'Em anos-luz',
            'magnitude': 'Quanto menor, mais brilhante. Ex: Sirius = -1.46',
        }
    
    def clean_distancia(self):
        distancia = self.cleaned_data.get('distancia')
        if distancia is not None:
            if distancia < 0:
                raise ValidationError('Distância não pode ser negativa')
            if distancia > 100000:
                raise ValidationError('Distância muito grande (máximo: 100.000 anos-luz)')
        return distancia