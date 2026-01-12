from scapy.all import *
import time, sys, numpy

target = "172.20.1.2"
port = 80
now = time.perf_counter() 
rtt = 0

# Envia 40 fluxos de pacotes (cada fluxo com 7 pacotes) simulando a interação do cliente com o servidor web
for j in range(100):
  ss = []
  for i in range(7):
    ans = None
    start = time.time()
    try:
      while (not ans):
        ans = sr1(IP(dst=target)/TCP(dport=80), timeout=2, verbose=0)
    except KeyboardInterrupt:
      rtt = (time.time() - start) * 1000  # em ms
      ss.append(rtt)

      if ss:
        sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\t')
        sys.stdout.write(f"RTT: {numpy.mean(ss):.2f}ms\n")
        exit(0)

    rtt = (time.time() - start) * 1000  # em ms
    ss.append(rtt)

  if ss:
    sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\t')
    sys.stdout.write(f"RTT: {numpy.mean(ss):.2f}ms\n")
  else:
    sys.stdout.write("Sem resposta\n")
  time.sleep(5)
