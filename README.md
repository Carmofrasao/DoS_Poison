# DoS Poison

## Informações básicas

### Hardware

* CPU: AMD EPYC 7401 24-Core 2.0GHz
* RAM: 32 GB 
* Kernel: 6.12.13
* SO: Debian GNU/Linux 12 (bookworm)

### Software

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

### Reivindicações #1

* Todo o processo foi executado com a maquina principal (host) em modo root!
* Para a execução do Experimento, são necessario 4 terminais.

No diretorio `SBSeg-2025-Frasao/ambiente`, execute o comando:

```bash
docker compose up
```

Aguarde todas as maquinas inicializarem.

#### Maquina suricata

Execute os seguintes comando:

```bash
docker exec -it suricata bash
cd /etc/suricata
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 monitor.py
```

A Figura a seguir demonstra a execução do ataque de negação de serviço baseado em envenenamento. Ao final, o servidor para de receber os pacotes que o cliente esta mandando, demonstrando a eficacia do ataque!

![Evolução do volume de pacotes gerados na rede.](https://github.com/Carmofrasao/SBSeg-2025-Frasao/blob/main/imagens/variacao_de_pacotes.jpg)

#### Maquina client

Execute os seguintes comando:

```bash
docker exec -it client bash
cd /home
./config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 time.py # Execute esse comando junto ao syn-flood.py
# Após o syn-flood.py finalizar a execução, pode parar o time.py
wget -qO- 172.20.1.2 # Esse comando deve ficar travado, significa que o cliente foi bloqueado pelo Suricata
```

O gráfico de tempo de resposta às requisições legítimas, presente na Figura a seguir apresenta um padrão de aumento contínuo, refletindo a degradação gradual no desempenho da comunicação entre o cliente legítimo e o servidor. Ao final, o tempo de resposta tende ao infinito, mostrando que o cliente esta bloqueado.

![Variação do tempo de resposta percebido pelo cliente legítimo ao fazer requisições para o servidor](https://github.com/Carmofrasao/SBSeg-2025-Frasao/blob/main/imagens/rtt.jpg)

#### Maquina attacker 

Execute os seguintes comando:

```bash
docker exec -it attacker bash
cd /home
./config.sh
python3 syn-flood.py
```

Para confirmar que o processo foi concluido, no diretório `SBSeg-2025-Frasao/ambiente/suricata-config/iprep/`, execute o comando: 

```bash
cat reputation.list
```

E verifique novamente a reputação do IP `172.20.1.3`, agora, deve ser `1,127`, indicando que ele esta na categoria 1 (BadHosts), com reputação 127 (com certeza é um BadHost), indicando que o Suricata reconheceu o cliente como um IP perigoso, mesmo ele não executando nenhum comando malicioso.

## LICENSE

GNU GPL v3
