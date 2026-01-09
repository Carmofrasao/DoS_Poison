#!/bin/sh
apt update && apt install -y iproute2
ip route delete default
ip route add default via 172.20.0.3 dev eth0

