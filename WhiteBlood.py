import functions as f, os, sys
import threading

# Muda o diretório de trabalho para o diretório do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Adiciona o diretório de trabalho ao PATH
sys.path.append(os.getcwd())

if __name__ == "__main__":
    # Inicialize a interface gráfica em uma thread separada
    interface_thread = threading.Thread(target=f.iniciar_interface)
    interface_thread.start()

    # Inicia o monitoramento
    f.ligar_monitoramento()

    while True:
        try:
            pass  # Coloque a sua lógica principal aqui

        except KeyboardInterrupt:
            break