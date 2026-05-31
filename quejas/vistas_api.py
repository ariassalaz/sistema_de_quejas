from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Departamento, Queja
from .serializadores import SerializadorDepartamento, SerializadorQueja


class ApiListaDepartamentos(generics.ListAPIView):
    queryset = Departamento.objects.all()
    serializer_class = SerializadorDepartamento
    permission_classes = [permissions.IsAuthenticated]


class ApiListaQuejas(generics.ListCreateAPIView):
    serializer_class = SerializadorQueja
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        consulta = Queja.objects.select_related('autor', 'departamento').all()
        departamento = self.request.query_params.get('departamento')
        estado = self.request.query_params.get('estado')
        if departamento:
            consulta = consulta.filter(departamento__pk=departamento)
        if estado:
            consulta = consulta.filter(estado=estado)
        return consulta

    def perform_create(self, serializer):
        anonima = serializer.validated_data.get('anonima', False)
        autor = None if anonima else self.request.user
        serializer.save(autor=autor)


class ApiDetalleQueja(generics.RetrieveAPIView):
    queryset = Queja.objects.select_related('autor', 'departamento').all()
    serializer_class = SerializadorQueja
    permission_classes = [permissions.IsAuthenticated]


class ApiEstadisticas(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from django.db.models import Count
        datos = {
            'total_quejas': Queja.objects.count(),
            'por_estado': list(
                Queja.objects.values('estado').annotate(total=Count('id'))
            ),
            'por_departamento': list(
                Departamento.objects.annotate(total=Count('quejas'))
                .values('nombre', 'total')
                .order_by('-total')
            ),
            'mas_votadas': list(
                Queja.objects.annotate(votos_count=Count('votos'))
                .order_by('-votos_count')
                .values('id', 'titulo', 'votos_count')[:5]
            ),
        }
        return Response(datos)
