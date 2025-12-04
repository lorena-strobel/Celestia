from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import MissaoEspacialForm, AstronautaForm
from .models import MissaoEspacial, Astronauta

# Create your views here.
def admin_required(view_func):
    return user_passes_test(lambda user: user.is_superuser)(view_func)

def visualizarExploracao(request):
    return render(request,"exploracao_espacial/index.html")

def listar_missoes(request):
    # Coleta parâmetros
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "-data_lancamento")
    status = request.GET.get("status", "")
    tipo = request.GET.get("tipo", "")
    agencia = request.GET.get("agencia", "")
    orcamento_max = request.GET.get("orcamento_max")

    # Query inicial
    missoes_qs = MissaoEspacial.objects.all()

    # Busca multi-campo
    if busca:
        missoes_qs = missoes_qs.filter(
            Q(nome__icontains=busca) |
            Q(agencia__icontains=busca) |
            Q(objetivo__icontains=busca) |
            Q(curiosidades__icontains=busca)
        )

    # Filtros avançados
    if status:
        missoes_qs = missoes_qs.filter(status=status)
    
    if tipo:
        missoes_qs = missoes_qs.filter(tipo=tipo)
    
    if agencia:
        missoes_qs = missoes_qs.filter(agencia__icontains=agencia)

    if orcamento_max:
        missoes_qs = missoes_qs.filter(orcamento__lte=orcamento_max)
    
    # Ordenação segura
    campos_ordenacao = ["nome", "data_lancamento", "data_termino", "status", "tipo", "agencia", "orcamento"]

    if ordenar.lstrip('-') in campos_ordenacao:
        missoes_qs = missoes_qs.order_by(ordenar)
    else:
        missoes_qs = missoes_qs.order_by("-data_lancamento")

    # Paginação
    paginator = Paginator(missoes_qs, 8)
    pagina = request.GET.get("pagina")
    missoes_paginadas = paginator.get_page(pagina)

    # Agências únicas para filtro
    agencias = MissaoEspacial.objects.values_list('agencia', flat=True).distinct()

    context = {
        "missoes": missoes_paginadas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "status": status,
            "tipo": tipo,
            "agencia": agencia,
        },
        "status_choices": MissaoEspacial.STATUS_CHOICES,
        "tipo_choices": MissaoEspacial.TIPO_CHOICES,
        "agencias": agencias,
        "orcamento_max": orcamento_max,
    }

    return render(request, "exploracao_espacial/missoes/listar_missoes.html", context)

def detalhes_missao(request, pk): 
    missao = get_object_or_404(MissaoEspacial, pk=pk)
    tripulantes = missao.tripulantes.all()
    
    return render(request, "exploracao_espacial/missoes/detalhes_missoes.html", {
        "missao": missao,
        "tripulantes": tripulantes
    })

@admin_required
def criar_missao(request):
    if request.method == "POST":
        form = MissaoEspacialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_missoes")
    else:
        form = MissaoEspacialForm()
    
    return render(request, "exploracao_espacial/missoes/forms_missoes.html", {"form": form, "titulo": "Criar Missão Espacial"})

@admin_required
def editar_missao(request, pk):
    missao = get_object_or_404(MissaoEspacial, pk=pk)

    if request.method == "POST":
        form = MissaoEspacialForm(request.POST, request.FILES, instance=missao)
        if form.is_valid():
            form.save()
            return redirect("detalhes_missao", pk=pk)
    else:
        form = MissaoEspacialForm(instance=missao)

    return render(request, "exploracao_espacial/missoes/forms_missoes.html", {"form": form, "titulo": "Editar Missão"})

@admin_required
def excluir_missao(request, pk):
    missao = get_object_or_404(MissaoEspacial, pk=pk)

    if request.method == "POST":
        nome = missao.nome
        missao.delete()
        messages.success(request, f'Missão "{nome}" excluída com sucesso!')
        return redirect("listar_missoes")

    messages.error(request, "Ação inválida.")
    return redirect("listar_missoes")


