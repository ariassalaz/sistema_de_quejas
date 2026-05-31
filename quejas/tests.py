from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Departamento, Queja
from .constantes import TIPO_QUEJA, TIPO_SUGERENCIA, ESTADO_PENDIENTE

Usuario = get_user_model()


class PruebasModeloDepartamento(TestCase):

    def setUp(self):
        self.departamento = Departamento.objects.create(
            nombre='Sistemas',
            descripcion='Departamento de prueba',
        )

    def test_departamento_str(self):
        """__str__ devuelve el nombre del departamento."""
        self.assertEqual(str(self.departamento), 'Sistemas')

    def test_departamento_ordenado_por_nombre(self):
        """Los departamentos se ordenan alfabéticamente."""
        Departamento.objects.create(nombre='Mecánica')
        primero = Departamento.objects.first()
        self.assertEqual(primero.nombre, 'Mecánica')


class PruebasModeloQueja(TestCase):

    def setUp(self):
        self.departamento = Departamento.objects.create(nombre='Industrial')
        self.usuario = Usuario.objects.create_user(
            username='alumno',
            password='TestPass123!',
        )
        self.queja = Queja.objects.create(
            titulo='Falla en proyector',
            descripcion='El proyector del salón 3A no funciona.',
            tipo=TIPO_QUEJA,
            departamento=self.departamento,
            autor=self.usuario,
        )

    def test_queja_str(self):
        """__str__ incluye el tipo y el título."""
        self.assertIn('Falla en proyector', str(self.queja))
        self.assertIn('Queja', str(self.queja))

    def test_queja_estado_inicial_pendiente(self):
        """El estado por defecto al crear una queja es 'pendiente'."""
        self.assertEqual(self.queja.estado, ESTADO_PENDIENTE)

    def test_total_votos_inicial_cero(self):
        """Una queja recién creada tiene 0 votos."""
        self.assertEqual(self.queja.total_votos, 0)

    def test_queja_anonima_no_tiene_autor(self):
        """Al enviar una queja marcada como anónima, autor queda en None."""
        cliente = Client()
        cliente.login(username='alumno', password='TestPass123!')
        datos = {
            'titulo': 'Queja anónima de prueba',
            'descripcion': 'Descripción de queja anónima',
            'tipo': TIPO_QUEJA,
            'departamento': self.departamento.pk,
            'anonima': True,
        }
        cliente.post(reverse('queja-crear'), datos)
        queja_anonima = Queja.objects.get(titulo='Queja anónima de prueba')
        self.assertIsNone(queja_anonima.autor)

    def test_queja_no_anonima_guarda_autor(self):
        """Al enviar una queja NO anónima, se guarda el autor correctamente."""
        cliente = Client()
        cliente.login(username='alumno', password='TestPass123!')
        datos = {
            'titulo': 'Queja con autor',
            'descripcion': 'Descripción',
            'tipo': TIPO_SUGERENCIA,
            'departamento': self.departamento.pk,
            'anonima': False,
        }
        cliente.post(reverse('queja-crear'), datos)
        queja = Queja.objects.get(titulo='Queja con autor')
        self.assertEqual(queja.autor, self.usuario)


class PruebasVistasQuejas(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.departamento = Departamento.objects.create(nombre='Química')
        self.autor = Usuario.objects.create_user(
            username='autor_test',
            password='TestPass123!',
        )
        self.otro_usuario = Usuario.objects.create_user(
            username='intruso_test',
            password='TestPass123!',
        )
        self.queja = Queja.objects.create(
            titulo='Queja de prueba en vista',
            descripcion='Descripción completa de prueba',
            tipo=TIPO_QUEJA,
            departamento=self.departamento,
            autor=self.autor,
        )

    def test_queja_list_requires_login(self):
        """Sin autenticación, la lista redirige al login."""
        respuesta = self.cliente.get(reverse('queja-lista'))
        url_login = reverse('iniciar-sesion')
        self.assertRedirects(respuesta, f'{url_login}?next={reverse("queja-lista")}')

    def test_crear_queja_autenticado(self):
        """Un usuario autenticado puede crear una queja mediante POST."""
        self.cliente.login(username='autor_test', password='TestPass123!')
        datos = {
            'titulo': 'Queja nueva desde test',
            'descripcion': 'Descripción desde test',
            'tipo': TIPO_QUEJA,
            'departamento': self.departamento.pk,
            'anonima': False,
        }
        respuesta = self.cliente.post(reverse('queja-crear'), datos)
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Queja.objects.filter(titulo='Queja nueva desde test').exists())

    def test_votar_queja(self):
        """Un usuario puede votar y desvotar una queja."""
        self.cliente.login(username='autor_test', password='TestPass123!')
        url_votar = reverse('queja-votar', kwargs={'pk': self.queja.pk})

        self.cliente.post(url_votar)
        self.queja.refresh_from_db()
        self.assertEqual(self.queja.total_votos, 1)

        self.cliente.post(url_votar)
        self.queja.refresh_from_db()
        self.assertEqual(self.queja.total_votos, 0)

    def test_solo_autor_puede_editar(self):
        """Un usuario que no es autor recibe 403 al intentar editar."""
        self.cliente.login(username='intruso_test', password='TestPass123!')
        respuesta = self.cliente.get(
            reverse('queja-editar', kwargs={'pk': self.queja.pk})
        )
        self.assertEqual(respuesta.status_code, 403)

    def test_solo_autor_puede_eliminar(self):
        """Un usuario que no es autor recibe 403 al intentar eliminar."""
        self.cliente.login(username='intruso_test', password='TestPass123!')
        respuesta = self.cliente.post(
            reverse('queja-eliminar', kwargs={'pk': self.queja.pk})
        )
        self.assertEqual(respuesta.status_code, 403)
