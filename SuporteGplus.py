import flet as ft
import requests 
import tkinter as tk
import tempfile
import subprocess
import os
import ctypes
import socket
import win32print
import win32api
from colorama import init, Fore, Style
from tkinter import messagebox, simpledialog
from tkinter import messagebox
from datetime import datetime
from bs4 import BeautifulSoup

def is_admin(e):
    """Verifica se o script está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# NOVO: Verificar ambiente GPlus direto no terminal (sem gerar .bat)
def verificar_gplus(e):
    import os

    script_path = os.path.join(os.path.dirname(__file__), "verificar_gplus_temp.py")

    with open(script_path, "w", encoding="utf-8") as f:
        f.write("""
import os
import subprocess
import shutil
from colorama import init, Fore

init(autoreset=True)

print(Fore.GREEN + '-' * 42)
print(Fore.GREEN + '         VERIFICAÇÃO DO GPLUS')
print(Fore.GREEN + '    serviços, arquivos e processos')
print(Fore.GREEN + '-' * 42)

caminhoExe = r'C:\\Gplus'
origem_fbclient = os.path.join(caminhoExe, 'fbclient.dll')

servicos = [
    "GplusApi", "GplusPromocao", "GplusBackup", "GplusEstoque", "FirebirdServerDefaultInstance"
]

executaveis = [
    "uploadCashierOpening.exe", "uploadCashierClosing.exe", "uploadSale.exe", "GplusTaskManager.exe",
    "ApiKDS.exe", "ibexpert.exe", "GplusApi.exe", "oPlus.exe", "GplusPromocao.exe",
    "BackupGplusAutomatico.exe", "MonitorGplus.exe", "GpIfood.exe", "GplusDocFisco.exe",
    "IntegradorDocFisco.exe", "Retaguarda.exe", "Gplus.exe", "FrenteCaixa.exe", "Boleto.exe",
    "AgendaGplus.exe", "GplusServidor.exe", "Configurador.exe", "ConfiguradorGpOmie.exe",
    "AgruparPedidosOmie.exe", "GeradorEtiqueta.exe", "EmissorFiscal.exe", "GpOmie.exe",
    "Impressor.exe", "MicroTerminal.exe", "NFe.exe", "OS.exe", "Recebimento.exe",
    "ServidorMobile.exe", "ApiInfinite.exe", "Terminal.exe", "GpToGo.exe", "GplusImagens.exe",
    "Integrador.exe", "eventConduit.exe", "ValidateFirebird1.0.exe", "AtualizarDocFisco2.0.exe",
    "BaixarEstoque2.0.exe", "DocFisco2.0.exe", "GeradorJson.exe", "LicenseManager1.0.exe",
    "LimpezaDados1.0.exe", "StatusXML2.0.exe", "UploadFechamentos2.0.exe", "UploadVendas2.0.exe"
]

executaveis_criticos = [
    "GplusTaskManager.exe", "ApiKDS.exe", "ApiInfinite.exe", "EmissorFiscal.exe",
    "GplusServidor.exe", "GpToGo.exe", "GpIfood.exe", "Impressor.exe", "Integrador.exe"
]

pastas_fbclient = [r"C:\\Windows\\System32", r"C:\\Windows\\SysWOW64"]
faltando_servicos = []
faltando_arquivos = []
processos_nao_rodando = []
faltando_fbclient = []
processos_criticos_parados = []

print('\\n' + Fore.CYAN + 'Verificando SERVIÇOS...')
for srv in servicos:
    result = subprocess.run(["sc", "query", srv], capture_output=True, text=True)
    if "FAILED" in result.stdout or "1060" in result.stdout:
        print(Fore.RED + f"[FALTANDO] Serviço: {srv}")
        faltando_servicos.append(srv)
    else:
        print(Fore.GREEN + f"[OK] Serviço: {srv} encontrado")

