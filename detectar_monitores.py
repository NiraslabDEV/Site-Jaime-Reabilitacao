"""
Script para detectar monitores conectados no Windows
Ajuda a diagnosticar problemas com identificação de telas HDMI
"""

import sys
import subprocess
import json
import os

# Configurar encoding para Windows
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

def detectar_monitores_windows():
    """Detecta monitores usando PowerShell no Windows"""
    print("=" * 60)
    print("DETECÇÃO DE MONITORES - WINDOWS")
    print("=" * 60)
    print()
    
    try:
        # Comando PowerShell para listar monitores
        ps_command = """
        Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBasicDisplayParams | 
        Select-Object InstanceName, MaxHorizontalImageSize, MaxVerticalImageSize |
        ConvertTo-Json
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                monitores = json.loads(result.stdout)
                if not isinstance(monitores, list):
                    monitores = [monitores]
                
                print(f"[OK] Encontrados {len(monitores)} monitor(es):\n")
                for i, monitor in enumerate(monitores, 1):
                    print(f"Monitor {i}:")
                    print(f"  Nome: {monitor.get('InstanceName', 'N/A')}")
                    print(f"  Resolução Máxima: {monitor.get('MaxHorizontalImageSize', 'N/A')} x {monitor.get('MaxVerticalImageSize', 'N/A')}")
                    print()
            except json.JSONDecodeError:
                print("[AVISO] Erro ao processar dados dos monitores")
                print("Saída do PowerShell:")
                print(result.stdout)
        else:
            print("[AVISO] Nenhum monitor detectado ou erro ao executar comando")
            if result.stderr:
                print(f"Erro: {result.stderr}")
    
    except Exception as e:
        print(f"[ERRO] Erro ao executar detecção: {e}")
    
    # Método alternativo usando DisplayConfig
    print("\n" + "=" * 60)
    print("MÉTODO ALTERNATIVO - DisplayConfig")
    print("=" * 60)
    print()
    
    try:
        ps_command2 = """
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class DisplayHelper {
            [DllImport("user32.dll")]
            public static extern int GetSystemMetrics(int nIndex);
            public static int GetMonitorCount() {
                return GetSystemMetrics(80); // SM_CMONITORS
            }
        }
"@
        [DisplayHelper]::GetMonitorCount()
        """
        
        result2 = subprocess.run(
            ["powershell", "-Command", ps_command2],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result2.returncode == 0:
            count = result2.stdout.strip()
            print(f"[OK] Número de monitores detectados pelo sistema: {count}")
        else:
            print("[AVISO] Não foi possível obter contagem de monitores")
    
    except Exception as e:
        print(f"[ERRO] Erro no método alternativo: {e}")
    
    # Verificar configurações de display
    print("\n" + "=" * 60)
    print("CONFIGURAÇÕES DE DISPLAY")
    print("=" * 60)
    print()
    
    try:
        ps_command3 = """
        Get-WmiObject -Class Win32_VideoController | 
        Select-Object Name, CurrentHorizontalResolution, CurrentVerticalResolution, VideoModeDescription |
        Format-List | Out-String
        """
        
        result3 = subprocess.run(
            ["powershell", "-Command", ps_command3],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result3.returncode == 0:
            print(result3.stdout)
        else:
            print("[AVISO] Não foi possível obter configurações de vídeo")
    
    except Exception as e:
        print(f"[ERRO] Erro ao obter configurações: {e}")
    
    print("\n" + "=" * 60)
    print("DICAS PARA RESOLVER PROBLEMAS")
    print("=" * 60)
    print()
    print("1. Verifique se o cabo HDMI está bem conectado")
    print("2. Tente desconectar e reconectar o cabo HDMI")
    print("3. Pressione Windows + P e selecione 'Estender' ou 'Duplicar'")
    print("4. Verifique as configurações de display:")
    print("   - Clique com botão direito na área de trabalho")
    print("   - Selecione 'Configurações de exibição'")
    print("   - Clique em 'Detectar'")
    print("5. Atualize os drivers da placa de vídeo")
    print("6. Reinicie o computador")
    print()

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este script é específico para Windows")
        sys.exit(1)
    
    detectar_monitores_windows()