def listar_astronautas(request):
    # Coleta parâmetros
    busca = request.GET.get("busca", "")
    ordenar = request.GET.get("ordenar", "nome")
    status = request.GET.get("status", "")
    nacionalidade = request.GET.get("nacionalidade", "")
    genero = request.GET.get("genero", "")

    total_astronautas = Astronauta.objects.count()

    # Query inicial
    astronautas_filtrados = Astronauta.objects.all()

    # Busca multi-campo
    if busca:
        astronautas_filtrados = astronautas_filtrados.filter(
            Q(nome__icontains=busca) |
            Q(nacionalidade__icontains=busca) |
            Q(biografia__icontains=busca)
        )

    # Filtros avançados
    if status:
        astronautas_filtrados = astronautas_filtrados.filter(status=status)
    
    if nacionalidade:
        astronautas_filtrados = astronautas_filtrados.filter(nacionalidade__icontains=nacionalidade)
    
    if genero:
        astronautas_filtrados = astronautas_filtrados.filter(genero=genero)

    # Ordenação segura
    campos_ordenacao = ["nome", "data_nascimento", "nacionalidade", "status"]
    if ordenar in campos_ordenacao:
        astronautas_filtrados = astronautas_filtrados.order_by(ordenar)
    else:
        astronautas_filtrados = astronautas_filtrados.order_by("nome")

    # Paginação
    paginator = Paginator(astronautas_filtrados, 8)
    pagina = request.GET.get("pagina")
    astronautas_paginadas = paginator.get_page(pagina)

    # Nacionalidades únicas para filtro
    nacionalidades = Astronauta.objects.values_list(
        'nacionalidade', flat=True
    ).distinct()

    context = {
        "astronautas": astronautas_paginadas,
        "total_astronautas": total_astronautas,
        "busca": busca,
        "ordenar": ordenar,
        "filtros": {
            "status": status,
            "nacionalidade": nacionalidade,
            "genero": genero,
        },
        "status_choices": Astronauta.STATUS_CHOICES,
        "genero_choices": Astronauta.GENERO_CHOICES,
        "nacionalidades": nacionalidades,
    }

    return render(request, "exploracao_espacial/astronautas/listar_astronautas.html", context)


def detalhes_astronauta(request, pk):  
    astronauta = get_object_or_404(Astronauta, pk=pk)
    missoes = astronauta.missoes.all()
    
    return render(request, "exploracao_espacial/astronautas/detalhes_astronautas.html", {
        "astronauta": astronauta,
        "missoes": missoes
    })

@admin_required
def criar_astronauta(request):
    if request.method == "POST":
        form = AstronautaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listar_astronautas")
    else:
        form = AstronautaForm()

    return render(request, "exploracao_espacial/astronautas/forms_astronautas.html", {"form": form, "titulo": "Registrar Astronauta"})

@admin_required
def editar_astronauta(request, pk):
    astronauta = get_object_or_404(Astronauta, pk=pk)

    if request.method == "POST":
        form = AstronautaForm(request.POST, request.FILES, instance=astronauta)
        if form.is_valid():
            form.save()
            return redirect("detalhes_astronauta", pk=pk)
    else:
        form = AstronautaForm(instance=astronauta)

    return render(request, "exploracao_espacial/astronautas/forms_astronautas.html", {"form": form, "titulo": "Editar Astronauta"})

@admin_required
def excluir_astronauta(request, pk):
    astronauta = get_object_or_404(Astronauta, pk=pk)

    if request.method == "POST":
        nome = astronauta.nome
        astronauta.delete()
        messages.success(request, f'Astronauta "{nome}" excluído com sucesso!')
        return redirect("listar_astronautas")

    messages.error(request, "Ação inválida.")
    return redirect("listar_astronautas")