print('\\n' + Fore.CYAN + f"Verificando ARQUIVOS .exe em {caminhoExe}...")
for exe in executaveis:
    if os.path.exists(os.path.join(caminhoExe, exe)):
        print(Fore.GREEN + f"[OK] Arquivo: {exe} encontrado")
    else:
        print(Fore.RED + f"[FALTANDO] Arquivo: {exe}")
        faltando_arquivos.append(exe)

print('\\n' + Fore.CYAN + "Verificando PROCESSOS EM EXECUÇÃO...")
for exe in executaveis:
    result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {exe}"], capture_output=True, text=True)
    if exe.lower() in result.stdout.lower():
        print(Fore.GREEN + f"[OK] Processo rodando: {exe}")
    else:
        print(Fore.YELLOW + f"[NÃO RODANDO] Processo: {exe}")
        processos_nao_rodando.append(exe)

print('\\n' + Fore.CYAN + "Verificando EXISTÊNCIA DO fbclient.dll...")
for pasta in pastas_fbclient:
    dll_path = os.path.join(pasta, "fbclient.dll")
    if os.path.exists(dll_path):
        print(Fore.GREEN + f"[OK] fbclient.dll encontrado em {pasta}")
    else:
        print(Fore.RED + f"[FALTANDO] fbclient.dll em {pasta}")
        faltando_fbclient.append(pasta)
        # Tenta copiar o arquivo
        if os.path.exists(origem_fbclient):
            try:
                shutil.copy2(origem_fbclient, dll_path)
                print(Fore.YELLOW + f"[COPIADO] fbclient.dll copiado para {pasta}")
            except Exception as e:
                print(Fore.RED + f"[ERRO] Falha ao copiar para {pasta}: {str(e)}")
        else:
            print(Fore.RED + "[ERRO] fbclient.dll de origem não encontrado em C:\\Gplus")

print('\\n' + Fore.CYAN + '-' * 42)
print(Fore.CYAN + '     VERIFICAÇÃO DE PROCESSOS CRÍTICOS')
print(Fore.CYAN + '-' * 42)

# Verificar se Firebird está em execução
firebird_em_execucao = True
result_fb = subprocess.run(["sc", "query", "FirebirdServerDefaultInstance"], capture_output=True, text=True)
if "RUNNING" in result_fb.stdout:
    print(Fore.GREEN + "[OK] Serviço FirebirdServerDefaultInstance está em execução.")
else:
    print(Fore.RED + "[ALERTA] Serviço FirebirdServerDefaultInstance NÃO está rodando.")
    firebird_em_execucao = False
    processos_criticos_parados.append("SERVIÇO: FirebirdServerDefaultInstance")

# Verificar processos críticos .exe
for exe in executaveis_criticos:
    result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {exe}"], capture_output=True, text=True)
    if exe.lower() in result.stdout.lower():
        print(Fore.GREEN + f"[OK] {exe} em execução.")
    else:
        print(Fore.RED + f"[ALERTA] {exe} NÃO está rodando.")
        processos_criticos_parados.append(exe)


# Perguntar se deseja iniciar processos críticos parados
if processos_criticos_parados:
    resposta = input(Fore.MAGENTA + "\\nDeseja inicializar os processos críticos que não estão rodando (incluindo Firebird)? (s/n): ").strip().lower()
    if resposta == 's':
        for proc in processos_criticos_parados:
            if proc.startswith("SERVIÇO:"):
                servico = proc.split("SERVIÇO:")[1].strip()
                print(Fore.CYAN + f"Iniciando serviço: {servico}...")
                result = subprocess.call(f"net start {servico}", shell=True)
                if result == 0:
                    print(Fore.GREEN + f"[INICIADO] Serviço {servico} iniciado com sucesso.")
                else:
                    print(Fore.RED + f"[ERRO] Falha ao iniciar serviço {servico}. Verifique permissões.")
            else:
                caminho_exe = os.path.join(caminhoExe, proc)
                if os.path.exists(caminho_exe):
                    try:
                        subprocess.Popen(caminho_exe)
                        print(Fore.GREEN + f"[INICIADO] Processo crítico {proc} iniciado.")
                    except Exception as e:
                        print(Fore.RED + f"[ERRO] Falha ao iniciar {proc}: {str(e)}")
                else:
                    print(Fore.RED + f"[ERRO] Executável {proc} não encontrado em {caminhoExe}.")

