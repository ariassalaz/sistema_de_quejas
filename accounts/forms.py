from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
    )
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {'username': 'Nombre de usuario'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.save()
        return usuario


class FormularioPerfil(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'bio': 'Biografía',
            'avatar': 'Foto de perfil',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe algo sobre ti...',
            }),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
