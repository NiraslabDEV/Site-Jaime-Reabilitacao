// ============================================
// CONFIGURAÇÃO E DADOS
// ============================================

// Array de produtos (bonés, artes, roupas)
const produtos = [
    {
        id: 1,
        nome: "Boné Snapback Premium",
        preco: 450.00,
        imagem: "🧢",
        categoria: "bonés"
    },
    {
        id: 2,
        nome: "Boné Trucker Clássico",
        preco: 380.00,
        imagem: "⛑️",
        categoria: "bonés"
    },
    {
        id: 3,
        nome: "Boné Beanie Inverno",
        preco: 250.00,
        imagem: "🎩",
        categoria: "bonés"
    },
    {
        id: 4,
        nome: "Arte Digital Abstrata",
        preco: 1200.00,
        imagem: "🎨",
        categoria: "artes"
    },
    {
        id: 5,
        nome: "Pintura Moderna",
        preco: 1500.00,
        imagem: "🖼️",
        categoria: "artes"
    },
    {
        id: 6,
        nome: "Arte em Tela Personalizada",
        preco: 2000.00,
        imagem: "🖌️",
        categoria: "artes"
    },
    {
        id: 7,
        nome: "Camiseta Básica Premium",
        preco: 350.00,
        imagem: "👕",
        categoria: "roupas"
    },
    {
        id: 8,
        nome: "Camiseta Estampada",
        preco: 420.00,
        imagem: "👔",
        categoria: "roupas"
    },
    {
        id: 9,
        nome: "Moletom com Capuz",
        preco: 680.00,
        imagem: "🧥",
        categoria: "roupas"
    }
];

// API Base URL (ajuste conforme necessário)
const API_BASE_URL = 'http://localhost:8000';

// ============================================
// ESTADO DO CARRINHO
// ============================================

let carrinho = [];

// Carregar carrinho do localStorage ao iniciar
function carregarCarrinho() {
    const carrinhoSalvo = localStorage.getItem('carrinho');
    if (carrinhoSalvo) {
        try {
            carrinho = JSON.parse(carrinhoSalvo);
            atualizarCarrinho();
        } catch (e) {
            console.error('Erro ao carregar carrinho:', e);
            carrinho = [];
        }
    }
}

// Salvar carrinho no localStorage
function salvarCarrinho() {
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
}

// ============================================
// INICIALIZAÇÃO
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    carregarCarrinho();
    renderizarProdutos();
    inicializarEventos();
});

// ============================================
// RENDERIZAÇÃO DE PRODUTOS
// ============================================

function renderizarProdutos() {
    const productsGrid = document.getElementById('productsGrid');
    if (!productsGrid) return;

    productsGrid.innerHTML = produtos.map(produto => `
        <div class="product-card">
            <div class="product-image">${produto.imagem}</div>
            <div class="product-info">
                <h3 class="product-name">${produto.nome}</h3>
                <div class="product-price">${formatarPreco(produto.preco)}</div>
                <button class="btn-add-cart" onclick="adicionarAoCarrinho(${produto.id})">
                    Adicionar ao Carrinho
                </button>
            </div>
        </div>
    `).join('');
}

// ============================================
// GERENCIAMENTO DO CARRINHO
// ============================================

function adicionarAoCarrinho(produtoId) {
    const produto = produtos.find(p => p.id === produtoId);
    if (!produto) return;

    const itemExistente = carrinho.find(item => item.id === produtoId);
    
    if (itemExistente) {
        itemExistente.quantidade += 1;
    } else {
        carrinho.push({
            ...produto,
            quantidade: 1
        });
    }

    salvarCarrinho();
    atualizarCarrinho();
    mostrarToast('Produto adicionado ao carrinho!', 'success');
}

function removerDoCarrinho(produtoId) {
    carrinho = carrinho.filter(item => item.id !== produtoId);
    salvarCarrinho();
    atualizarCarrinho();
    mostrarToast('Produto removido do carrinho', 'warning');
}

