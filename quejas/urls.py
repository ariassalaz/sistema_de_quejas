from django.urls import path

from . import views

urlpatterns = [
    path('', views.VistaListaQuejas.as_view(), name='queja-lista'),
    path('nueva/', views.VistaCrearQueja.as_view(), name='queja-crear'),
    path('<int:pk>/', views.VistaDetalleQueja.as_view(), name='queja-detalle'),
    path('<int:pk>/editar/', views.VistaEditarQueja.as_view(), name='queja-editar'),
    path('<int:pk>/eliminar/', views.VistaEliminarQueja.as_view(), name='queja-eliminar'),
    path('<int:pk>/votar/', views.VistaVotarQueja.as_view(), name='queja-votar'),
    path('<int:pk>/estado/', views.VistaCambiarEstado.as_view(), name='queja-cambiar-estado'),
]
