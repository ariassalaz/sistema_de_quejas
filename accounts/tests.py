from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class PruebasRegistro(TestCase):

    def setUp(self):
        self.cliente = Client()

    def test_registro_usuario_nuevo(self):
        """Un usuario nuevo puede registrarse correctamente."""
        datos = {
            'username': 'nuevo_alumno',
            'email': 'nuevo@itlalaguna.edu.mx',
            'password1': 'TestPass456!',
            'password2': 'TestPass456!',
        }
        respuesta = self.cliente.post(reverse('registro'), datos)
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Usuario.objects.filter(username='nuevo_alumno').exists())

    def test_registro_redirige_si_autenticado(self):
        """Un usuario ya autenticado es redirigido al inicio si intenta registrarse."""
        Usuario.objects.create_user(username='existente', password='TestPass123!')
        self.cliente.login(username='existente', password='TestPass123!')
        respuesta = self.cliente.get(reverse('registro'))
        self.assertRedirects(respuesta, reverse('inicio'))


class PruebasLogin(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.usuario = Usuario.objects.create_user(
            username='alumno_login',
            email='alumno@itlalaguna.edu.mx',
            password='TestPass123!',
        )

    def test_login_correcto_redirige(self):
        """Login con credenciales correctas redirige al inicio."""
        respuesta = self.cliente.post(reverse('iniciar-sesion'), {
            'username': 'alumno_login',
            'password': 'TestPass123!',
        })
        self.assertRedirects(respuesta, reverse('inicio'))

    def test_login_incorrecto_permanece_en_login(self):
        """Login con contraseña incorrecta no autentica al usuario."""
        respuesta = self.cliente.post(reverse('iniciar-sesion'), {
            'username': 'alumno_login',
            'password': 'contrasena_incorrecta',
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)

    def test_perfil_requiere_autenticacion(self):
        """La vista de perfil redirige al login si no hay sesión activa."""
        respuesta = self.cliente.get(reverse('perfil'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn(reverse('iniciar-sesion'), respuesta['Location'])

    def test_perfil_accesible_autenticado(self):
        """Un usuario autenticado puede acceder a su perfil."""
        self.cliente.login(username='alumno_login', password='TestPass123!')
        respuesta = self.cliente.get(reverse('perfil'))
        self.assertEqual(respuesta.status_code, 200)