function atualizarQuantidade(produtoId, novaQuantidade) {
    if (novaQuantidade <= 0) {
        removerDoCarrinho(produtoId);
        return;
    }

    const item = carrinho.find(item => item.id === produtoId);
    if (item) {
        item.quantidade = novaQuantidade;
        salvarCarrinho();
        atualizarCarrinho();
    }
}

function calcularTotal() {
    return carrinho.reduce((total, item) => {
        return total + (item.preco * item.quantidade);
    }, 0);
}

function atualizarCarrinho() {
    // Atualizar contador do header
    const cartCount = document.getElementById('cartCount');
    const totalItens = carrinho.reduce((sum, item) => sum + item.quantidade, 0);
    if (cartCount) {
        cartCount.textContent = totalItens;
        cartCount.style.display = totalItens > 0 ? 'flex' : 'none';
    }

    // Atualizar corpo do carrinho
    const cartEmpty = document.getElementById('cartEmpty');
    const cartItems = document.getElementById('cartItems');
    const cartFooter = document.getElementById('cartFooter');
    const totalAmount = document.getElementById('totalAmount');
    const btnPay = document.getElementById('btnPay');

    if (carrinho.length === 0) {
        if (cartEmpty) cartEmpty.classList.add('active');
        if (cartItems) cartItems.classList.remove('active');
        if (cartFooter) cartFooter.style.display = 'none';
    } else {
        if (cartEmpty) cartEmpty.classList.remove('active');
        if (cartItems) cartItems.classList.add('active');
        if (cartFooter) cartFooter.style.display = 'block';

        // Renderizar itens
        if (cartItems) {
            cartItems.innerHTML = carrinho.map(item => `
                <div class="cart-item">
                    <div class="cart-item-image">${item.imagem}</div>
                    <div class="cart-item-info">
                        <div class="cart-item-name">${item.nome}</div>
                        <div class="cart-item-price">${formatarPreco(item.preco)}</div>
                        <div class="cart-item-controls">
                            <button class="quantity-btn" onclick="atualizarQuantidade(${item.id}, ${item.quantidade - 1})">-</button>
                            <span class="quantity-display">${item.quantidade}</span>
                            <button class="quantity-btn" onclick="atualizarQuantidade(${item.id}, ${item.quantidade + 1})">+</button>
                            <button class="btn-remove-item" onclick="removerDoCarrinho(${item.id})" title="Remover">🗑️</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Atualizar total
        const total = calcularTotal();
        if (totalAmount) {
            totalAmount.textContent = formatarPreco(total);
        }
        if (btnPay) {
            btnPay.disabled = false;
        }
    }
}

// ============================================
// CONTROLE DO CARRINHO LATERAL
// ============================================

function abrirCarrinho() {
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    
    if (cartSidebar) cartSidebar.classList.add('active');
    if (cartOverlay) cartOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function fecharCarrinho() {
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    
    if (cartSidebar) cartSidebar.classList.remove('active');
    if (cartOverlay) cartOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

// ============================================
// MODAL DE PAGAMENTO
// ============================================

function abrirModalPagamento() {
    const paymentModal = document.getElementById('paymentModal');
    const modalTotal = document.getElementById('modalTotal');
    const orderRef = document.getElementById('orderRef');
    
    if (!paymentModal) return;

    const total = calcularTotal();
    if (modalTotal) modalTotal.textContent = formatarPreco(total);
    
    // Gerar referência única do pedido
    const referencia = 'ORD-' + Date.now().toString(36).toUpperCase();
    if (orderRef) orderRef.textContent = referencia;

    paymentModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function fecharModalPagamento() {
    const paymentModal = document.getElementById('paymentModal');
    if (paymentModal) {
        paymentModal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============================================
// PROCESSAMENTO DE PAGAMENTO
// ============================================

async function processarPagamento(event) {
    event.preventDefault();

    const phoneNumber = document.getElementById('phoneNumber').value;
    const btnSubmitPayment = document.getElementById('btnSubmitPayment');
    const orderRef = document.getElementById('orderRef').textContent;
    const total = calcularTotal();

    if (!phoneNumber || phoneNumber.length !== 9) {
        mostrarToast('Por favor, insira um número de telefone válido (9 dígitos)', 'error');
        return;
    }

    // Desabilitar botão e mostrar loading
    if (btnSubmitPayment) {
        btnSubmitPayment.disabled = true;
        btnSubmitPayment.textContent = 'Processando...';
    }

    try {
        // Preparar dados do pagamento
        const paymentData = {
            amount: total,
            phone_number: phoneNumber,
            order_reference: orderRef
        };

        // Enviar requisição para o backend
        const response = await fetch(`${API_BASE_URL}/api/payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paymentData)
        });

        const data = await response.json();

        if (response.ok && data.success) {
            mostrarToast('Pagamento iniciado! Confirme no seu telefone.', 'success');
            
            // Limpar carrinho após pagamento bem-sucedido
            setTimeout(() => {
                carrinho = [];
                salvarCarrinho();
                atualizarCarrinho();
                fecharModalPagamento();
                fecharCarrinho();
                
                // Resetar formulário
                document.getElementById('paymentForm').reset();
            }, 2000);
        } else {
            mostrarToast(data.message || 'Erro ao processar pagamento. Tente novamente.', 'error');
        }
    } catch (error) {
        console.error('Erro ao processar pagamento:', error);
        mostrarToast('Erro de conexão. Verifique se o servidor está rodando.', 'error');
    } finally {
        // Reabilitar botão
        if (btnSubmitPayment) {
            btnSubmitPayment.disabled = false;
            btnSubmitPayment.textContent = 'Confirmar Pagamento';
        }
    }
}

