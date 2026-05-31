from django import forms

from .models import Queja


class FormularioQueja(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['titulo', 'descripcion', 'tipo', 'departamento', 'anonima', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un título breve y descriptivo',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe detalladamente tu queja o sugerencia',
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'tipo': 'Tipo',
            'departamento': 'Departamento',
            'anonima': 'Enviar de forma anónima',
            'imagen': 'Imagen adjunta (opcional)',
        }
