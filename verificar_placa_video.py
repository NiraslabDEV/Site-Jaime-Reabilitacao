"""
Script para identificar a placa de video e verificar drivers
"""

import subprocess
import sys
import os

# Configurar encoding para Windows
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

def verificar_placa_video():
    """Identifica a placa de video instalada"""
    print("=" * 60)
    print("VERIFICACAO DE PLACA DE VIDEO")
    print("=" * 60)
    print()
    
    print("[INFO] Verificando informacoes da placa de video...")
    print()
    
    # Obter informações detalhadas da placa de vídeo
    ps_command = """
    $adapters = Get-WmiObject -Class Win32_VideoController
    foreach ($adapter in $adapters) {
        Write-Host "=== ADAPTADOR DE VIDEO ==="
        Write-Host "Nome: $($adapter.Name)"
        Write-Host "Fabricante: $($adapter.Manufacturer)"
        Write-Host "Descricao: $($adapter.Description)"
        Write-Host "Status: $($adapter.Status)"
        Write-Host "Driver Version: $($adapter.DriverVersion)"
        Write-Host "Driver Date: $($adapter.DriverDate)"
        Write-Host "PNP Device ID: $($adapter.PNPDeviceID)"
        Write-Host "Video Processor: $($adapter.VideoProcessor)"
        Write-Host "Adapter RAM: $([math]::Round($adapter.AdapterRAM / 1GB, 2)) GB"
        Write-Host ""
    }
    """
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=15
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"[ERRO] {result.stderr}")
    except Exception as e:
        print(f"[ERRO] {e}")
    
    print()
    print("=" * 60)
    print("DIAGNOSTICO")
    print("=" * 60)
    print()
    
    # Verificar se está usando driver genérico
    ps_command2 = """
    $adapters = Get-WmiObject -Class Win32_VideoController
    $isGeneric = $false
    foreach ($adapter in $adapters) {
        if ($adapter.Name -like "*Basic Display*" -or $adapter.Name -like "*Standard*") {
            $isGeneric = $true
            break
        }
    }
    if ($isGeneric) {
        Write-Host "PROBLEMA DETECTADO: Driver generico do Windows em uso"
        Write-Host "Isso impede a deteccao de multiplos monitores"
    } else {
        Write-Host "OK: Driver especifico da placa de video detectado"
    }
    """
    
    try:
        result2 = subprocess.run(
            ["powershell", "-Command", ps_command2],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        
        if result2.returncode == 0:
            print(result2.stdout)
    except Exception as e:
        print(f"[ERRO] {e}")
    
    print()
    print("=" * 60)
    print("SOLUCOES")
    print("=" * 60)
    print()
    print("Se voce esta usando 'Microsoft Basic Display Adapter':")
    print()
    print("1. IDENTIFICAR SUA PLACA DE VIDEO:")
    print("   - Abra Gerenciador de Dispositivos (Win + X > Gerenciador)")
    print("   - Expanda 'Adaptadores de video'")
    print("   - Anote o nome exato da placa")
    print()
    print("2. INSTALAR DRIVERS CORRETOS:")
    print("   - NVIDIA: https://www.nvidia.com/drivers")
    print("   - AMD: https://www.amd.com/support")
    print("   - Intel: https://www.intel.com/content/www/us/en/download-center/home.html")
    print()
    print("3. ALTERNATIVA - Atualizar via Windows Update:")
    print("   - Configuracoes > Atualizacao e Seguranca")
    print("   - Verificar atualizacoes")
    print("   - Procurar atualizacoes opcionais")
    print()
    print("4. DEPOIS DE INSTALAR OS DRIVERS:")
    print("   - Reinicie o computador")
    print("   - Conecte a segunda tela HDMI")
    print("   - Pressione Windows + P")
    print("   - Selecione 'Estender'")
    print("   - Ou va em Configuracoes > Sistema > Tela > Detectar")
    print()

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este script e especifico para Windows")
        sys.exit(1)
    
    verificar_placa_video()



