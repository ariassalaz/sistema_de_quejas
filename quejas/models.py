from django.db import models
from django.urls import reverse

from .constantes import OPCIONES_TIPO, OPCIONES_ESTADO, ESTADO_PENDIENTE, TIPO_QUEJA


class Departamento(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=100, unique=True)
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    responsable = models.ForeignKey(
        'accounts.CustomUser',
        verbose_name='Responsable',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departamentos_a_cargo',
    )

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('departamento-detalle', kwargs={'pk': self.pk})


class Queja(models.Model):
    titulo = models.CharField(verbose_name='Título', max_length=200)
    descripcion = models.TextField(verbose_name='Descripción')
    tipo = models.CharField(
        verbose_name='Tipo',
        max_length=20,
        choices=OPCIONES_TIPO,
        default=TIPO_QUEJA,
    )
    estado = models.CharField(
        verbose_name='Estado',
        max_length=20,
        choices=OPCIONES_ESTADO,
        default=ESTADO_PENDIENTE,
    )
    anonima = models.BooleanField(verbose_name='Anónima', default=False)
    autor = models.ForeignKey(
        'accounts.CustomUser',
        verbose_name='Autor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quejas_creadas',
    )
    departamento = models.ForeignKey(
        Departamento,
        verbose_name='Departamento',
        on_delete=models.PROTECT,
        related_name='quejas',
    )
    fecha_creacion = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(verbose_name='Última actualización', auto_now=True)
    imagen = models.ImageField(
        verbose_name='Imagen',
        upload_to='quejas/',
        blank=True,
        null=True,
    )
    votos = models.ManyToManyField(
        'accounts.CustomUser',
        verbose_name='Votos',
        blank=True,
        related_name='quejas_votadas',
    )

    class Meta:
        verbose_name = 'Queja'
        verbose_name_plural = 'Quejas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.titulo}'

    def get_absolute_url(self):
        return reverse('queja-detalle', kwargs={'pk': self.pk})

    @property
    def total_votos(self):
        return self.votos.count()
