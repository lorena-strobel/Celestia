// Função para confirmar exclusão
function confirmarExclusao(url, nome, tipo = 'item') {
    if (confirm(`Tem certeza que deseja excluir ${tipo} "${nome}"?\n\nEsta ação não pode ser desfeita.`)) {
        
        // Cria um formulário dinâmico
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = url;
        form.style.display = 'none';
        
        // Busca o token CSRF de 3 formas diferentes (para garantir)
        let csrfToken = '';
        
        // 1. Tenta pelo input hidden
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) {
            csrfToken = csrfInput.value;
        }
        // 2. Tenta pela meta tag
        else {
            const metaTag = document.querySelector('meta[name="csrf-token"]');
            if (metaTag) {
                csrfToken = metaTag.getAttribute('content');
            }
        }
        // 3. Se ainda não encontrou, tenta pelo cookie (fallback)
        if (!csrfToken) {
            csrfToken = getCookie('csrftoken');
        }
        
        // Se encontrou o token, adiciona ao formulário
        if (csrfToken) {
            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'csrfmiddlewaretoken';
            tokenInput.value = csrfToken;
            form.appendChild(tokenInput);
        } else {
            console.error(' Token CSRF não encontrado!');
            alert('Erro de segurança. Por favor, recarregue a página.');
            return;
        }
        
        // Adiciona o formulário na página e envia
        document.body.appendChild(form);
        form.submit();
    }
}

// Função auxiliar para pegar cookie (fallback)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Ativa os botões automaticamente quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Encontra todos os botões com classe 'btn-excluir'
    const botoesExcluir = document.querySelectorAll('.btn-excluir');
    
    botoesExcluir.forEach(botao => {
        botao.addEventListener('click', function(e) {
            e.preventDefault(); // Impede comportamento padrão
            
            // Pega os dados do botão
            const url = this.getAttribute('data-url');
            const nome = this.getAttribute('data-nome');
            const tipo = this.getAttribute('data-tipo') || 'item';
            
            // Chama a função de confirmação
            confirmarExclusao(url, nome, tipo);
        });
    });
    
    // Debug: verifica se encontrou CSRF token
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    
    if (csrfInput || metaTag) {
        console.log(' Token CSRF encontrado no DOM');
    } else {
        console.warn(' Token CSRF não encontrado no DOM. Verifique o base.html');
    }
    
    console.log(` ${botoesExcluir.length} botões de exclusão ativados`);
});