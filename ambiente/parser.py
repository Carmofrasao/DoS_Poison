import matplotlib.pyplot as plt
import numpy as np
import math

path_server = "./server-config/log.log"
path_client = "./client-config/log.log"
path_attacker = "./attacker-config/log.log"

path_rtt = "./client-config/rtt.txt"

tempo = ''
obj_attacker = {}
with open(path_attacker, 'r') as file:
    for linha in file:
        if 'Tempo' in linha:
            tempo = int(linha.split(":")[1].strip().split(".")[0])
        if 'Nenhum' in linha:
            obj_attacker[tempo] = 0
        elif 'Pacotes' in linha:
            pkts = int(linha.split()[2])
            obj_attacker[tempo] = pkts


obj_client = {}
with open(path_client, 'r') as file:
    for linha in file:
        if 'Tempo' in linha:
            tempo = int(linha.split(":")[1].strip().split(".")[0])
        if 'Nenhum' in linha:
            obj_client[tempo] = 0
        elif 'Pacotes' in linha:
            pkts = int(linha.split()[2])
            obj_client[tempo] = pkts

obj_server = {}
with open(path_server, 'r') as file:
    for linha in file:
        if 'Tempo' in linha:
            tempo = int(linha.split(":")[1].strip().split(".")[0])
        if 'Nenhum' in linha:
            obj_server[tempo] = 0
        elif 'Pacotes' in linha:
            pkts = int(linha.split()[2])
            obj_server[tempo] = pkts

obj_rtt = {}
with open(path_rtt, 'r') as file:
    for linha in file:
        if "Tempo" in linha:
            tempo = int(linha.split()[1].split('.')[0])
            rtt = int(linha.split()[3].split('.')[0])
            obj_rtt[tempo] = rtt

all_times = sorted(
    set(obj_server.keys()) |
    set(obj_attacker.keys()) |
    set(obj_client.keys())
)

server_y = [obj_server.get(t, 0) for t in all_times]
attacker_y = [obj_attacker.get(t, 0) for t in all_times]
client_y = [obj_client.get(t, 0) for t in all_times]

fig, ax1 = plt.subplots()

ax1.plot(all_times, server_y, label='Suricata -> Web Server', color='red', linestyle='-')
ax1.plot(all_times, attacker_y, label='Attacker -> Suricata', color='blue', linestyle='--')
ax1.plot(all_times, client_y, label='Client -> Suricata', color='green', linestyle='-.')
ax1.set_xlabel("Time")
ax1.set_ylabel("Packets")
ax1.tick_params(axis='y', labelcolor='black')

ax2 = ax1.twinx()

ax2.plot(list(obj_rtt.keys()), list(obj_rtt.values()), label='RTT', color='purple', linestyle='solid')
ax2.set_ylabel("Time (ms)")
ax2.tick_params(axis='y', labelcolor='black')

last_y = list(obj_rtt.values())[-1]
last_x = list(obj_rtt.keys())[-1]

ax2.scatter(last_x, last_y, marker='x', color='black', s=100, label="Couln't receive response")

# 1. Coleta as informações de ambos os eixos
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# 2. Une as listas e cria uma legenda única no ax1 ou ax2
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.grid(True)

fig.set_size_inches(10, 6)

plt.savefig('../imagens/graph.pdf', dpi=300, bbox_inches='tight', format='pdf')

plt.show()
