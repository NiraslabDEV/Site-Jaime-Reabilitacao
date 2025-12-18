# 🛍️ Loja Virtual - Landing Page com Carrinho + M-Pesa

Landing page completa de e-commerce com carrinho de compras e integração M-Pesa (mock).

## 📋 Características

- ✅ **Frontend puro**: HTML + CSS + JavaScript (sem frameworks pesados)
- ✅ **Design moderno e responsivo**: Mobile-first, leve e rápido
- ✅ **Carrinho funcional**: Adicionar/remover itens, atualizar quantidade
- ✅ **Persistência**: Carrinho salvo em localStorage
- ✅ **Integração M-Pesa**: Endpoint mock preparado para integração real
- ✅ **UX otimizada**: Feedback visual, loading states, notificações

## 🚀 Como Usar

### 1. Iniciar o Backend (FastAPI)

```bash
# Ativar ambiente virtual (se necessário)
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Instalar dependências (se ainda não instalou)
pip install -r requirements.txt

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em: `http://localhost:8000`

### 2. Abrir a Landing Page

Abra o arquivo `index.html` no navegador ou use um servidor local:

```bash
# Python
python -m http.server 8080

# Node.js
npx http-server -p 8080
```

Acesse: `http://localhost:8080`

### 3. Testar o Fluxo

1. **Navegar pelos produtos**: Veja os 9 produtos (bonés, artes, roupas)
2. **Adicionar ao carrinho**: Clique em "Adicionar ao Carrinho"
3. **Abrir carrinho**: Clique no ícone do carrinho no header
4. **Ajustar quantidades**: Use os botões + e -
5. **Remover itens**: Clique no ícone 🗑️
6. **Pagar**: Clique em "Pagar com M-Pesa"
7. **Preencher dados**: Insira número de telefone (9 dígitos)
8. **Confirmar**: O sistema simula o pagamento

## 📁 Estrutura de Arquivos

```
.
├── index.html              # Landing page principal
├── style.css               # Estilos modernos e responsivos
├── script.js               # Lógica do carrinho e pagamento
├── app/
│   ├── main.py            # FastAPI app (atualizado)
│   ├── routers/
│   │   └── payment.py     # Endpoint /api/payment
│   └── schemas/
│       └── payment.py     # Schemas Pydantic para pagamento
└── LOJA_VIRTUAL_README.md  # Este arquivo
```

## 🎨 Produtos Disponíveis

A loja vem com 9 produtos pré-configurados:

### Bonés (3 produtos)
- Boné Snapback Premium - 450,00 MTZ
- Boné Trucker Clássico - 380,00 MTZ
- Boné Beanie Inverno - 250,00 MTZ

### Artes (3 produtos)
- Arte Digital Abstrata - 1.200,00 MTZ
- Pintura Moderna - 1.500,00 MTZ
- Arte em Tela Personalizada - 2.000,00 MTZ

### Roupas (3 produtos)
- Camiseta Básica Premium - 350,00 MTZ
- Camiseta Estampada - 420,00 MTZ
- Moletom com Capuz - 680,00 MTZ

## 🔌 API Endpoints

### POST `/api/payment`

Processa pagamento via M-Pesa (mock).

**Request:**
```json
{
    "amount": 450.00,
    "phone_number": "841234567",
    "order_reference": "ORD-ABC123"
}
```

**Response (Sucesso):**
```json
{
    "success": true,
    "message": "Pagamento iniciado. Confirme no seu telefone.",
    "transaction_id": "TXN-123456789",
    "order_reference": "ORD-ABC123",
    "amount": 450.00,
    "phone_number": "841234567",
    "status": "pending",
    "timestamp": "2024-01-01T12:00:00"
}
```

### GET `/api/payment/status/{transaction_id}`

Consulta status de um pagamento.

## 🔧 Personalização

### Adicionar/Modificar Produtos

Edite o array `produtos` em `script.js`:

```javascript
const produtos = [
    {
        id: 10,
        nome: "Novo Produto",
        preco: 500.00,
        imagem: "🆕",
        categoria: "roupas"
    },
    // ... mais produtos
];
```

### Alterar API URL

Em `script.js`, ajuste a constante:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Personalizar Cores

Edite as variáveis CSS em `style.css`:

```css
:root {
    --primary: #2563eb;
    --secondary: #10b981;
    /* ... */
}
```

## 🔐 Integração Real com M-Pesa

O código está preparado para integração real. Veja comentários em `app/routers/payment.py` com instruções detalhadas.

**Requisitos:**
1. Credenciais M-Pesa (Consumer Key, Secret, Passkey)
2. Business Short Code
3. Configurar callback URL
4. Implementar validação de callbacks

**Bibliotecas sugeridas:**
- `requests` para chamadas HTTP
- Variáveis de ambiente para credenciais
- HTTPS obrigatório em produção

## 📱 Responsividade

A loja é totalmente responsiva:
- **Desktop**: Grid de produtos, carrinho lateral
- **Tablet**: Layout adaptado, carrinho em tela cheia
- **Mobile**: Coluna única, carrinho em tela cheia

## 🎯 Funcionalidades Implementadas

- ✅ Hero section atrativa
- ✅ Grid de produtos responsivo
- ✅ Carrinho lateral com animações
- ✅ Adicionar/remover produtos
- ✅ Atualizar quantidades
- ✅ Cálculo automático do total
- ✅ Persistência em localStorage
- ✅ Modal de pagamento
- ✅ Validação de formulário
- ✅ Integração com backend (mock)
- ✅ Notificações toast
- ✅ Feedback visual (loading, sucesso, erro)
- ✅ Design moderno e limpo

## 🐛 Troubleshooting

### Backend não responde
- Verifique se o servidor está rodando: `http://localhost:8000`
- Confira se a porta 8000 está livre
- Verifique logs do servidor

### CORS Error
- O backend já está configurado com CORS permissivo
- Em produção, ajuste `allow_origins` em `app/main.py`

### Carrinho não persiste
- Verifique se localStorage está habilitado no navegador
- Limpe cache e tente novamente

## 📝 Notas Importantes

1. **Pagamento é Mock**: O sistema simula pagamentos (80% sucesso, 20% falha)
2. **Sem Banco de Dados**: Carrinho salvo apenas no localStorage do navegador
3. **Pronto para Produção**: Estrutura preparada para integração real
4. **Segurança**: Em produção, valide todos os dados no backend
5. **HTTPS**: Obrigatório para integração real com M-Pesa

## 🚀 Próximos Passos

Para produção:
1. Integrar M-Pesa real (STK Push)
2. Adicionar banco de dados para pedidos
3. Implementar autenticação de usuários
4. Adicionar gestão de estoque
5. Configurar webhooks para callbacks
6. Implementar notificações por email/SMS
7. Adicionar analytics e tracking

## 📄 Licença

Este projeto é privado e proprietário.

---

**Desenvolvido com foco em simplicidade, velocidade e clareza.** 🚀





