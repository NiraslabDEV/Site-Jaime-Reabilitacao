// ============================================
// NAVEGAÇÃO E UTILITÁRIOS GERAIS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Menu mobile toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
        
        // Fechar menu ao clicar em um link
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
        
        // Fechar menu ao clicar fora
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                navMenu.classList.remove('active');
            }
        });
    }

    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Adicionar efeito de hover nos cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Função para formatar preço
function formatarPreco(valor) {
    return new Intl.NumberFormat('pt-BR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(valor) + ' MT';
}

// Função para obter parâmetro da URL
function obterParametroURL(nome) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(nome);
}

