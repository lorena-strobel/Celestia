from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Sum
from .models import Galaxia, Nebulosa, SistemaPlanetario
from .forms import GalaxiaForm, NebulosaForm, SistemaPlanetarioForm

def admin_required(view_func):
    return user_passes_test(lambda user: user.is_superuser)(view_func)

def visualizarUniverso(request):
    return render(request, "universo/index.html")

def listar_galaxias(request):
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    tipo = request.GET.get("tipo", "")
    diametro_min = request.GET.get("diametro_min", "")
    distancia_max = request.GET.get("distancia_max", "")
    galaxias_qs = Galaxia.objects.all()

    # Busca multi-campo
    if busca:
        galaxias_qs = galaxias_qs.filter(
            Q(nome__icontains=busca) |
            Q(tipo__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    # Filtros
    if tipo:
        galaxias_qs = galaxias_qs.filter(tipo=tipo)

    if diametro_min:
        try:
            galaxias_qs = galaxias_qs.filter(diametro__gte=float(diametro_min))
        except (ValueError, TypeError):
            pass
    
    if distancia_max:
        try:
            galaxias_qs = galaxias_qs.filter(distancia_terra__lte=float(distancia_max))
        except (ValueError, TypeError):
            pass

    # Ordenação
    campos_ordenacao = ["nome", "tipo", "diametro", "massa", "distancia_terra"]
    if ordenar in campos_ordenacao:
        galaxias_qs = galaxias_qs.order_by(ordenar)
    else:
        galaxias_qs = galaxias_qs.order_by("nome")

    # Paginação
    paginator = Paginator(galaxias_qs, 8)
    pagina = request.GET.get("pagina")
    galaxias_paginadas = paginator.get_page(pagina)

    context = {
        "galaxias": galaxias_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "tipo": tipo,
        },
        "tipos_galaxia": Galaxia.TIPO_CHOICES,
    }

    return render(request, "universo/galaxias/listar_galaxias.html", context)

def detalhes_galaxia(request, pk):
    galaxia = get_object_or_404(Galaxia, pk=pk)
    sistemas = galaxia.sistemas_planetarios.all()
    total_planetas = sistemas.aggregate(
        total=Sum('numero_planetas')
    )['total'] or 0

    return render(request, "universo/galaxias/detalhes_galaxia.html", {
        "galaxia": galaxia,
        "sistemas": sistemas,
        "total_planetas": total_planetas
    })

@admin_required
def criar_galaxia(request):
    if request.method == "POST":
        form = GalaxiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_galaxias")
    else:
        form = GalaxiaForm()
    return render(request, "universo/galaxias/form_galaxias.html", {
        "form": form, 
        "titulo": "Criar Galáxia",
        "url_voltar": "listar_galaxias"
    })

@admin_required
def editar_galaxia(request, pk):
    galaxia = get_object_or_404(Galaxia, pk=pk)
    if request.method == "POST":
        form = GalaxiaForm(request.POST, request.FILES, instance=galaxia)
        if form.is_valid():
            form.save()
            return redirect("detalhes_galaxia", pk=pk)
    else:
        form = GalaxiaForm(instance=galaxia)
    return render(request, "universo/galaxias/form_galaxias.html", {
        "form": form, 
        "titulo": "Editar Galáxia",
        "url_voltar": "detalhes_galaxia"
    })

@admin_required
def excluir_galaxia(request, pk):  
    galaxia = get_object_or_404(Galaxia, pk=pk)
    
    if request.method == "POST":
        # Verifica se tem sistemas vinculados
        if galaxia.sistemas_planetarios.exists():
            messages.error(
                request, 
                f'Não é possível excluir a galáxia "{galaxia.nome}" '
                f'porque ela possui sistemas planetários vinculados. '
                f'Delete ou mova os sistemas primeiro.'
            )
            return redirect("detalhes_galaxia", pk=pk)
        
        galaxia.delete()
        messages.success(
            request, 
            f'Galáxia "{galaxia.nome}" excluída com sucesso!'
        )
        return redirect("listar_galaxias")

    # Se alguém tentar acessar via GET direto pela URL
    messages.error(request, "Acesso inválido.")
    return redirect("listar_galaxias")



def listar_sistemas(request):
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    galaxia = request.GET.get("galaxia", "")
    planetas_min = request.GET.get("planetas_min", "")
    idade_max = request.GET.get("idade_max", "")
    sistemas_qs = SistemaPlanetario.objects.select_related('galaxia').all()

    # Busca multi-campo
    if busca:
        sistemas_qs = sistemas_qs.filter(
            Q(nome__icontains=busca) |
            Q(estrela_principal__icontains=busca) |
            Q(galaxia__nome__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    # Filtros
    if galaxia and galaxia.isdigit():
        sistemas_qs = sistemas_qs.filter(galaxia_id=galaxia)

    if planetas_min:
        try:
            sistemas_qs = sistemas_qs.filter(numero_planetas__gte=int(planetas_min))
        except (ValueError, TypeError):
            pass
    
    if idade_max:
        try:
            sistemas_qs = sistemas_qs.filter(idade__lte=float(idade_max))
        except (ValueError, TypeError):
            pass
    
    # Ordenação
    campos_ordenacao = ["nome", "estrela_principal", "idade", "numero_planetas"]
    if ordenar in campos_ordenacao:
        sistemas_qs = sistemas_qs.order_by(ordenar)
    else:
        sistemas_qs = sistemas_qs.order_by("nome")

    total_planetas_sistemas = 0
    for sistema in sistemas_qs:
        if sistema.numero_planetas:
            total_planetas_sistemas += sistema.numero_planetas

    # Paginação
    paginator = Paginator(sistemas_qs, 8)
    pagina = request.GET.get("pagina")
    sistemas_paginadas = paginator.get_page(pagina)

    # galáxias com sistemas únicos
    galaxias_com_sistemas = Galaxia.objects.filter(
        sistemas_planetarios__in=sistemas_qs
    ).distinct().count()

    context = {
        "sistemas": sistemas_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "galaxia": galaxia,
        },
        "galaxias": Galaxia.objects.all(),
        "total_planetas_sistemas": total_planetas_sistemas,
        "galaxias_com_sistemas": galaxias_com_sistemas,
    }

    return render(request, "universo/sistemas/listar_sistemas.html", context)

def detalhes_sistema(request, pk):
    sistema = get_object_or_404(SistemaPlanetario, pk=pk)
    return render(request, "universo/sistemas/detalhes_sistemas.html", {"sistema": sistema})

@admin_required
def criar_sistema(request):
    if request.method == "POST":
        form = SistemaPlanetarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_sistemas")
    else:
        form = SistemaPlanetarioForm()
    return render(request, "universo/sistemas/form_sistemas.html", {
        "form": form, 
        "titulo": "Criar Sistema Planetário",
        "url_voltar": "listar_sistemas"
    })

@admin_required
def editar_sistema(request, pk):
    sistema = get_object_or_404(SistemaPlanetario, pk=pk)
    if request.method == "POST":
        form = SistemaPlanetarioForm(request.POST, request.FILES, instance=sistema)
        if form.is_valid():
            form.save()
            return redirect("detalhes_sistema", pk=pk)
    else:
        form = SistemaPlanetarioForm(instance=sistema)
    return render(request, "universo/sistemas/form_sistemas.html", {
        "form": form, 
        "titulo": "Editar Sistema Planetário",
        "url_voltar": "detalhes_sistema"
    })

@admin_required
def excluir_sistema(request, pk):
    sistema = get_object_or_404(SistemaPlanetario, pk=pk)

    if request.method == "POST":
        sistema.delete()
        messages.success(
            request,
            f'Sistema "{sistema.nome}" excluído com sucesso!'
        )
        return redirect("listar_sistemas")

    messages.error(request, "Acesso inválido.")
    return redirect("listar_sistemas")

def listar_nebulosas(request):
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    tipo = request.GET.get("tipo", "")
    distancia_max = request.GET.get("distancia_max", "")
    magnitude_max = request.GET.get("magnitude_max", "")
    nebulosas_qs = Nebulosa.objects.all()

    # Busca multi-campo
    if busca:
        nebulosas_qs = nebulosas_qs.filter(
            Q(nome__icontains=busca) |
            Q(tipo__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    # Filtros
    if tipo:
        nebulosas_qs = nebulosas_qs.filter(tipo=tipo)

    if distancia_max and distancia_max.isdigit():
        nebulosas_qs = nebulosas_qs.filter(distancia__lte=float(distancia_max))
    
    if magnitude_max:
        try:
            nebulosas_qs = nebulosas_qs.filter(magnitude__lte=float(magnitude_max))
        except ValueError:
            pass
    
    # Ordenação
    campos_ordenacao = ["nome", "tipo", "distancia", "diametro", "magnitude"]
    if ordenar in campos_ordenacao:
        nebulosas_qs = nebulosas_qs.order_by(ordenar)
    else:
        nebulosas_qs = nebulosas_qs.order_by("nome")

    # Paginação
    paginator = Paginator(nebulosas_qs, 8)
    pagina = request.GET.get("pagina")
    nebulosas_paginadas = paginator.get_page(pagina)

    context = {
        "nebulosas": nebulosas_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "tipo": tipo,
        },
        "tipos_nebulosa": Nebulosa.TIPO_CHOICES,
        "request": request, 
    }

    return render(request, "universo/nebulosas/listar_nebulosas.html", context)


def detalhes_nebulosa(request, pk):
    nebulosa = get_object_or_404(Nebulosa, pk=pk)
    return render(request, "universo/nebulosas/detalhes_nebulosas.html", {"nebulosa": nebulosa})

@admin_required
def criar_nebulosa(request):
    if request.method == "POST":
        form = NebulosaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_nebulosas")
    else:
        form = NebulosaForm()
    return render(request, "universo/nebulosas/form_nebulosas.html", {
        "form": form, 
        "titulo": "Criar Nebulosa",
        "url_voltar": "listar_nebulosas"
    })

@admin_required
def editar_nebulosa(request, pk):
    nebulosa = get_object_or_404(Nebulosa, pk=pk)
    if request.method == "POST":
        form = NebulosaForm(request.POST, request.FILES, instance=nebulosa)
        if form.is_valid():
            form.save()
            return redirect("detalhes_nebulosa", pk=pk)
    else:
        form = NebulosaForm(instance=nebulosa)
    return render(request, "universo/nebulosas/form_nebulosas.html", {
        "form": form, 
        "titulo": "Editar Nebulosa",
        "url_voltar": "detalhes_nebulosa",
        "nebulosa": nebulosa
    })

@admin_required
def excluir_nebulosa(request, pk):
    nebulosa = get_object_or_404(Nebulosa, pk=pk)

    if request.method == "POST":
        nebulosa.delete()
        messages.success(
            request, 
            f'Nebulosa "{nebulosa.nome}" excluída com sucesso!'
        )
        return redirect("listar_nebulosas")

    messages.error(request, "Acesso inválido.")
    return redirect("listar_nebulosas")