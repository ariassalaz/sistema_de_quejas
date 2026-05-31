from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import FormularioRegistro, FormularioPerfil
from .models import CustomUser


class VistaRegistro(CreateView):
    form_class = FormularioRegistro
    template_name = 'accounts/registro.html'
    success_url = reverse_lazy('iniciar-sesion')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)


class VistaPerfil(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/perfil.html'
    context_object_name = 'usuario_perfil'

    def get_object(self):
        return self.request.user


class VistaEditarPerfil(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = FormularioPerfil
    template_name = 'accounts/editar_perfil.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)