// ============================================
// EVENTOS
// ============================================

function inicializarEventos() {
    // Toggle do carrinho
    const cartToggle = document.getElementById('cartToggle');
    if (cartToggle) {
        cartToggle.addEventListener('click', abrirCarrinho);
    }

    // Fechar carrinho
    const cartClose = document.getElementById('cartClose');
    if (cartClose) {
        cartClose.addEventListener('click', fecharCarrinho);
    }

    // Overlay do carrinho
    const cartOverlay = document.getElementById('cartOverlay');
    if (cartOverlay) {
        cartOverlay.addEventListener('click', fecharCarrinho);
    }

    // Botão pagar
    const btnPay = document.getElementById('btnPay');
    if (btnPay) {
        btnPay.addEventListener('click', () => {
            fecharCarrinho();
            setTimeout(abrirModalPagamento, 300);
        });
    }

    // Modal de pagamento
    const paymentClose = document.getElementById('paymentClose');
    if (paymentClose) {
        paymentClose.addEventListener('click', fecharModalPagamento);
    }

    const paymentModal = document.getElementById('paymentModal');
    if (paymentModal) {
        paymentModal.addEventListener('click', (e) => {
            if (e.target === paymentModal) {
                fecharModalPagamento();
            }
        });
    }

    // Formulário de pagamento
    const paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', processarPagamento);
    }

    // Fechar com ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            fecharCarrinho();
            fecharModalPagamento();
        }
    });
}

// ============================================
// TOAST NOTIFICATIONS
// ============================================

function mostrarToast(mensagem, tipo = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.textContent = mensagem;

    toastContainer.appendChild(toast);

    // Remover após 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// ============================================
// UTILITÁRIOS
// ============================================

function formatarPreco(valor) {
    // Formatação compatível para Metical de Moçambique (MTZ)
    // Se o navegador não suportar MZN, usa formatação manual
    try {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'MZN',
            minimumFractionDigits: 2
        }).format(valor);
    } catch (e) {
        // Fallback para formatação manual
        return new Intl.NumberFormat('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(valor) + ' MTZ';
    }
}

// Exportar funções para uso global
window.adicionarAoCarrinho = adicionarAoCarrinho;
window.removerDoCarrinho = removerDoCarrinho;
window.atualizarQuantidade = atualizarQuantidade;
