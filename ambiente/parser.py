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

rtt_y = [x / 1000 for x in obj_rtt.values()]

fig, ax1 = plt.subplots(2,2)

ax1[0,0].plot(all_times, server_y, label='Suricata -> Web Server', color='red', linestyle='solid', linewidth=0.5)
ax1[0,1].plot(all_times, attacker_y, label='Attacker -> Suricata', color='blue', linestyle='solid', linewidth=0.5)
ax1[1,0].plot(all_times, client_y, label='Client -> Suricata', color='green', linestyle='solid', linewidth=0.5)
ax1[1,1].plot(list(obj_rtt.keys()), rtt_y, label='RTT', color='purple', linestyle='solid', linewidth=0.5)

ax1[0,0].set_xlabel("Time (s)", fontsize=8)
ax1[0,1].set_xlabel("Time (s)", fontsize=8)
ax1[1,0].set_xlabel("Time (s)", fontsize=8)
ax1[1,1].set_xlabel("Time (s)", fontsize=8)

ax1[0,0].set_ylabel("Packets", fontsize=8)
ax1[0,1].set_ylabel("Packets", fontsize=8)
ax1[1,0].set_ylabel("Packets", fontsize=8)
ax1[1,1].set_ylabel("Seconds", fontsize=8)


ax1[0,0].set_title("Suricata → Web Server", fontsize=10)
ax1[0,1].set_title("Attacker → Suricata", fontsize=10)
ax1[1,0].set_title("Client → Suricata", fontsize=10)
ax1[1,1].set_title("RTT", fontsize=10)

last_y = rtt_y[-1]
last_x = list(obj_rtt.keys())[-1]

ax1[1,1].scatter(last_x, last_y, marker='x', color='black', s=13, label="Could not receive response")
ax1[1,1].set_label("Could not receive response")

ax1[0,0].grid(True, alpha=0.4, linestyle="--")
ax1[0,1].grid(True, alpha=0.4, linestyle="--")
ax1[1,0].grid(True, alpha=0.4, linestyle="--")
ax1[1,1].grid(True, alpha=0.4, linestyle="--")

ax1[0,0].set_ylim(0, 105)
ax1[0,1].set_ylim(0, 105)
ax1[1,0].set_ylim(0, 105)
ax1[1,1].set_ylim(0, 65)

ax1[0,0].set_xlim(0, 400)
ax1[0,1].set_xlim(0, 400)
ax1[1,0].set_xlim(0, 400)
ax1[1,1].set_xlim(0, 400)

ax1[0,0].tick_params(axis='both', labelsize=6)
ax1[0,1].tick_params(axis='both', labelsize=6)
ax1[1,0].tick_params(axis='both', labelsize=6)
ax1[1,1].tick_params(axis='both', labelsize=6)

ax1[0,0].set_xticks([0,50,100,150,200,250,300,350,400])
ax1[0,1].set_xticks([0,50,100,150,200,250,300,350,400])
ax1[1,0].set_xticks([0,50,100,150,200,250,300,350,400])
ax1[1,1].set_xticks([0,50,100,150,200,250,300,350,400])

fig.set_size_inches(7.5, 4.5)

plt.subplots_adjust(hspace=0.5, wspace=0.2) 

plt.savefig('../imagens/graph.pdf', dpi=300, bbox_inches='tight', format='pdf')

plt.show()
