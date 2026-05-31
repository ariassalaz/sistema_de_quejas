from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .constantes import OPCIONES_ESTADO, OPCIONES_TIPO, COLOR_ESTADO
from .forms import FormularioQueja
from .models import Departamento, Queja


class VistaListaQuejas(LoginRequiredMixin, ListView):
    model = Queja
    template_name = 'quejas/queja_lista.html'
    context_object_name = 'quejas'
    paginate_by = 10

    def get_queryset(self):
        # Todos los usuarios autenticados ven todas las quejas
        # Staff y usuarios regulares ven el mismo listado
        # La anonimidad se protege en el template (no mostrando el nombre del autor)
        consulta = Queja.objects.select_related('autor', 'departamento').all()

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

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        self._enviar_notificacion()
        messages.success(self.request, 'Estado actualizado correctamente.')
        return respuesta

    def _enviar_notificacion(self):
        queja = self.object
        if queja.anonima or not queja.autor or not queja.autor.email:
            return
        url_detalle = self.request.build_absolute_uri(queja.get_absolute_url())
        cuerpo = render_to_string('quejas/emails/cambio_estado.txt', {
            'queja': queja,
            'url_detalle': url_detalle,
        })
        send_mail(
            subject=f'Tu queja ha sido actualizada: {queja.get_estado_display()}',
            message=cuerpo,
            from_email=None,
            recipient_list=[queja.autor.email],
            fail_silently=True,
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class VistaEstadisticas(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'quejas/estadisticas.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        total = Queja.objects.count()
        contexto['total'] = total

        # Quejas por estado
        por_estado = {valor: 0 for valor, _ in OPCIONES_ESTADO}
        for item in Queja.objects.values('estado').annotate(total=Count('id')):
            por_estado[item['estado']] = item['total']
        contexto['por_estado'] = [
            {'etiqueta': etiqueta, 'valor': valor, 'total': por_estado[valor], 'color': COLOR_ESTADO[valor]}
            for valor, etiqueta in OPCIONES_ESTADO
        ]

        # Quejas por departamento
        contexto['por_departamento'] = (
            Departamento.objects
            .annotate(total=Count('quejas'))
            .order_by('-total')
        )

        # Quejas por tipo
        contexto['por_tipo'] = {
            etiqueta: Queja.objects.filter(tipo=valor).count()
            for valor, etiqueta in OPCIONES_TIPO
        }

        # Top 5 más votadas
        contexto['mas_votadas'] = (
            Queja.objects
            .annotate(num_votos=Count('votos'))
            .order_by('-num_votos')[:5]
        )

        return contexto
