from django.db import models


class Departamento(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=100, unique=True)
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
