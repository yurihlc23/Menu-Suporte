import time
import subprocess
import psutil
import os

# Caminhos dos executáveis
caminho_gp = r"C:\Gplus\GpToGo.exe"
nome_frente = "FrenteCaixa.exe"

def frente_rodando():
    """Verifica se FrenteCaixa.exe está rodando."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == nome_frente:
            return True
    return False

def iniciar_gp():
    """Inicia GpToGo.exe se ainda não estiver rodando."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "GpToGo.exe":
            return  # Já está rodando
    subprocess.Popen(caminho_gp)
    print("GpToGo.exe iniciado.")

if __name__ == "__main__":
    print("Monitor de FrenteCaixa iniciado.")
    while True:
        if frente_rodando():
            iniciar_gp()
        time.sleep(5)  # Verifica a cada 5 segundos
