from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from universo.models import SistemaPlanetario
from .models import Estrela, Planeta, SateliteNatural
from .forms import EstrelaForm, PlanetaForm, SateliteNaturalForm

def admin_required(view_func):
    return user_passes_test(lambda user: user.is_superuser)(view_func)

def visualizarCorposCelestes(request):
    return render(request, "corpos_celestes/index.html")

# ESTRELAS
def listar_estrelas(request):
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    classificacao = request.GET.get("classificacao", "")  
    estagio = request.GET.get("estagio", "")             
    sistema = request.GET.get("sistema", "")             

    estrelas_filtradas = Estrela.objects.select_related('sistema_planetario').all()

    if busca:
        estrelas_filtradas = estrelas_filtradas.filter(
            Q(nome__icontains=busca) |
            Q(sistema_planetario__nome__icontains=busca) |
            Q(classificacao_espectral__icontains=busca) |
            Q(estagio_evolutivo__icontains=busca)
        )

    if classificacao:
        estrelas_filtradas = estrelas_filtradas.filter(classificacao_espectral=classificacao)

    if estagio:
        estrelas_filtradas = estrelas_filtradas.filter(estagio_evolutivo=estagio)

    if sistema:
        estrelas_filtradas = estrelas_filtradas.filter(sistema_planetario_id=sistema)

    campos_ordenacao = ["nome", "classificacao_espectral", "estagio_evolutivo", "massa", "temperatura"]
    
    if ordenar in campos_ordenacao:
        estrelas_filtradas = estrelas_filtradas.order_by(ordenar)
    else:
        estrelas_filtradas = estrelas_filtradas.order_by("nome")

    # contagem total de estrelas 
    total_estrelas = Estrela.objects.count()

    # contagem com filtros aplicados
    estrelas_filtradas_count = estrelas_filtradas.count()

    paginator = Paginator(estrelas_filtradas, 8)
    pagina = request.GET.get("pagina")
    estrelas_paginadas = paginator.get_page(pagina)

    context = {
        "estrelas": estrelas_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "classificacao": classificacao,
            "estagio": estagio,
            "sistema": sistema,
        },
        "sistemas": SistemaPlanetario.objects.all(),
        "espectrais": Estrela.ESPECTRAL_CHOICES,
        "estagios": Estrela.EVOLUCAO_CHOICES,
        "total_estrelas": total_estrelas, 
        "estrelas_filtradas_count": estrelas_filtradas_count, 
    }

    return render(request, "corpos_celestes/estrelas/listar_estrelas.html", context)

def detalhes_estrela(request, id):
    estrela = get_object_or_404(Estrela, id=id)
    context = {
        'estrela': estrela,
    }
    return render(request, "corpos_celestes/estrelas/detalhes_estrelas.html", context)

@admin_required
def criar_estrela(request):
    if request.method == "POST":
        form = EstrelaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_estrelas")
    else:
        form = EstrelaForm()
    return render(request, "corpos_celestes/estrelas/form_estrelas.html", {"form": form, "titulo": "Criar Estrela"})

@admin_required
def editar_estrela(request, id):
    estrela = get_object_or_404(Estrela, id=id)

    if request.method == "POST":
        form = EstrelaForm(request.POST, request.FILES, instance=estrela)
        if form.is_valid():
            form.save()
            return redirect("listar_estrelas")
    else:
        form = EstrelaForm(instance=estrela)

    return render(request, "corpos_celestes/estrelas/form_estrelas.html", {"form": form, "titulo": "Editar Estrela"})

@admin_required
def deletar_estrela(request, id):
    estrela = get_object_or_404(Estrela, id=id)

    if request.method == "POST":
        nome = estrela.nome
        estrela.delete()
        messages.success(request, f'Estrela "{nome}" excluída com sucesso!')
        return redirect("listar_estrelas")

    messages.error(request, "Ação inválida.")
    return redirect("listar_estrelas")

