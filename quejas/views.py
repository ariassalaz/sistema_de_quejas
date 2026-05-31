from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import FormularioQueja
from .models import Queja


class VistaListaQuejas(LoginRequiredMixin, ListView):
    model = Queja
    template_name = 'quejas/queja_lista.html'
    context_object_name = 'quejas'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Queja.objects.select_related('autor', 'departamento').all()
        return Queja.objects.select_related('autor', 'departamento').filter(
            autor=self.request.user
        )


class VistaDetalleQueja(LoginRequiredMixin, DetailView):
    model = Queja
    template_name = 'quejas/queja_detalle.html'
    context_object_name = 'queja'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['usuario_voto'] = self.object.votos.filter(pk=self.request.user.pk).exists()
        return contexto


class VistaCrearQueja(LoginRequiredMixin, CreateView):
    model = Queja
    form_class = FormularioQueja
    template_name = 'quejas/queja_formulario.html'

    def form_valid(self, form):
        queja = form.save(commit=False)
        if not queja.anonima:
            queja.autor = self.request.user
        queja.save()
        messages.success(self.request, 'Tu queja fue registrada correctamente.')
        return super().form_valid(form)


class VistaEditarQueja(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Queja
    form_class = FormularioQueja
    template_name = 'quejas/queja_formulario.html'

    def test_func(self):
        queja = self.get_object()
        return self.request.user.is_staff or queja.autor == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Queja actualizada correctamente.')
        return super().form_valid(form)


class VistaEliminarQueja(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Queja
    template_name = 'quejas/queja_confirmar_eliminar.html'
    context_object_name = 'queja'
    success_url = reverse_lazy('queja-lista')

    def test_func(self):
        queja = self.get_object()
        return self.request.user.is_staff or queja.autor == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Queja eliminada.')
        return super().form_valid(form)
