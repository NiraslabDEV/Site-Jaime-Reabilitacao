"""
Script para testar integração real com API M-Pesa
Execute: python test_mpesa_real.py
"""
import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se API Key está configurada
mpesa_api_key = os.getenv("MPESA_API_KEY")

if not mpesa_api_key:
    print("❌ ERRO: MPESA_API_KEY não configurada!")
    print("\nConfigure no arquivo .env:")
    print("MPESA_API_KEY=HeceKhPwJLOuAr4D00hMpNlcAghmkLEG")
    print("MPESA_API_URL=https://api.mpesa.com")
    print("MPESA_ENVIRONMENT=sandbox")
    sys.exit(1)

print("✅ API Key encontrada!")
print(f"   Key: {mpesa_api_key[:10]}...{mpesa_api_key[-10:]}")
print(f"   Environment: {os.getenv('MPESA_ENVIRONMENT', 'sandbox')}")
print(f"   API URL: {os.getenv('MPESA_API_URL', 'https://api.mpesa.com')}")
print("\n" + "="*60)
print("TESTE DE INTEGRAÇÃO REAL M-PESA")
print("="*60 + "\n")

# Importar após verificar configuração
import asyncio
from app.core.mpesa_client import MpesaClient
from app.core.config import settings

async def test_authentication():
    """Testa autenticação com API M-Pesa"""
    print("1. Testando autenticação...")
    try:
        token = await MpesaClient.get_access_token()
        if token:
            print(f"   ✅ Token obtido com sucesso!")
            print(f"   Token: {token[:20]}...{token[-10:]}")
            return True
        else:
            print("   ❌ Token não retornado")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

async def test_payment_link():
    """Testa criação de link de pagamento"""
    print("\n2. Testando criação de link de pagamento...")
    try:
        response = await MpesaClient.initiate_payment_link(
            phone_number="258841234567",
            amount=10.00,  # Valor mínimo para teste
            order_reference="TEST-REAL-001",
            description="Teste de integração real"
        )
        print(f"   ✅ Link criado com sucesso!")
        print(f"   Resposta: {response}")
        return True
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        print(f"   Detalhes: {type(e).__name__}")
        return False

async def main():
    """Executa todos os testes"""
    results = []
    
    # Teste 1: Autenticação
    results.append(("Autenticação", await test_authentication()))
    
    # Teste 2: Criação de pagamento (apenas se autenticação passou)
    if results[0][1]:
        results.append(("Criação de Link", await test_payment_link()))
    else:
        print("\n⚠️  Pulando teste de pagamento (autenticação falhou)")
        results.append(("Criação de Link", False))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! Integração funcionando.")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique:")
        print("   1. URL da API está correta?")
        print("   2. Método de autenticação está correto?")
        print("   3. API Key é válida?")
        print("   4. Endpoints estão corretos?")
        print("\n   Consulte INTEGRACAO_MPESA.md para mais detalhes.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)





