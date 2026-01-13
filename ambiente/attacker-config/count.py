import subprocess
import time
import sys
from datetime import datetime

def count_packets(interface="eth0", interval=10, total_duration=300):
    """
    Conta pacotes de rede em intervalos regulares usando tcpdump.

    Args:
        interface (str): Interface de rede (eth0 ou eth1)
        interval (int): Duração de cada contagem em segundos (padrão: 10)
        total_duration (int): Duração total do monitoramento em segundos (padrão: 300)
    """
    num_intervals = total_duration // interval
    now = time.perf_counter()

    print(f"Monitorando tráfego na interface {interface}: {num_intervals} intervalos de {interval} segundos")

    for i in range(num_intervals):
        start_time = f'{(time.perf_counter()-now):.2f}s'

        # Limita a um número alto de pacotes
        c = 1000000

        cmd = [
            "tcpdump",
            "-i", interface,        # Usa a interface especificada
            "-c", str(c),           # Limita a um número alto de pacotes
            "-w", "-",              # Não salva em arquivo
            "-q",                   # Modo quiet
            "-G", str(interval),    # Duração do intervalo
            "-W", "1",              # Apenas uma execução
            # Atenas pacotes SYN que venham do atacante e vão para o suricata
            "tcp and ip and dst 172.20.1.2 and ether src 7a:f4:40:cd:6c:51"
        ]

        print(f"\nIntervalo {i+1}/{num_intervals} - Tempo: {start_time}")

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = process.communicate()

            if "packets captured" in stderr.decode():
                packets_line = stderr.decode().split("\n")[-3]
                packets = packets_line.split(" ")[0]
                print(f"Pacotes capturados: {packets}")
            else:
                print("Nenhum pacote capturado ou erro na leitura.")

        except KeyboardInterrupt:
            print("\nMonitoramento interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro durante a captura: {e}")
            break

    print("\nMonitoramento finalizado.")

if __name__ == "__main__":
    # Mapeamento de argumentos para interfaces
    interface_map = {
        "0": "eth0",
        "1": "eth1",
    }

    # Verifica se foi passado um argumento
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in interface_map:
            selected_interface = interface_map[arg]
        else:
            print("Argumento inválido. Use:")
            print("0 para eth0 | 1 para eth1")
            sys.exit(1)
    else:
        selected_interface = "eth0"  # Padrão

    count_packets(interface=selected_interface, interval=5, total_duration=450)
