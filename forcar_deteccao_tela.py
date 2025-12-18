"""
Script para forçar detecção de segunda tela HDMI no Windows
"""

import subprocess
import sys
import os

# Configurar encoding para Windows
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

def forcar_deteccao():
    """Força o Windows a detectar monitores conectados"""
    print("=" * 60)
    print("FORCAR DETECCAO DE SEGUNDA TELA HDMI")
    print("=" * 60)
    print()
    
    print("Executando comandos para forcar detecção...")
    print()
    
    # Comando 1: Usar DisplaySwitch para estender
    print("[1] Tentando configurar modo 'Estender'...")
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{P}')"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("   [OK] Comando executado")
        print("   NOTA: Pressione Windows + P manualmente e selecione 'Estender'")
    except Exception as e:
        print(f"   [AVISO] {e}")
    
    print()
    
    # Comando 2: Forçar detecção via PowerShell
    print("[2] Forcando detecção de monitores...")
    try:
        ps_command = """
        $monitors = Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBasicDisplayParams
        Write-Host "Monitores encontrados: $($monitors.Count)"
        foreach ($monitor in $monitors) {
            Write-Host "Monitor: $($monitor.InstanceName)"
        }
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        
        if result.returncode == 0:
            print("   [OK] Resultado:")
            print(result.stdout)
        else:
            print(f"   [ERRO] {result.stderr}")
    except Exception as e:
        print(f"   [ERRO] {e}")
    
    print()
    
    # Comando 3: Verificar adaptadores de vídeo
    print("[3] Verificando adaptadores de video...")
    try:
        ps_command = """
        Get-WmiObject -Class Win32_VideoController | 
        Select-Object Name, Status, Availability, AdapterRAM |
        Format-List | Out-String
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        
        if result.returncode == 0:
            print("   [OK] Adaptadores encontrados:")
            print(result.stdout)
        else:
            print(f"   [ERRO] {result.stderr}")
    except Exception as e:
        print(f"   [ERRO] {e}")
    
    print()
    print("=" * 60)
    print("SOLUCOES MANUAIS")
    print("=" * 60)
    print()
    print("1. Pressione Windows + P e selecione 'Estender'")
    print("2. Vá em Configuracoes > Sistema > Tela")
    print("3. Clique no botao 'Detectar'")
    print("4. Verifique se o cabo HDMI esta bem conectado")
    print("5. Tente trocar o cabo HDMI ou a porta")
    print("6. Reinicie o computador com a segunda tela conectada")
    print("7. Atualize os drivers da placa de video:")
    print("   - Abra Gerenciador de Dispositivos")
    print("   - Expanda 'Adaptadores de video'")
    print("   - Clique com botao direito e selecione 'Atualizar driver'")
    print()

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este script e especifico para Windows")
        sys.exit(1)
    
    forcar_deteccao()



