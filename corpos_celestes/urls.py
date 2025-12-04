from django.urls import path
from . import views

urlpatterns = [
    # vizualizar página geral
    path("corposcelestes/",views.visualizarCorposCelestes,name='visualizarCorposCelestes'),
    # estrelas
    path('estrelas/', views.listar_estrelas, name='listar_estrelas'),
    path('estrelas/criar/', views.criar_estrela, name='criar_estrela'),
    path('estrelas/editar/<int:id>/', views.editar_estrela, name='editar_estrela'),
    path('estrelas/deletar/<int:id>/', views.deletar_estrela, name='deletar_estrela'),
    path('estrelas/detalhes/<int:id>/', views.detalhes_estrela, name='detalhes_estrela'),  

    
    # Planetas
    path('planetas/', views.listar_planetas, name='listar_planetas'),
    path('planetas/criar/', views.criar_planeta, name='criar_planeta'),
    path('planetas/editar/<int:id>/', views.editar_planeta, name='editar_planeta'),
    path('planetas/deletar/<int:id>/', views.deletar_planeta, name='deletar_planeta'),
    path('planetas/<int:id>/', views.detalhes_planeta, name='detalhes_planeta'),


    # Satélites
    path('satelites/', views.listar_satelites, name='listar_satelites'),
    path('satelites/criar/', views.criar_satelite, name='criar_satelite'),
    path('satelites/editar/<int:id>/', views.editar_satelite, name='editar_satelite'),
    path('satelites/deletar/<int:id>/', views.deletar_satelite, name='deletar_satelite'),
    path('satelites/<int:id>/', views.detalhes_satelite, name='detalhes_satelite'),

]