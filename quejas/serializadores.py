from rest_framework import serializers

from .models import Departamento, Queja


class SerializadorDepartamento(serializers.ModelSerializer):
    total_quejas = serializers.SerializerMethodField()

    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'total_quejas']

    def get_total_quejas(self, obj):
        return obj.quejas.count()


class SerializadorQueja(serializers.ModelSerializer):
    autor_nombre = serializers.SerializerMethodField()
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    total_votos = serializers.IntegerField(read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Queja
        fields = [
            'id', 'titulo', 'descripcion', 'tipo', 'tipo_display',
            'estado', 'estado_display', 'anonima', 'autor_nombre',
            'departamento', 'departamento_nombre', 'total_votos',
            'fecha_creacion', 'fecha_actualizacion',
        ]
        read_only_fields = ['estado', 'fecha_creacion', 'fecha_actualizacion']

    def get_autor_nombre(self, obj):
        if obj.anonima or not obj.autor:
            return 'Anónimo'
        return obj.autor.get_full_name() or obj.autor.username
