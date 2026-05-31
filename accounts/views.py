from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import FormularioRegistro
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
    template_name = 'accounts/editar_perfil.html'
    fields = ['first_name', 'last_name', 'email', 'bio', 'avatar']
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user
