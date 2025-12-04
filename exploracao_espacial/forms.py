from django import forms
from .models import MissaoEspacial, Astronauta

class MissaoEspacialForm(forms.ModelForm):
    class Meta:
        model = MissaoEspacial
        fields = '__all__'
        widgets = {
            'data_lancamento': forms.DateInput(attrs={'type': 'date'}),
            'data_termino': forms.DateInput(attrs={'type': 'date'}),
            'objetivo': forms.Textarea(attrs={'rows': 4}),
            'curiosidades': forms.Textarea(attrs={'rows': 4}),
            'orcamento': forms.NumberInput(attrs={'step': '0.01'}),
        }

class AstronautaForm(forms.ModelForm):
    class Meta:
        model = Astronauta
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_falecimento': forms.DateInput(attrs={'type': 'date'}),
            'biografia': forms.Textarea(attrs={'rows': 6}),
            'missoes': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }