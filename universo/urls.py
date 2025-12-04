from django.urls import path
from universo import views

urlpatterns = [
    path("universo/",views.visualizarUniverso,name="visualizarUniverso"),
    path("galaxias/", views.listar_galaxias, name="listar_galaxias"),
    path("galaxias/<int:pk>/", views.detalhes_galaxia, name="detalhes_galaxia"),
    path("galaxias/criar/", views.criar_galaxia, name="criar_galaxia"),
    path("galaxias/<int:pk>/editar/", views.editar_galaxia, name="editar_galaxia"),
    path("galaxias/<int:pk>/excluir/", views.excluir_galaxia, name="excluir_galaxia"),

    path("sistemas/", views.listar_sistemas, name="listar_sistemas"),
    path("sistemas/<int:pk>/", views.detalhes_sistema, name="detalhes_sistema"),
    path("sistemas/criar/", views.criar_sistema, name="criar_sistema"),
    path("sistemas/<int:pk>/editar/", views.editar_sistema, name="editar_sistema"),
    path("sistemas/<int:pk>/excluir/", views.excluir_sistema, name="excluir_sistema"),

        # Nebulosas
    path("nebulosas/", views.listar_nebulosas, name="listar_nebulosas"),
    path("nebulosas/<int:pk>/", views.detalhes_nebulosa, name="detalhes_nebulosa"),
    path("nebulosas/criar/", views.criar_nebulosa, name="criar_nebulosa"),
    path("nebulosas/<int:pk>/editar/", views.editar_nebulosa, name="editar_nebulosa"),
    path("nebulosas/<int:pk>/excluir/", views.excluir_nebulosa, name="excluir_nebulosa"),

    ]
