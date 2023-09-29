import psutil, ctypes, os, threading, win32com.client
from tkinter import Tk, Button, Label, Text, PhotoImage

# Variáveis globais para a thread de injeção
thread_injecao = None
# Adicione uma variável global para controlar o estado do monitoramento
monitoramento_ligado = False

def ligar_monitoramento():
    global monitoramento_ligado
    global parar_injecao

    create_shortcut()

    if not monitoramento_ligado:
        monitoramento_ligado = True

        # Cria um evento para sinalizar quando a injeção deve ser interrompida
        parar_injecao = threading.Event()

        def run_in_thread():
            while not parar_injecao.is_set():
                # Chama a função de injeção dentro do loop
                inject()
                #time.sleep(0.000001)

        # Inicia o loop infinito em um thread separado
        threading.Thread(target=run_in_thread).start()
    else:
        print("O monitoramento já está ligado.")

def iniciar_interface():
    # Cria a janela principal
    janela = Tk()
    janela.title("WhiteBlood")
    janela.geometry("400x300")
    janela.configure(background='white')

    # Carrega a imagem da logo
    logo = PhotoImage(file="logo.png")
    logo = logo.subsample(4)  # Reduz o tamanho da imagem pela metade

    # Cria a marca d'água com a logo
    marca_dagua = Label(janela, image=logo, bg='white')
    marca_dagua.pack(side='bottom', anchor='sw')

    # Adiciona o ícone
    janela.iconbitmap('logo.ico')

    # Cria os botões
    botao_ligar = Button(janela, text="Ligar monitoramento", command=ligar_monitoramento)
    botao_desligar = Button(janela, text="Desligar monitoramento", command=desligar_monitoramento)

    # Posiciona os botões na janela
    botao_ligar.pack()
    botao_desligar.pack()

    # Cria o campo de texto para o log
    campo_texto = Text(janela)
    campo_texto.pack()

    # Inicia o loop principal da interface gráfica
    janela.mainloop()

def desligar_monitoramento():
    global monitoramento_ligado
    global parar_injecao

    if monitoramento_ligado:
        monitoramento_ligado = False

        # Sinaliza que a injeção deve ser interrompida
        if parar_injecao is not None:
            parar_injecao.set()
    else:
        print("O monitoramento já está desligado.")



def create_shortcut():
    # Caminho para o executável do seu programa
    program_path = "C:\\Program Files (x86)\\ProunersCyBR\\WhiteBlood\\WhiteBlood.exe"

    # Caminho para a pasta de inicialização
    startup_folder = os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Caminho para a área de trabalho
    desktop_folder = os.path.expanduser('~\\Desktop')

    # Nome do atalho
    shortcut_name = "WhiteBlood.lnk"

    # Caminho completo para o atalho na pasta de inicialização
    startup_shortcut_path = os.path.join(startup_folder, shortcut_name)

    # Caminho completo para o atalho na área de trabalho
    desktop_shortcut_path = os.path.join(desktop_folder, shortcut_name)

    # Verifica se o atalho já existe na pasta de inicialização
    if not os.path.exists(startup_shortcut_path):
        # Cria o atalho na pasta de inicialização
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(startup_shortcut_path)
        shortcut.TargetPath = program_path
        shortcut.Save()

    # Verifica se o atalho já existe na área de trabalho
    if not os.path.exists(desktop_shortcut_path):
        # Cria o atalho na área de trabalho
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(desktop_shortcut_path)
        shortcut.TargetPath = program_path
        shortcut.Save()


def inj_dll(proc, handle, addr):
    # Escreva o caminho da DLL na memória alocada
    dll_path = 'C:\\Program Files (x86)\\ProunersCyBR\\WhiteBlood\\injecaodll\\x64\\Debug\\injetador.dll'
    buffer = ctypes.create_string_buffer(dll_path.encode('utf-8'))
    size = len(dll_path) + 1
    bytes_written = ctypes.c_int(0)
    ctypes.windll.kernel32.WriteProcessMemory(handle, addr, buffer, size, ctypes.byref(bytes_written))
    
    # Crie uma nova thread no processo de destino
    LOAD_LIBRARY = ctypes.windll.kernel32.GetProcAddress(ctypes.windll.kernel32.GetModuleHandleA("kernel32.dll"), b"LoadLibraryA")
    thread_id = ctypes.c_ulong(0)
    ctypes.windll.kernel32.CreateRemoteThread(handle, None, 0, LOAD_LIBRARY, addr, 0, ctypes.byref(thread_id))

def inj_exc(process):
    try:
        exe_path = process.info['exe']
        if exe_path is not None:
            if not exe_path.startswith("C:\\Windows") and not exe_path.startswith("C:\\Program Files\\Python311") and not exe_path.startswith("C:\\Program Files") and not exe_path.startswith("C:\\Program Files (x86)") and process.info['name'] not in ["System", "Registry", "WhiteBlood.exe"]:
                # exe_path não está localizado na pasta "C:\Windows"
                return False
        return True
    except Exception as e:
        print("Erro não previsto:", e)
        return False

def inject():
    proc_mal_pids = set()
    # Obtenha um identificador para o processo de destino
    PROCESS_ALL_ACCESS = 0x1F0FFF

    try: 
        for process in psutil.process_iter(["name", "pid", "exe"]):
            legit = inj_exc(process)
            if not legit:
                proc_mal_pids.add(process.pid)
            else:
                continue
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

    for pid in proc_mal_pids:
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

        # Aloque memória no processo de destino
        MEM_RESERVE = 0x00002000
        MEM_COMMIT = 0x00001000
        PAGE_READWRITE = 0x04
        size = 1024  # Substitua pelo tamanho necessário
        addr = ctypes.windll.kernel32.VirtualAllocEx(handle, 0, size, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)

        inj_dll(pid, handle, addr)