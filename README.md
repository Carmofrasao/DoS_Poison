# DoS Poison

## Basic information

### Hardware

* CPU: Intel(R) Core(TM) i5-10400 CPU @ 2.90GHz
* RAM: 16 GB 

### Software

* Kernel: 6.12.57
* SO: Debian GNU/Linux 13 (trixie)
* Docker - version 28.1.1.

## Dependencies

The entire system runs on Docker, so the only thing needed to run the artifact is Docker itself.

## Installation

### System update
```
sudo apt update && sudo apt upgrade
```

### Dependencies 
```
sudo apt install ca-certificates curl gnupg
```

### Add Docker's official GPG key 
```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### Set up the Docker repository
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Update the package index
```
sudo apt update
```

### Install the Docker Engine and the Docker Compose plugin
```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Experiments

* The entire process was run with the host machine in root mode!
* Four terminals are required to run the experiment.

In the `DoS_Poison/ambiente` directory, run the following command:

```bash
docker compose up
```

Please wait for all machines to start up.

### Server machine

Run the following commands:

```bash
docker exec -it server bash
cd /home
./config.sh
exit
```

### Suricata machine

Run the following commands:

```bash
docker exec -it suricata bash
cd /etc/suricata
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 monitor.py
```

### Client machine

Run the following commands:

```bash
docker exec -it client bash
cd /home
./config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 time.py # Run this command alongside full_attack.py
# Once full_attack.py has finished running, you can stop time.py
wget -qO- 172.20.1.2 # This command should be stuck; it means the client has been blocked by Suricata
```

### Attacker machine

Run the following commands:

```bash
docker exec -it attacker bash
cd /home
./config.sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 full_attack.py
```

To verify that the process has completed, in the `DoS_Poison/ambiente/suricata-config/iprep/` directory, run the following command:

```bash
cat reputation.list
```

And check the reputation of IP `172.20.1.3` again; it should now be `1,127`, indicating that it is in category 1 (BadHosts) with a reputation of 127 (it is definitely a BadHost), meaning that Suricata has identified the client as a dangerous IP address, even though it did not execute any malicious commands.
