from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(
        verbose_name='Biografía',
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    departamento_asignado = models.ForeignKey(
        'quejas.Departamento',
        verbose_name='Departamento asignado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personal',
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name() or self.username
