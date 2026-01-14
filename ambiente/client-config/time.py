import time, sys, requests

target = "172.20.1.2"
port = 80
now = time.perf_counter() 
rtt = 0

# Envia 100 fluxos de pacotes simulando a interação do cliente com o servidor web
for j in range(100):
    ans = None
    start = time.time()
    try:
        asn = requests.get('http://172.20.1.2')
    except KeyboardInterrupt:
        rtt = (time.time() - start) * 1000  # em ms

        if rtt:
            sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\t')
            sys.stdout.write(f"RTT: {rtt:.2f}ms\n")
            exit(0)

    rtt = (time.time() - start) * 1000  # em ms

    if rtt:
        sys.stdout.write(f'Tempo: {(time.perf_counter()-now):.2f}s\t')
        sys.stdout.write(f"RTT: {rtt:.2f}ms\n")
    else:
        sys.stdout.write("Sem resposta\n")
    time.sleep(10)
    rtt = 0
