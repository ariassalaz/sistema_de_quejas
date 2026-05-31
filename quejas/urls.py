from django.urls import path

from . import views, vistas_api

urlpatterns = [
    # Vistas web
    path('', views.VistaListaQuejas.as_view(), name='queja-lista'),
    path('nueva/', views.VistaCrearQueja.as_view(), name='queja-crear'),
    path('estadisticas/', views.VistaEstadisticas.as_view(), name='queja-estadisticas'),
    path('<int:pk>/', views.VistaDetalleQueja.as_view(), name='queja-detalle'),
    path('<int:pk>/editar/', views.VistaEditarQueja.as_view(), name='queja-editar'),
    path('<int:pk>/eliminar/', views.VistaEliminarQueja.as_view(), name='queja-eliminar'),
    path('<int:pk>/votar/', views.VistaVotarQueja.as_view(), name='queja-votar'),
    path('<int:pk>/estado/', views.VistaCambiarEstado.as_view(), name='queja-cambiar-estado'),

    # API REST
    path('api/quejas/', vistas_api.ApiListaQuejas.as_view(), name='api-quejas'),
    path('api/quejas/<int:pk>/', vistas_api.ApiDetalleQueja.as_view(), name='api-queja-detalle'),
    path('api/departamentos/', vistas_api.ApiListaDepartamentos.as_view(), name='api-departamentos'),
    path('api/estadisticas/', vistas_api.ApiEstadisticas.as_view(), name='api-estadisticas'),
]
