// ============================================
// FUNIL INTERATIVO - LÓGICA COMPLETA
// ============================================

// Estado do funil
const estadoFunil = {
    objetivo: null,
    avaliacao: true, // Sempre true (obrigatória)
    frequencia: null,
    frequenciaValor: 0,
    modalidade: 'presencial',
    hibrido: false,
    focoEspecifico: false,
    suporteExtra: false,
    total: 700, // Avaliação obrigatória
    nome: '',
    whatsapp: '',
    bairro: ''
};

let passoAtual = 1;
const totalPassos = 9;

// ============================================
// INICIALIZAÇÃO
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Verificar se há objetivo na URL
    const objetivoURL = obterParametroURL('objetivo');
    if (objetivoURL && ['reabilitacao', 'idosos', 'atletas'].includes(objetivoURL)) {
        estadoFunil.objetivo = objetivoURL;
        // Avançar automaticamente para o passo 2
        setTimeout(() => {
            avancarPasso();
        }, 500);
    }

    inicializarEventos();
    atualizarTotalParcial();
    atualizarProgresso();
});

// ============================================
// EVENTOS
// ============================================

function inicializarEventos() {
    // Opções clicáveis
    document.querySelectorAll('.option-card').forEach(card => {
        card.addEventListener('click', function() {
            const stepId = this.closest('.funil-step').id;
            selecionarOpcao(this, stepId);
        });
    });

    // Botões de navegação
    const btnAvancar = document.getElementById('btnAvancar');
    const btnVoltar = document.getElementById('btnVoltar');

    if (btnAvancar) {
        btnAvancar.addEventListener('click', avancarPasso);
    }

    if (btnVoltar) {
        btnVoltar.addEventListener('click', voltarPasso);
    }

    // Formulário de dados
    const formDados = document.getElementById('formDados');
    if (formDados) {
        formDados.addEventListener('submit', function(e) {
            e.preventDefault();
            coletarDados();
            avancarPasso();
        });
    }
}

// ============================================
// SELEÇÃO DE OPÇÕES
// ============================================

function selecionarOpcao(card, stepId) {
    // Remover seleção anterior no mesmo passo
    const step = card.closest('.funil-step');
    step.querySelectorAll('.option-card').forEach(c => {
        c.classList.remove('selected');
    });

    // Adicionar seleção
    card.classList.add('selected');

    // Processar seleção baseado no passo
    const valor = card.dataset.value;
    const preco = parseFloat(card.dataset.price) || 0;

    switch (stepId) {
        case 'step1':
            estadoFunil.objetivo = valor;
            setTimeout(() => avancarPasso(), 300);
            break;

        case 'step3':
            estadoFunil.frequencia = valor;
            estadoFunil.frequenciaValor = preco;
            atualizarTotalParcial();
            setTimeout(() => avancarPasso(), 300);
            break;

        case 'step4':
            estadoFunil.modalidade = valor;
            estadoFunil.hibrido = valor === 'hibrido';
            calcularTotal();
            setTimeout(() => avancarPasso(), 300);
            break;

        case 'step5':
            estadoFunil.focoEspecifico = valor === 'sim';
            calcularTotal();
            setTimeout(() => avancarPasso(), 300);
            break;

        case 'step6':
            estadoFunil.suporteExtra = valor === 'sim';
            calcularTotal();
            setTimeout(() => avancarPasso(), 300);
            break;
    }

    // Atualizar totais
    calcularTotal();
}

// ============================================
// NAVEGAÇÃO ENTRE PASSOS
// ============================================

