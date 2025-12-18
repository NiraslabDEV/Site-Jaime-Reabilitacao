"""Script de teste para a API"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa o endpoint de health check"""
    print("[TESTE] Testando /health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"[OK] Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("[ERRO] Servidor nao esta rodando. Inicie com: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"[ERRO] {e}")
        return False

def test_root():
    """Testa o endpoint raiz"""
    print("\n[TESTE] Testando / (root)...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"[OK] Status: {response.status_code}")
        print(f"   Resposta: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"[ERRO] {e}")
        return False

def test_register():
    """Testa o registro de usuário"""
    print("\n[TESTE] Testando POST /auth/register...")
    try:
        data = {
            "email": f"teste_{int(time.time())}@example.com",
            "password": "teste123456"
        }
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=data,
            timeout=5
        )
        print(f"[OK] Status: {response.status_code}")
        result = response.json()
        print(f"   Token recebido: {result.get('access_token', 'N/A')[:50]}...")
        return result.get('access_token')
    except Exception as e:
        print(f"[ERRO] {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Resposta: {e.response.text}")
        return None

def test_login(email, password):
    """Testa o login"""
    print("\n[TESTE] Testando POST /auth/login...")
    try:
        data = {"email": email, "password": password}
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=data,
            timeout=5
        )
        print(f"[OK] Status: {response.status_code}")
        result = response.json()
        print(f"   Token recebido: {result.get('access_token', 'N/A')[:50]}...")
        return result.get('access_token')
    except Exception as e:
        print(f"[ERRO] {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Resposta: {e.response.text}")
        return None

def test_create_search(token):
    """Testa criar uma busca"""
    print("\n[TESTE] Testando POST /searches...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"url": "https://fastapi.tiangolo.com"}
        response = requests.post(
            f"{BASE_URL}/searches",
            json=data,
            headers=headers,
            timeout=5
        )
        print(f"[OK] Status: {response.status_code}")
        result = response.json()
        print(f"   Busca criada: ID={result.get('id')}, URL={result.get('url')}")
        return result.get('id')
    except Exception as e:
        print(f"[ERRO] {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Resposta: {e.response.text}")
        return None

def test_get_searches(token):
    """Testa listar buscas"""
    print("\n[TESTE] Testando GET /searches...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/searches",
            headers=headers,
            timeout=5
        )
        print(f"[OK] Status: {response.status_code}")
        result = response.json()
        print(f"   Total de buscas: {len(result)}")
        if result:
            print(f"   Primeira busca: {result[0].get('url')}")
        return True
    except Exception as e:
        print(f"[ERRO] {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Resposta: {e.response.text}")
        return False

def main():
    print("=" * 60)
    print("TESTE DA API - Technical Documentation Analyzer")
    print("=" * 60)
    
    # Teste 1: Health check
    if not test_health():
        sys.exit(1)
    
    # Teste 2: Root endpoint
    test_root()
    
    # Teste 3: Registrar usuário
    token = test_register()
    if not token:
        print("\n[AVISO] Nao foi possivel obter token. Verifique se o Supabase esta configurado.")
        return
    
    # Teste 4: Criar busca
    search_id = test_create_search(token)
    
    # Teste 5: Listar buscas
    test_get_searches(token)
    
    print("\n" + "=" * 60)
    print("[OK] Testes concluidos!")
    print("=" * 60)

if __name__ == "__main__":
    main()

