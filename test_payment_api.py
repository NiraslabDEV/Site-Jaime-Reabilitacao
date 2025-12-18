"""
Script de teste automatizado para API de pagamento M-Pesa
Execute: python test_payment_api.py
"""
import requests
import json
import time
from datetime import datetime

# Configuração
API_BASE_URL = "http://localhost:8000"
PAYMENT_ENDPOINT = f"{API_BASE_URL}/api/payment"
STATUS_ENDPOINT = f"{API_BASE_URL}/api/payment/status"

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}[OK] {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}[ERRO] {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.BLUE}[INFO] {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}[AVISO] {message}{Colors.RESET}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def test_server_health():
    """Testa se o servidor está rodando"""
    print_header("1. TESTANDO CONECTIVIDADE DO SERVIDOR")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"Servidor está rodando em {API_BASE_URL}")
            print_info(f"Resposta: {response.json()}")
            return True
        else:
            print_error(f"Servidor retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Não foi possível conectar ao servidor em {API_BASE_URL}")
        print_warning("Certifique-se de que o servidor está rodando:")
        print_warning("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print_error(f"Erro ao testar servidor: {str(e)}")
        return False

def test_payment_success():
    """Testa pagamento bem-sucedido"""
    print_header("2. TESTANDO PAGAMENTO BEM-SUCEDIDO")
    
    payment_data = {
        "amount": 450.00,
        "phone_number": "841234567",
        "order_reference": f"TEST-{int(time.time())}"
    }
    
    print_info(f"Enviando requisição: {json.dumps(payment_data, indent=2)}")
    
    try:
        response = requests.post(
            PAYMENT_ENDPOINT,
            json=payment_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print_info(f"Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Pagamento iniciado com sucesso!")
            print_info(f"Resposta: {json.dumps(data, indent=2, default=str)}")
            
            # Testar consulta de status
            if "transaction_id" in data:
                transaction_id = data["transaction_id"]
                print_info(f"\nConsultando status da transação: {transaction_id}")
                time.sleep(1)
                
                status_response = requests.get(
                    f"{STATUS_ENDPOINT}/{transaction_id}",
                    timeout=5
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print_success("Status consultado com sucesso!")
                    print_info(f"Status: {json.dumps(status_data, indent=2, default=str)}")
                else:
                    print_warning(f"Erro ao consultar status: {status_response.status_code}")
            
            return True
        else:
            print_error(f"Falha no pagamento. Status: {response.status_code}")
            print_error(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erro ao processar pagamento: {str(e)}")
        return False

def test_payment_validation():
    """Testa validações de pagamento"""
    print_header("3. TESTANDO VALIDAÇÕES")
    
    test_cases = [
        {
            "name": "Valor muito baixo",
            "data": {"amount": 0.5, "phone_number": "841234567", "order_reference": "TEST-1"},
            "expected_status": 400
        },
        {
            "name": "Número de telefone inválido",
            "data": {"amount": 450.00, "phone_number": "123456789", "order_reference": "TEST-2"},
            "expected_status": 400
        },
        {
            "name": "Número de telefone muito curto",
            "data": {"amount": 450.00, "phone_number": "84123", "order_reference": "TEST-3"},
            "expected_status": 422
        },
        {
            "name": "Dados válidos (deve passar)",
            "data": {"amount": 450.00, "phone_number": "841234567", "order_reference": "TEST-4"},
            "expected_status": 200
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        print_info(f"\nTeste: {test_case['name']}")
        print_info(f"Dados: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                PAYMENT_ENDPOINT,
                json=test_case['data'],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == test_case['expected_status']:
                print_success(f"Validação correta (Status: {response.status_code})")
                passed += 1
            else:
                print_error(f"Validação falhou. Esperado: {test_case['expected_status']}, Recebido: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print_error(f"Erro no teste: {str(e)}")
            failed += 1
    
    print_info(f"\nResultado: {passed} passou, {failed} falhou")
    return failed == 0

def test_multiple_payments():
    """Testa múltiplos pagamentos simultâneos"""
    print_header("4. TESTANDO MÚLTIPLOS PAGAMENTOS")
    
    payments = [
        {"amount": 250.00, "phone_number": "841111111", "order_reference": f"MULTI-1-{int(time.time())}"},
        {"amount": 350.00, "phone_number": "842222222", "order_reference": f"MULTI-2-{int(time.time())}"},
        {"amount": 450.00, "phone_number": "843333333", "order_reference": f"MULTI-3-{int(time.time())}"},
    ]
    
    print_info(f"Enviando {len(payments)} pagamentos simultâneos...")
    
    results = []
    for i, payment in enumerate(payments, 1):
        try:
            response = requests.post(
                PAYMENT_ENDPOINT,
                json=payment,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Pagamento {i} iniciado: {data.get('transaction_id')}")
                results.append(True)
            else:
                print_error(f"Pagamento {i} falhou: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print_error(f"Erro no pagamento {i}: {str(e)}")
            results.append(False)
    
    success_count = sum(results)
    print_info(f"\nResultado: {success_count}/{len(payments)} pagamentos bem-sucedidos")
    return success_count == len(payments)

def main():
    """Executa todos os testes"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}TESTE AUTOMATIZADO - API DE PAGAMENTO M-PESA{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    print_info(f"API Base URL: {API_BASE_URL}")
    print_info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # Teste 1: Conectividade
    results.append(("Conectividade", test_server_health()))
    
    if not results[0][1]:
        print_error("\nServidor não está acessível. Abortando testes.")
        return
    
    time.sleep(1)
    
    # Teste 2: Pagamento bem-sucedido
    results.append(("Pagamento Bem-Sucedido", test_payment_success()))
    
    time.sleep(1)
    
    # Teste 3: Validações
    results.append(("Validações", test_payment_validation()))
    
    time.sleep(1)
    
    # Teste 4: Múltiplos pagamentos
    results.append(("Múltiplos Pagamentos", test_multiple_payments()))
    
    # Resumo final
    print_header("RESUMO DOS TESTES")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    failed = total - passed
    
    for name, result in results:
        status_icon = "[OK]" if result else "[FALHOU]"
        status_color = Colors.GREEN if result else Colors.RED
        print(f"{status_color}{status_icon} {name}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} testes passaram{Colors.RESET}")
    
    if failed > 0:
        print_error(f"{failed} teste(s) falharam")
        return 1
    else:
        print_success("Todos os testes passaram!")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