else:
    print(Fore.GREEN + "Todos os processos críticos estão em execução.")

print('\\n' + Fore.MAGENTA + '-' * 42)
print(Fore.MAGENTA + '           RELATÓRIO FINAL')
print(Fore.MAGENTA + '-' * 42)

if faltando_servicos:
    print(Fore.RED + "Serviços faltando:")
    for s in faltando_servicos:
        print(f" - {s}")
else:
    print(Fore.GREEN + "Todos os serviços foram encontrados.")

if faltando_arquivos:
    print(Fore.RED + "\\nArquivos .exe faltando:")
    for a in faltando_arquivos:
        print(f" - {a}")
else:
    print(Fore.GREEN + f"Todos os arquivos .exe estão presentes em {caminhoExe}.")

if processos_nao_rodando:
    print(Fore.YELLOW + "\\nProcessos que NÃO estão rodando:")
    for p in processos_nao_rodando:
        print(f" - {p}")
else:
    print(Fore.GREEN + "Todos os processos estão em execução.")

if processos_criticos_parados:
    print(Fore.RED + "\\nALERTA: Processos críticos NÃO estão rodando:")
    for c in processos_criticos_parados:
        print(f" - {c}")

if faltando_fbclient:
    print(Fore.YELLOW + "\\nfbclient.dll estava faltando e foi copiado (se possível).")
else:
    print(Fore.GREEN + "fbclient.dll encontrado em todas as pastas.")