// Tornar função global para uso no HTML
window.avancarPasso = function() {
    // Validações antes de avançar
    if (!validarPassoAtual()) {
        return;
    }

    if (passoAtual < totalPassos) {
        // Esconder passo atual
        const stepAtual = document.getElementById(`step${passoAtual}`);
        if (stepAtual) {
            stepAtual.classList.remove('active');
        }

        // Avançar
        passoAtual++;

        // Mostrar próximo passo
        const proximoStep = document.getElementById(`step${passoAtual}`);
        if (proximoStep) {
            proximoStep.classList.add('active');
        }

        // Ações específicas por passo
        if (passoAtual === 7) {
            gerarResumoFinal();
        } else if (passoAtual === 9) {
            enviarWhatsApp();
        }

        atualizarNavegacao();
        atualizarProgresso();
        atualizarTotalParcial();
        
        // Scroll para o topo
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
};

function voltarPasso() {
    if (passoAtual > 1) {
        // Esconder passo atual
        const stepAtual = document.getElementById(`step${passoAtual}`);
        if (stepAtual) {
            stepAtual.classList.remove('active');
        }

        // Voltar
        passoAtual--;

        // Mostrar passo anterior
        const stepAnterior = document.getElementById(`step${passoAtual}`);
        if (stepAnterior) {
            stepAnterior.classList.add('active');
        }

        atualizarNavegacao();
        atualizarProgresso();
        atualizarTotalParcial();
        
        // Scroll para o topo
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function validarPassoAtual() {
    switch (passoAtual) {
        case 1:
            if (!estadoFunil.objetivo) {
                alert('Por favor, selecione seu objetivo principal.');
                return false;
            }
            break;
        case 2:
            // Passo 2 não precisa validação, só informativo
            break;
        case 3:
            if (!estadoFunil.frequencia) {
                alert('Por favor, selecione a frequência de sessões.');
                return false;
            }
            break;
        case 4:
            if (!estadoFunil.modalidade) {
                alert('Por favor, selecione a modalidade.');
                return false;
            }
            break;
        case 8:
            const nome = document.getElementById('nome').value.trim();
            const whatsapp = document.getElementById('whatsapp').value.trim();
            const bairro = document.getElementById('bairro').value.trim();

            if (!nome || !whatsapp || !bairro) {
                alert('Por favor, preencha todos os campos.');
                return false;
            }

            if (whatsapp.length !== 9 || !/^\d+$/.test(whatsapp)) {
                alert('Por favor, insira um número de WhatsApp válido (9 dígitos).');
                return false;
            }
            break;
    }
    return true;
}

function atualizarNavegacao() {
    const funilNavigation = document.getElementById('funilNavigation');
    const btnVoltar = document.getElementById('btnVoltar');
    const btnAvancar = document.getElementById('btnAvancar');

    if (passoAtual === 1) {
        // Primeiro passo - sem navegação
        if (funilNavigation) funilNavigation.style.display = 'none';
    } else if (passoAtual === 2) {
        // Passo 2 (avaliação) - botão dentro do card, sem navegação externa
        if (funilNavigation) funilNavigation.style.display = 'none';
    } else if (passoAtual === 9) {
        // Último passo - sem navegação
        if (funilNavigation) funilNavigation.style.display = 'none';
    } else {
        // Passos intermediários - ambos botões
        if (funilNavigation) funilNavigation.style.display = 'flex';
        if (btnVoltar) btnVoltar.style.display = 'block';
        if (btnAvancar) {
            btnAvancar.style.display = 'block';
            btnAvancar.textContent = passoAtual === 8 ? 'Enviar para WhatsApp →' : 'Avançar →';
        }
    }
}

// ============================================
// CÁLCULOS E TOTAIS
// ============================================

function calcularTotal() {
    let total = 700; // Avaliação obrigatória

    // Frequência
    if (estadoFunil.frequenciaValor) {
        total += estadoFunil.frequenciaValor;
    }

    // Híbrido
    if (estadoFunil.hibrido) {
        total += 1500;
    }

    // Foco específico
    if (estadoFunil.focoEspecifico) {
        total += 1000;
    }

    // Suporte extra
    if (estadoFunil.suporteExtra) {
        total += 800;
    }

    estadoFunil.total = total;
    atualizarTotalParcial();
}

function atualizarTotalParcial() {
    const totalParcial = document.getElementById('totalParcial');
    const totalValue = document.getElementById('totalValue');

    if (totalParcial && totalValue) {
        calcularTotal();
        totalValue.textContent = formatarPreco(estadoFunil.total);
        
        // Mostrar a partir do passo 2
        if (passoAtual >= 2) {
            totalParcial.style.display = 'block';
        } else {
            totalParcial.style.display = 'none';
        }
    }
}

function atualizarProgresso() {
    const progressFill = document.getElementById('progressFill');
    if (progressFill) {
        const porcentagem = (passoAtual / totalPassos) * 100;
        progressFill.style.width = porcentagem + '%';
    }
}

// ============================================
// RESUMO FINAL
// ============================================

function gerarResumoFinal() {
    const resumoFinal = document.getElementById('resumoFinal');
    if (!resumoFinal) return;

    const objetivoTexto = {
        'reabilitacao': 'Reabilitação / Dor',
        'idosos': 'Saúde e Autonomia (Idosos)',
        'atletas': 'Performance Esportiva (Atletas)'
    };

    const frequenciaTexto = {
        '1': '1x por semana',
        '2': '2x por semana',
        '3': '3x por semana',
        '5': '5x por semana'
    };

    const modalidadeTexto = {
        'presencial': 'Presencial Domiciliar',
        'hibrido': 'Híbrido (Presencial + Vídeos)'
    };

    calcularTotal();

    resumoFinal.innerHTML = `
        <h3 class="resumo-title">Resumo do Seu Plano</h3>
        
        <div class="resumo-item">
            <span class="resumo-item-label">Objetivo:</span>
            <span class="resumo-item-value">${objetivoTexto[estadoFunil.objetivo] || 'Não informado'}</span>
        </div>

        <div class="resumo-item">
            <span class="resumo-item-label">Avaliação funcional + bioimpedância:</span>
            <span class="resumo-item-value">700 MT</span>
        </div>

        <div class="resumo-item">
            <span class="resumo-item-label">Plano:</span>
            <span class="resumo-item-value">${frequenciaTexto[estadoFunil.frequencia] || 'Não selecionado'} - ${formatarPreco(estadoFunil.frequenciaValor)}/mês</span>
        </div>

        <div class="resumo-item">
            <span class="resumo-item-label">Modalidade:</span>
            <span class="resumo-item-value">${modalidadeTexto[estadoFunil.modalidade] || 'Não selecionado'}</span>
        </div>

        ${estadoFunil.hibrido ? `
        <div class="resumo-item">
            <span class="resumo-item-label">Modalidade Híbrida:</span>
            <span class="resumo-item-value">+1.500 MT/mês</span>
        </div>
        ` : ''}

        ${estadoFunil.focoEspecifico ? `
        <div class="resumo-item">
            <span class="resumo-item-label">Foco Específico:</span>
            <span class="resumo-item-value">+1.000 MT/mês</span>
        </div>
        ` : ''}

        ${estadoFunil.suporteExtra ? `
        <div class="resumo-item">
            <span class="resumo-item-label">Suporte Contínuo:</span>
            <span class="resumo-item-value">+800 MT/mês</span>
        </div>
        ` : ''}

        <div class="resumo-total">
            <span class="resumo-total-label">Total mensal estimado:</span>
            <span class="resumo-total-value">${formatarPreco(estadoFunil.total)}</span>
        </div>
    `;
}

// ============================================
// COLETA DE DADOS
// ============================================

function coletarDados() {
    estadoFunil.nome = document.getElementById('nome').value.trim();
    estadoFunil.whatsapp = document.getElementById('whatsapp').value.trim();
    estadoFunil.bairro = document.getElementById('bairro').value.trim();
}

// ============================================
// ENVIO PARA WHATSAPP
// ============================================

function enviarWhatsApp() {
    coletarDados();

    const objetivoTexto = {
        'reabilitacao': 'Reabilitação / Dor',
        'idosos': 'Saúde e Autonomia (Idosos)',
        'atletas': 'Performance Esportiva (Atletas)'
    };

    const frequenciaTexto = {
        '1': '1x por semana',
        '2': '2x por semana',
        '3': '3x por semana',
        '5': '5x por semana'
    };

    const modalidadeTexto = {
        'presencial': 'Presencial Domiciliar',
        'hibrido': 'Híbrido (Presencial + Vídeos)'
    };

    let servicos = `- Avaliação funcional + bioimpedância (700 MT)
- Plano: ${frequenciaTexto[estadoFunil.frequencia]} (${formatarPreco(estadoFunil.frequenciaValor)}/mês)
- Modalidade: ${modalidadeTexto[estadoFunil.modalidade]}`;

    if (estadoFunil.hibrido) {
        servicos += '\n- Modalidade Híbrida: +1.500 MT/mês';
    }

    if (estadoFunil.focoEspecifico) {
        servicos += '\n- Foco específico: +1.000 MT/mês';
    }

    if (estadoFunil.suporteExtra) {
        servicos += '\n- Suporte contínuo: +800 MT/mês';
    }

    const mensagem = `Olá Jaime, tudo bem?

Meu nome é ${estadoFunil.nome}.

Objetivo: ${objetivoTexto[estadoFunil.objetivo]}

Serviços escolhidos:
${servicos}

Local: Atendimento domiciliar – ${estadoFunil.bairro}

Valor total mensal estimado: ${formatarPreco(estadoFunil.total)}

Aguardo confirmação e formas de pagamento.`;

    // Codificar mensagem para URL
    const mensagemEncoded = encodeURIComponent(mensagem);
    
    // Número do WhatsApp do Jaime
    const whatsappJaime = '258842391741';
    
    // URL do WhatsApp
    const urlWhatsApp = `https://wa.me/${whatsappJaime}?text=${mensagemEncoded}`;
    
    // Aguardar 2 segundos e redirecionar
    setTimeout(() => {
        window.open(urlWhatsApp, '_blank');
    }, 2000);
}