# Planetas
def listar_planetas(request):
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    tipo = request.GET.get("tipo", "")
    sistema = request.GET.get("sistema", "")
    agua = request.GET.get("agua", "")
    atmosfera = request.GET.get("atmosfera", "")

    planetas_filtrados = Planeta.objects.select_related('sistema_planetario').all()

    # Excluir planetas sem ID
    planetas_filtrados = planetas_filtrados.exclude(id__isnull=True)
    # Excluir planetas com nome vazio
    planetas_filtrados = planetas_filtrados.exclude(nome="")
    # Excluir planetas com nome None
    planetas_filtrados = planetas_filtrados.exclude(nome__isnull=True)
    
    if busca:
        planetas_filtrados = planetas_filtrados.filter(
            Q(nome__icontains=busca) |
            Q(sistema_planetario__nome__icontains=busca) |
            Q(tipo__icontains=busca) |
            Q(descricao__icontains=busca)  
        )

    if tipo:
        planetas_filtrados = planetas_filtrados.filter(tipo=tipo)
    
    if sistema:
        planetas_filtrados = planetas_filtrados.filter(sistema_planetario_id=sistema)
    
    if agua == "sim":
        planetas_filtrados = planetas_filtrados.filter(possui_agua=True)
    elif agua == "nao":
        planetas_filtrados = planetas_filtrados.filter(possui_agua=False)
    
    if atmosfera == "sim":
        planetas_filtrados = planetas_filtrados.filter(possui_atmosfera=True)
    elif atmosfera == "nao":
        planetas_filtrados = planetas_filtrados.filter(possui_atmosfera=False)

    campos_ordenacao = ["nome", "tipo", "diametro", "massa", "temperatura_media", "periodo_orbital"]
    if ordenar in campos_ordenacao:
        planetas_filtrados = planetas_filtrados.order_by(ordenar)
    else:
        planetas_filtrados = planetas_filtrados.order_by("nome")

    #  contagens de planetas
    total_planetas = Planeta.objects.exclude(id__isnull=True).exclude(nome="").exclude(nome__isnull=True).count()
    planetas_filtrados_count = planetas_filtrados.count()

    # contagem sistemas únicos com planetas
    sistemas_com_planetas = SistemaPlanetario.objects.annotate(
        num_planetas=Count('planeta')
    ).filter(num_planetas__gt=0).count()

    paginator = Paginator(planetas_filtrados, 8)
    pagina = request.GET.get("pagina")
    planetas_paginadas = paginator.get_page(pagina)

    context = {
        "planetas": planetas_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "tipo": tipo,
            "sistema": sistema,
            "agua": agua,
            "atmosfera": atmosfera,
        },
        "sistemas": SistemaPlanetario.objects.all(),
        "tipos_planeta": Planeta._meta.get_field('tipo').choices,
        "total_planetas": total_planetas,
        "planetas_filtrados_count": planetas_filtrados_count,
        "sistemas_com_planetas": sistemas_com_planetas,
    }

    return render(request, "corpos_celestes/planetas/listar_planetas.html", context)

@admin_required
def criar_planeta(request):
    if request.method == "POST":
        form = PlanetaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_planetas")
    else:
        form = PlanetaForm()
    return render(request, "corpos_celestes/planetas/form_planetas.html", {"form": form, "titulo": "Criar Planeta"})

@admin_required
def editar_planeta(request, id):
    planeta = get_object_or_404(Planeta, id=id)

    if request.method == "POST":
        form = PlanetaForm(request.POST, request.FILES, instance=planeta)
        if form.is_valid():
            form.save()
            return redirect("listar_planetas")
    else:
        form = PlanetaForm(instance=planeta)

    return render(request, "corpos_celestes/planetas/form_planetas.html", {"form": form, "titulo": "Editar Planeta"})

@admin_required
def deletar_planeta(request, id):
    planeta = get_object_or_404(Planeta, id=id)

    if request.method == "POST":
        nome = planeta.nome
        print(f"Excluindo planeta: {planeta.nome}")  # Log no console
        planeta.delete()
        messages.success(request, f'Planeta "{nome}" excluído com sucesso!')
        return redirect("listar_planetas")

    return redirect("listar_planetas")