input("\\nPressione ENTER para sair...")
""")

    os.system(f'start cmd /k python "{script_path}"')


# Outras funções do sistema
def executar_comando(comando):
    os.system(f'start cmd /k "{comando}"')
    resultado = subprocess.getoutput(comando)
    messagebox.showinfo("Resultado", resultado)

def reiniciar(e):
    os.system('start cmd /k "shutdown /r /t 0"')

def lentidao(e):
    os.system('start cmd /k "sfc /scannow"')
    resultado = subprocess.getoutput("sfc /scannow")
    messagebox.showinfo("Lentidão", f"Verificação SFC executada.\nResultado:\n{resultado}\n\nLembre-se de limpar arquivos temporários manualmente se necessário.")

def flush_dns(e):
    executar_comando("ipconfig /flushdns")

def checklist_rede(e):
    executar_comando("ipconfig /all")

def obter_ip_local_real():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
    except Exception:
        ip_local = "IP local não identificado"
    return ip_local

def ping_servidor(e):
    ip_local = obter_ip_local_real()
    alvo = simpledialog.askstring("Ping", f"Seu IP local: {ip_local}\n\nDigite o IP ou nome do servidor para testar:")
    if alvo:
        executar_comando(f"echo Seu IP local: {ip_local} && ping {alvo}")

def erro_11b(e):
    os.system('start cmd /k reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled /t REG_DWORD /d 0 /f')
    resultado = subprocess.getoutput('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled')
    messagebox.showinfo("Erro 0x0000011b", f"Corrigido com sucesso!\n\n{resultado}")

def erro_0bcb(e):
    os.system('start cmd /k reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Printers\\PointAndPrint" /v RestrictDriverInstallationToAdministrators /t REG_DWORD /d 0 /f')
    resultado = subprocess.getoutput('reg query "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Printers\\PointAndPrint" /v RestrictDriverInstallationToAdministrators')
    messagebox.showinfo("Erro 0x00000bcb", f"Corrigido com sucesso!\n\n{resultado}")

def erro_709(e):
    os.system('start cmd /k reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Printers\\RPC" /v RpcUseNamedPipeProtocol /t REG_DWORD /d 1 /f')
    resultado = subprocess.getoutput('reg query "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Printers\\RPC" /v RpcUseNamedPipeProtocol')
    messagebox.showinfo("Erro 0x00000709", f"Corrigido com sucesso!\n\n{resultado}")

def spooler(e):
    os.system('start cmd /k "net stop spooler && net start spooler"')
    resultado = subprocess.getoutput("sc query spooler")
    messagebox.showinfo("Spooler", f"Spooler reiniciado com sucesso.\n\n{resultado}")

def verificar_conexao(e):
    os.system('start cmd /k "ping www.google.com -n 2"')
    response = os.system("ping www.google.com -n 2 >nul")
    if response == 0:
        messagebox.showinfo("Conectividade", "Conectado à internet.")
    else:
        messagebox.showwarning("Conectividade", "Sem conexão com a internet.")

def verificar_antivirus(e):
    os.system('start cmd /k "wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName /value"')
    resultado = subprocess.getoutput('wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName /value')
    if "DisplayName" in resultado:
        messagebox.showinfo("Antivírus", resultado)
    else:
        messagebox.showwarning("Antivírus", "Nenhum antivírus detectado pelo Windows.")

def verificar_sat(e):
    try:
        resultado = subprocess.check_output("sc query ecosat", shell=True, text=True)
        if "RUNNING" in resultado:
            messagebox.showinfo("SAT Fiscal", "O serviço do SAT está ativo e em execução.")
        else:
            messagebox.showwarning("SAT Fiscal", "O SAT não está em execução.\nVerifique a conexão e tente novamente.")
    except subprocess.CalledProcessError:
        messagebox.showerror(
            "SAT não encontrado",
            "O serviço do SAT não foi localizado.\n\nVerifique se o SAT está conectado ao computador.\n"
            "Caso esteja, tente desconectar e conectar novamente."
        )

def verificar_shipay_status(e=None):
    import requests
    import tkinter as tk
    from tkinter import messagebox

    def consultar_componentes():
        try:
            url = "https://shipay.instatus.com/v2/components.json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("components", [])
            else:
                messagebox.showwarning("Erro", f"Erro HTTP {response.status_code} ao consultar o status da Shipay.")
                return []
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao acessar o status da Shipay:\n{str(ex)}")
            return []

    def exibir_componentes():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        componentes = consultar_componentes()
        if not componentes:
            return

        status_legenda = {
            "OPERATIONAL": "Operacional",
            "DEGRADED_PERFORMANCE": "Desempenho Degradado",
            "PARTIAL_OUTAGE": "Falha Parcial",
            "MAJOR_OUTAGE": "Fora do Ar"
        }

        status_cores_bg = {
            "OPERATIONAL": "#c8f7c5",     # verde claro
            "MAJOR_OUTAGE": "#f7c5c5",     # vermelho claro
            "PARTIAL_OUTAGE": "#f7e3b5",   # amarelo claro
            "DEGRADED_PERFORMANCE": "#f7e3b5",  # amarelo claro
        }

        status_cores_fg = {
            "OPERATIONAL": "green",
            "MAJOR_OUTAGE": "red",
            "PARTIAL_OUTAGE": "orange",
            "DEGRADED_PERFORMANCE": "orange"
        }

        for comp in componentes:
            grupo = comp.get("group")
            grupo_nome = grupo.get("name") if grupo else comp.get("name", "Desconhecido")
            status_raw = comp.get("status", "UNKNOWN").upper()
            status_traduzido = status_legenda.get(status_raw, status_raw)

            cor_bg = status_cores_bg.get(status_raw, "#e0e0e0")
            cor_fg = status_cores_fg.get(status_raw, "black")

            linha_frame = tk.Frame(scrollable_frame, bg="white")
            linha_frame.pack(fill="x", pady=2)

            tk.Label(linha_frame,
                     text=f"{grupo_nome}: ",
                     font=("Arial", 12),
                     bg="white",
                     anchor="w").pack(side="left")

            tk.Label(linha_frame,
                     text=status_traduzido,
                     font=("Arial", 12, "bold"),
                     fg=cor_fg,
                     bg=cor_bg,
                     padx=5,
                     pady=2).pack(side="left")

    # Janela principal
    janela = tk.Tk()
    janela.title("Status Shipay")
    janela.geometry("600x800")
    janela.configure(bg="white")

    tk.Label(janela, text="📡 Status das Operações Shipay", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Frame com rolagem
    frame_container = tk.Frame(janela)
    frame_container.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(frame_container, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botões
    botoes_frame = tk.Frame(janela, bg="white")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="🔄 Atualizar Status", command=exibir_componentes).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="❌ Fechar", command=janela.destroy).pack(side="left", padx=5)

    # Primeira exibição
    exibir_componentes()

    janela.mainloop()


def verificar_certificado(e):
    script_path = os.path.join(os.path.dirname(__file__), "verificar_certificado_temp.bat")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write("""@echo off
        echo ------------------------------------------
        echo VERIFICANDO CERTIFICADO DIGITAL...
        echo ------------------------------------------
        certutil -store my
        echo.
        echo Tentando acessar SEFAZ via curl (se instalado)...
        where curl >nul 2>&1
        if %errorlevel%==0 (
            curl -v https://www.nfe.fazenda.sp.gov.br >nul 2>&1 && echo Conexao com SEFAZ ok. || echo Falha ao conectar SEFAZ.
        ) else (
            echo [AVISO] curl nao instalado.
        )
        pause
        """)
    os.system(f'start cmd /k "{script_path}"')

    repetir = messagebox.askyesno("Repetir Verificação", "Deseja verificar o certificado novamente?")
    if repetir:
        verificar_certificado()


def verificar_impressora(e):
    try:
        # Lista as impressoras
        impressoras = [printer[2] for printer in win32print.EnumPrinters(2)]
        if not impressoras:
            messagebox.showwarning("Impressoras", "Nenhuma impressora encontrada.")
            return

        escolha = simpledialog.askstring(
            "Escolher Impressora",
            "Escolha uma impressora:\n\n" + "\n".join(f"{i+1}. {nome}" for i, nome in enumerate(impressoras))
        )

        if not escolha:
            return

        try:
            indice = int(escolha) - 1
            if indice < 0 or indice >= len(impressoras):
                messagebox.showerror("Erro", "Número inválido.")
                return
            nome_impressora = impressoras[indice]
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido.")
            return

        # Criar conteúdo do teste
        conteudo = (
            "******** Página de Teste Python ********\n\n"
            f"Impressora: {nome_impressora}\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            "----------------------------------------\n"
            "Se você está vendo esta página, a impressora está funcionando.\n"
        )

        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(conteudo)
            caminho_arquivo = temp_file.name

        # Abrir impressora e criar job manualmente
        handle = win32print.OpenPrinter(nome_impressora)
        try:
            hJob = win32print.StartDocPrinter(handle, 1, ("Pagina de Teste Python", None, "RAW"))
            win32print.StartPagePrinter(handle)

            with open(caminho_arquivo, "rb") as f:
                win32print.WritePrinter(handle, f.read())

            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)

            messagebox.showinfo("Sucesso", f"Página de teste enviada com sucesso para: {nome_impressora}")

        finally:
            win32print.ClosePrinter(handle)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao imprimir.\n\nVerifique:\n- Conexão da impressora\n- Drivers\n\nErro:\n{e}")


def verificar_integrador(e=None):
    import subprocess
    import os
    from tkinter import messagebox
    
    exes_criticos = ["GpIfood.exe", "Integrador.exe", "GpToGo.exe"]
    caminho_gplus = r"C:\Gplus"
    processos_travados = []
    processos_nao_rodando = []
    
    # Verificação dos processos
    for exe in exes_criticos:
        try:
            # Verifica se o processo está rodando (usando codificação 'latin-1' para evitar problemas)
            output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {exe}"', shell=True).decode('latin-1')
            if exe.lower() in output.lower():
                # Verifica se está respondendo
                try:
                    pid_output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {exe}" /NH /FO CSV', shell=True).decode('latin-1')
                    pid = pid_output.split(',')[1].strip('"')
                    subprocess.check_output(f'tasklist /FI "PID eq {pid}" /FI "STATUS eq RUNNING"', shell=True).decode('latin-1')
                except:
                    processos_travados.append(exe)
            else:
                processos_nao_rodando.append(exe)
        except subprocess.CalledProcessError:
            processos_nao_rodando.append(exe)

    # Se houver processos problemáticos, perguntar se deseja reiniciar
    if processos_travados or processos_nao_rodando:
        mensagem = "Os seguintes processos precisam de atenção:\n\n"
        mensagem += "\n".join([f"- {exe} (Travado)" for exe in processos_travados])
        mensagem += "\n" if processos_travados else ""
        mensagem += "\n".join([f"- {exe} (Não está rodando)" for exe in processos_nao_rodando])
        mensagem += "\n\nDeseja reiniciar estes processos?"
        
        resposta = messagebox.askyesno("Processos Críticos", mensagem)
        
        if resposta:
            for exe in processos_travados + processos_nao_rodando:
                try:
                    # Tenta encerrar o processo se estiver travado
                    if exe in processos_travados:
                        subprocess.call(f'taskkill /f /im "{exe}"', shell=True)
                    
                    # Inicia o processo novamente
                    caminho_exe = os.path.join(caminho_gplus, exe)
                    subprocess.Popen(caminho_exe)
                    messagebox.showinfo("Sucesso", f"{exe} reiniciado com sucesso!")
                except Exception as err:
                    messagebox.showerror("Erro", f"Falha ao reiniciar {exe}:\n{str(err)}")
    else:
        messagebox.showinfo("Status", "Todos os processos críticos estão rodando normalmente.")
                              
                                      

def encerrar_processos_gplus(e):
    import os
    import subprocess
    import tempfile

    script_path = os.path.join(tempfile.gettempdir(), "encerrar_processos_gplus_temp.py")

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(r'''
import os
import subprocess
from colorama import init, Fore

init(autoreset=True)

print(Fore.RED + '-' * 50)
print(Fore.RED + '      ENCERRANDO PROCESSOS DO GPLUS')
print(Fore.RED + '-' * 50)

pasta_gplus = r"C:\Gplus"

if not os.path.exists(pasta_gplus):
    print(Fore.RED + "Erro: A pasta C:\\Gplus não foi encontrada.")
    input("Pressione ENTER para sair...")
    exit()

exes = [f for f in os.listdir(pasta_gplus) if f.endswith(".exe")]
processos_finalizados = []

if not exes:
    print(Fore.YELLOW + "Nenhum arquivo .exe encontrado na pasta C:\\Gplus.")
else:
    for exe in exes:
        nome_processo = exe
        result = subprocess.call(f'taskkill /f /im "{nome_processo}" >nul 2>&1', shell=True)
        if result == 0:
            print(Fore.GREEN + f"[FINALIZADO] {nome_processo}")
            processos_finalizados.append(nome_processo)
        else:
            print(Fore.YELLOW + f"[IGNORADO] {nome_processo} não estava em execução ou não pôde ser encerrado.")

if processos_finalizados:
    print(Fore.GREEN + f"Total de processos encerrados: {len(processos_finalizados)}")
else:
    print(Fore.YELLOW + "Nenhum processo foi encerrado.")

# Pergunta se deseja parar o serviço Firebird
resposta = input(Fore.CYAN + "\\nDeseja parar o serviço Firebird? (s/n): ").strip().lower()
if resposta == 's':
    result = subprocess.call("net stop FirebirdServerDefaultInstance", shell=True)
    if result == 0:
        print(Fore.GREEN + "Serviço Firebird parado com sucesso.")
    else:
        print(Fore.RED + "Erro ao parar o serviço Firebird. Verifique permissões de administrador.")

input("\\nPressione ENTER para sair...")
''')

    # Abre o console executando o script temporário
    os.system(f'start cmd /k python "{script_path}"')


def criar_grupo(titulo, botoes):
    widgets = [ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD)]
    for texto, funcao, descricao in botoes:
        widgets.append(
            ft.ElevatedButton(
                text=texto,
                on_click=funcao,
                tooltip=descricao,
                style=ft.ButtonStyle(
                    padding=20,
                    bgcolor= "#FF7B00",     # Cor de fundo laranja
                    color= "white"         # Cor do texto branca
                ),
                width=420
            )
        )
    return ft.Column(widgets, spacing=10)

def main(page: ft.Page):
    page.title = "Menu do Suporte GPLUS"
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 1000
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Título principal centralizado
    titulo_principal = ft.Container(
        content=ft.Text(
            "SUPORTE GPLUS SISTEMAS",
            size=35,
            weight=ft.FontWeight.BOLD,
            color="#FF7B00",
        ),
        alignment=ft.alignment.center,
        width=page.window_width,
    )
    
    # Definir os grupos
    grupos = [
        criar_grupo("🖥️  Computador", [
            ("🔁  Reiniciar Computador", reiniciar, "Reinicia o computador imediatamente."),
            ("🐢  Verificar Lentidão", lentidao, "Executa verificação SFC para detectar arquivos corrompidos."),
            ("🛡️ Verificar Antivírus Instalado", verificar_antivirus, "Mostra o antivírus detectado pelo Windows."),
            ("🌐  Flush DNS", flush_dns, "Limpa o cache DNS do sistema.")
        ]),

        criar_grupo("🌐  Rede", [
            ("📋  Checklist de Rede", checklist_rede, "Mostra detalhes da configuração de rede."),
            ("📶  Ping Servidor", ping_servidor, "Faz ping para um IP ou hostname informado."),
            ("📡  Verificar Internet", verificar_conexao, "Verifica a conexão com a internet.")
        ]),

        criar_grupo("📦  Fiscal", [
            ("📦  Verificar SAT", verificar_sat, "Verifica se o SAT está conectado e comunicando com SEFAZ."),
            ("🔐  Verificar Certificado Digital", verificar_certificado, "Verifica validade e comunicação do certificado digital.")
        ]),

        criar_grupo("🖨️  Impressora", [
            ("🖨️ Verificar Impressora", verificar_impressora, "Lista impressoras instaladas e conectadas."),
            ("🛠️ Corrigir erro 0x0000011b", erro_11b, "Corrige erro de impressão em rede (0x0000011b)."),
            ("🛠️ Corrigir erro 0x00000bcb", erro_0bcb, "Corrige erro de impressão (0x00000bcb)."),
            ("🛠️ Corrigir erro 0x00000709", erro_709, "Corrige erro de impressora padrão (0x00000709).")
        ]),

        criar_grupo("⚙️  Sistema GPLUS", [
            ("✅  Verificacao GPLUS", verificar_gplus, "Verifica serviços, arquivos e processos do GPLUS."),
            ("🚫  Encerrar os exes e o Firebird", encerrar_processos_gplus, "Para todos os exes do sistema e o Firebird."),
            ("🚀  Verificar Status Shipay", verificar_shipay_status, "Consulta o status do servidor da Shipay."),
            ("🔄  Verificar Integradores", verificar_integrador, "Verifica e reinicia GpIfood, Integrador e GpToGo se necessário.")
        ])
    ]

    # Dividir os grupos em colunas
    col1 = ft.Column(grupos[:3], spacing=25)
    col2 = ft.Column(grupos[3:], spacing=25)

    # Adicionar à página
    page.add(
        ft.Column([
            titulo_principal,
            ft.Row(
                [col1, col2],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            )
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # page.add(ft.Row([col1, col2], alignment=ft.MainAxisAlignment.SPACE_EVENLY))

if __name__ == "__main__":
    ft.app(target=main)