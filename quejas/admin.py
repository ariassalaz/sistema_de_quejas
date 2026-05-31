from django.contrib import admin

from .models import Departamento, Queja
from .constantes import ESTADO_EN_REVISION, ESTADO_RESUELTA, ESTADO_RECHAZADA


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'responsable', 'total_quejas')
    list_filter = ('responsable',)
    search_fields = ('nombre', 'descripcion')

    @admin.display(description='Total de quejas')
    def total_quejas(self, obj):
        return obj.quejas.count()


@admin.register(Queja)
class QuejaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'estado', 'departamento', 'autor', 'anonima', 'total_votos', 'fecha_creacion')
    list_filter = ('tipo', 'estado', 'departamento', 'anonima')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'total_votos')
    date_hierarchy = 'fecha_creacion'
    actions = ['marcar_en_revision', 'marcar_resuelta', 'marcar_rechazada']

    @admin.action(description='Marcar como "En revisión"')
    def marcar_en_revision(self, _request, queryset):
        queryset.update(estado=ESTADO_EN_REVISION)

    @admin.action(description='Marcar como "Resuelta"')
    def marcar_resuelta(self, _request, queryset):
        queryset.update(estado=ESTADO_RESUELTA)

    @admin.action(description='Marcar como "Rechazada"')
    def marcar_rechazada(self, _request, queryset):
        queryset.update(estado=ESTADO_RECHAZADA)
