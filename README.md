# DoS Poison

## Informações básicas

### Hardware

* CPU: Intel(R) Core(TM) i5-10400 CPU @ 2.90GHz
* RAM: 16 GB 

### Software

* Kernel: 6.12.57
* SO: Debian GNU/Linux 13 (trixie)
* Docker - versão 28.1.1.

## Dependências

Todo o sistema foi rodado em Docker, então a unica coisa necessaria para executar o arterfato é o proprio Docker.

## Instalação

### Atualização do sistema
```
sudo apt update && sudo apt upgrade
```

### Dependencias 
```
sudo apt install ca-certificates curl gnupg
```

### Adicione a chave GPG oficial da Docker 
```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### Configure o repositório da Docker
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Atualize o índice de pacotes
```
sudo apt update
```

### Instale o Docker Engine e o plugin do Docker Compose
```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Experimentos

* Todo o processo foi executado com a maquina principal (host) em modo root!
* Para a execução do Experimento, são necessario 4 terminais.

No diretorio `DoS_Poison/ambiente`, execute o comando:

```bash
docker compose up
```

Aguarde todas as maquinas inicializarem.

### Maquina Server

Execute os seguintes comandos:

```bash
docker exec -it server bash
cd /home
./config.sh
exit
```

### Maquina suricata

Execute os seguintes comandos:

```bash
docker exec -it suricata bash
cd /etc/suricata
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 monitor.py
```

### Maquina client

Execute os seguintes comandos:

```bash
docker exec -it client bash
cd /home
./config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 time.py # Execute esse comando junto ao full_attack.py
# Após o full_attack.py finalizar a execução, pode parar o time.py
wget -qO- 172.20.1.2 # Esse comando deve ficar travado, significa que o cliente foi bloqueado pelo Suricata
```

### Maquina attacker 

Execute os seguintes comandos:

```bash
docker exec -it attacker bash
cd /home
./config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 full_attack.py
```

Para confirmar que o processo foi concluido, no diretório `DoS_Poison/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique novamente a reputação do IP `172.20.1.3`, agora, deve ser `1,127`, indicando que ele esta na categoria 1 (BadHosts), com reputação 127 (com certeza é um BadHost), indicando que o Suricata reconheceu o cliente como um IP perigoso, mesmo ele não executando nenhum comando malicioso.

## LICENSE

GNU GPL v3
