import pyinotify
import ast
import json
import os
import subprocess

log_file = '/etc/suricata/eve.json'
lua_script_file = '/etc/suricata/rules/script.lua'
reputation_file = '/etc/suricata/iprep/reputation.list'
ips = "/etc/suricata/suricata.yaml"

reputation_dict = {
  3: {
    127: 0.00,
    107: 0.05,
    87: 0.10,
    67: 0.15,
    47: 0.20,
    27: 0.25,
    7: 0.30
  },
  2: {
    7: 0.35,
    27: 0.40,
    47: 0.45,
    67: 0.50,
    87: 0.55,
    107: 0.60,
    127: 0.65
  },
  1: {
    7: 0.70,
    27: 0.75,
    47: 0.80,
    67: 0.85,
    87: 0.90,
    107: 0.95,
    127: 1.00
  }
}

# Monitorando atualização do arquivo eve.json (onde o suricata grava os logs)
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        if event.pathname == log_file:
            with open(log_file, 'r') as f:
                for line in f:
                    pass
                event = json.loads(line)
                if 'alert' in event:
                    src_ip = event['src_ip']
                    if src_ip:
                        update_reputation(src_ip)

def update_ips_file(ip):
  # Lê todas as linhas do arquivo
  with open(ips, "r") as f:
      linhas = f.readlines()

  # Procura a linha que define HOME_NET
  for i in range(len(linhas)):
      linha = linhas[i]
      if "HOME_NET:" in linha:
          # Extrai a string entre aspas
          inicio = linha.find('"')
          fim = linha.rfind('"')
          conteudo_str = linha[inicio+1:fim]

          # Remove espaços extras de IPs (segurança extra)
          ipn = [ipl.strip() for ipl in conteudo_str[1:-1].split(",") if ipl.strip()]

          # Adiciona se não estiver
          if ip not in ipn:
              ipn.append(ip)

          # Gera a nova string no formato desejado (sem aspas nos IPs)
          nova_str = '[{}]'.format(','.join(ipn))

          # Atualiza a linha
          linhas[i] = f'    HOME_NET: "{nova_str}"\n'
          break

  # Escreve o arquivo de volta
  with open(ips, "w") as f:
      f.writelines(linhas)

# Atualizando provavilidade do suricata dropar um pacote ou não, 
# de acordo com a reputação do IP de origem
def update_drop_probability(probability):
    with open(lua_script_file, 'r+') as f:
        lines = f.readlines()
        lines[9] = f"\t\t\tif math.random() < {probability} then\n"
        f.seek(0)
        f.writelines(lines)
        f.close()

# Atualizando reputação de IPs que tiveram interações mal intencionadas com o Suricata
def update_reputation(ip):
    new_category = 2
    new_reputation = 7
    if not os.path.exists(reputation_file):
        with open(reputation_file, 'w') as f:
            f.write(f"{ip},2,7\n")
    else:
        with open(reputation_file, 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Caso onde o IP ja esta em reputation.list
                if line.startswith(ip):
                    # Para o GoodHost, quanto mais alta a reputação, melhor
                    # Para o GreyHost e BadHost, quanto mais alta a reputação, pior
                    new_category = int(line.split(",")[1])
                    new_reputation = int(line.split(",")[2])
                    # Caso onde a categoria é GoodHost
                    if new_category == 3:
                      # Caso onde a reputação esta baixa de mais, abaixa a categoria e reseta a reputação
                      if new_reputation < 10:
                        new_reputation = 7 
                        new_category = 2
                      # Caso onde a reputação ainda esta boa 
                      else:
                        new_reputation -= 20
                    # Caso onde a categoria é GreyHost
                    elif new_category == 2:
                      # Caso onde a reputação esta alta de mais, abaixa a categoria e reseta a reputação
                      if new_reputation > 120:
                        new_reputation = 7
                        new_category = 1
                      # Caso onde a reputação ainda esta boa 
                      else:
                        new_reputation += 20
                    # Caso onde a categoria é BadHost
                    elif new_category == 1:
                      # Caso onde a reputação ainda esta "boa" 
                      if new_reputation <= 107:
                        new_reputation += 20
                      # Depois disso, a regra de drop joga os pacotes fora! 

                    lines[i] = f"{ip},{new_category},{new_reputation}\n"
                    break
            else:
                lines.append(f"{ip},3,127\n")
            f.seek(0)
            f.writelines(lines)
    update_drop_probability(reputation_dict[new_category][new_reputation])
    update_ips_file(ip)
    reload_suricata()

def reload_suricata():
    subprocess.run(['suricatasc', '-c', 'ruleset-reload-nonblocking'])

wm = pyinotify.WatchManager()
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch(log_file, pyinotify.IN_MODIFY)

print(f"Monitorando {log_file} para atualizações...")
notifier.loop()
