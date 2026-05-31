from django.urls import path
from django.contrib.auth import views as vistas_auth
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path('registro/', views.VistaRegistro.as_view(), name='registro'),

    path('entrar/', vistas_auth.LoginView.as_view(
        template_name='accounts/login.html',
    ), name='iniciar-sesion'),

    path('salir/', vistas_auth.LogoutView.as_view(), name='cerrar-sesion'),

    path('perfil/', views.VistaPerfil.as_view(), name='perfil'),
    path('perfil/editar/', views.VistaEditarPerfil.as_view(), name='editar-perfil'),

    path('contrasena/cambiar/', vistas_auth.PasswordChangeView.as_view(
        template_name='accounts/cambiar_contrasena.html',
        success_url=reverse_lazy('contrasena-cambiada'),
    ), name='cambiar-contrasena'),

    path('contrasena/cambiada/', vistas_auth.PasswordChangeDoneView.as_view(
        template_name='accounts/contrasena_cambiada.html',
    ), name='contrasena-cambiada'),

    path('contrasena/restablecer/', vistas_auth.PasswordResetView.as_view(
        template_name='accounts/restablecer_contrasena.html',
        email_template_name='accounts/emails/correo_restablecer.html',
        subject_template_name='accounts/emails/asunto_restablecer.txt',
        success_url=reverse_lazy('restablecer-enviado'),
    ), name='restablecer-contrasena'),

    path('contrasena/restablecer/enviado/', vistas_auth.PasswordResetDoneView.as_view(
        template_name='accounts/restablecer_enviado.html',
    ), name='restablecer-enviado'),

    path('contrasena/restablecer/<uidb64>/<token>/', vistas_auth.PasswordResetConfirmView.as_view(
        template_name='accounts/confirmar_restablecer.html',
        success_url=reverse_lazy('restablecer-completo'),
    ), name='confirmar-restablecer'),

    path('contrasena/restablecer/completo/', vistas_auth.PasswordResetCompleteView.as_view(
        template_name='accounts/restablecer_completo.html',
    ), name='restablecer-completo'),
]
