from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .constantes import OPCIONES_ESTADO
from .forms import FormularioQueja
from .models import Departamento, Queja


class VistaListaQuejas(LoginRequiredMixin, ListView):
    model = Queja
    template_name = 'quejas/queja_lista.html'
    context_object_name = 'quejas'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            consulta = Queja.objects.select_related('autor', 'departamento').all()
        else:
            consulta = Queja.objects.select_related('autor', 'departamento').filter(
                autor=self.request.user
            )

        busqueda = self.request.GET.get('busqueda', '').strip()
        departamento = self.request.GET.get('departamento', '').strip()
        estado = self.request.GET.get('estado', '').strip()

        if busqueda:
            consulta = consulta.filter(
                Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda)
            )
        if departamento:
            consulta = consulta.filter(departamento__pk=departamento)
        if estado:
            consulta = consulta.filter(estado=estado)

        return consulta

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['departamentos'] = Departamento.objects.all()
        contexto['opciones_estado'] = OPCIONES_ESTADO
        contexto['busqueda'] = self.request.GET.get('busqueda', '')
        contexto['filtro_departamento'] = self.request.GET.get('departamento', '')
        contexto['filtro_estado'] = self.request.GET.get('estado', '')
        return contexto


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
        form.save_m2m()
        self.object = queja
        messages.success(self.request, 'Tu queja fue registrada correctamente.')
        return HttpResponseRedirect(queja.get_absolute_url())


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


class VistaVotarQueja(LoginRequiredMixin, View):
    def post(self, request, pk):
        queja = get_object_or_404(Queja, pk=pk)
        if queja.votos.filter(pk=request.user.pk).exists():
            queja.votos.remove(request.user)
            messages.info(request, 'Voto retirado.')
        else:
            queja.votos.add(request.user)
            messages.success(request, '¡Voto registrado!')
        return redirect(queja.get_absolute_url())


class VistaCambiarEstado(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Queja
    fields = ['estado']
    template_name = 'quejas/cambiar_estado.html'
    context_object_name = 'queja'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['opciones_estado'] = OPCIONES_ESTADO
        return contexto

    def get_success_url(self):
        messages.success(self.request, 'Estado actualizado correctamente.')
        return self.object.get_absolute_url()
