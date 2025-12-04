from django import forms
from .models import Estrela, Planeta, SateliteNatural

# forms de corpos_celestes 

class EstrelaForm(forms.ModelForm):
    class Meta:
        model = Estrela
        fields = [
            'nome',
            'sistema_planetario',
            'classificacao_espectral',
            'estagio_evolutivo',
            'massa',
            'temperatura',
            'imagem',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}), 
        }


class PlanetaForm(forms.ModelForm):
    class Meta:
        model = Planeta
        fields = "__all__"
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'diametro': forms.NumberInput(attrs={'step': '0.1'}),
            'massa': forms.NumberInput(attrs={'step': '0.001'}),
            'temperatura_media': forms.NumberInput(attrs={'min': '0'}),
            'periodo_orbital': forms.NumberInput(attrs={'step': '0.01'}),
        }

class SateliteNaturalForm(forms.ModelForm):
    class Meta:
        model = SateliteNatural
        fields = "__all__"
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'diametro': forms.NumberInput(attrs={'step': '0.1'}),
            'massa': forms.NumberInput(attrs={'step': '0.001'}),
        }