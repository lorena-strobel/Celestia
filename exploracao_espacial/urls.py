from django.urls import path
from . import views

urlpatterns = [
    # Página inicial da exploração espacial
    path("", views.visualizarExploracao, name="visualizarExploracao"),
    
    # Missões
    path("missoes/", views.listar_missoes, name="listar_missoes"),
    path("missoes/criar/", views.criar_missao, name="criar_missao"),
    path("missoes/<int:pk>/", views.detalhes_missao, name="detalhes_missao"),
    path("missoes/<int:pk>/editar/", views.editar_missao, name="editar_missao"),
    path("missoes/<int:pk>/excluir/", views.excluir_missao, name="excluir_missao"),

    # Astronautas 
    path("astronautas/", views.listar_astronautas, name="listar_astronautas"),
    path("astronautas/criar/", views.criar_astronauta, name="criar_astronauta"),
    path("astronautas/<int:pk>/", views.detalhes_astronauta, name="detalhes_astronauta"),
    path("astronautas/<int:pk>/editar/", views.editar_astronauta, name="editar_astronauta"),
    path("astronautas/<int:pk>/excluir/", views.excluir_astronauta, name="excluir_astronauta"),
]