def detalhes_planeta(request, id):
    planeta = get_object_or_404(Planeta, id=id)
    satelites = planeta.satelites.all()  # Pega todos os satélites deste planeta
    
    context = {
        'planeta': planeta,
        'satelites': satelites,
    }
    return render(request, "corpos_celestes/planetas/detalhes_planetas.html", context)

# SATÉLITES NATURAIS
def listar_satelites(request):
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    planeta_filtro = request.GET.get("planeta", "")
    sistema_filtro = request.GET.get("sistema", "")

    satelites_filtrados = SateliteNatural.objects.select_related('planeta').all()

    if busca:
        satelites_filtrados = satelites_filtrados.filter(
            Q(nome__icontains=busca) |
            Q(planeta__nome__icontains=busca)
        )

    if planeta_filtro:
        satelites_filtrados = satelites_filtrados.filter(planeta_id=planeta_filtro)

    if sistema_filtro:
        satelites_filtrados = satelites_filtrados.filter(planeta__sistema_planetario_id=sistema_filtro)

    campos_ordenacao = ["nome", "diametro", "massa"]
    if ordenar in campos_ordenacao:
        satelites_filtrados = satelites_filtrados.order_by(ordenar)
    else:
        satelites_filtrados = satelites_filtrados.order_by("nome")

    # CONTAGENS
    total_satelites = SateliteNatural.objects.count()
    satelites_filtrados_count = satelites_filtrados.count()
    
    # Contar planetas únicos com satélites
    planetas_com_luas = Planeta.objects.annotate(
        num_satelites=Count('satelites')
    ).filter(num_satelites__gt=0).count()
    
    # Contar sistemas únicos com satélites
    sistemas_com_luas = SistemaPlanetario.objects.annotate(
        num_satelites=Count('planeta__satelites')
    ).filter(num_satelites__gt=0).count()

    paginator = Paginator(satelites_filtrados, 8)
    pagina = request.GET.get("pagina")
    satelites_paginadas = paginator.get_page(pagina)

    context = {
        "satelites": satelites_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "planeta": planeta_filtro,
            "sistema": sistema_filtro,
        },
        "planetas": Planeta.objects.all(),
        "sistemas": SistemaPlanetario.objects.all(),
        "total_satelites": total_satelites,
        "satelites_filtrados_count": satelites_filtrados_count,
        "planetas_com_luas": planetas_com_luas,
        "sistemas_com_luas": sistemas_com_luas,
    }

    return render(request, "corpos_celestes/satelites/listar_satelites.html", context)

@admin_required
def criar_satelite(request):
    if request.method == "POST":
        form = SateliteNaturalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_satelites")
    else:
        form = SateliteNaturalForm()
    
    # CORREÇÃO: template correto para formulário
    return render(request, "corpos_celestes/satelites/form_satelites.html", {
        "form": form, 
        "titulo": "Criar Satélite"
    })

@admin_required
def editar_satelite(request, id):
    satelite = get_object_or_404(SateliteNatural, id=id)

    if request.method == "POST":
        form = SateliteNaturalForm(request.POST, request.FILES, instance=satelite)
        if form.is_valid():
            form.save()
            return redirect("listar_satelites")
    else:
        form = SateliteNaturalForm(instance=satelite)

    return render(request, "corpos_celestes/satelites/form_satelites.html", {
        "form": form, 
        "titulo": "Editar Satélite"
    })

@admin_required
def deletar_satelite(request, id):
    satelite = get_object_or_404(SateliteNatural, id=id)

    if request.method == "POST":
        nome = satelite.nome
        print(f"Excluindo satélite: {satelite.nome}")  # Log no console
        satelite.delete()
        messages.success(request, f'Satélite "{nome}" excluído com sucesso!')
        return redirect("listar_satelites")

    return redirect("listar_satelites")

def detalhes_satelite(request, id):
    satelite = get_object_or_404(SateliteNatural, id=id)
    
    context = {
        'satelite': satelite,
    }
    return render(request, "corpos_celestes/satelites/detalhes_satelites.html", context)