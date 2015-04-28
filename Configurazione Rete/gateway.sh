#!/bin/bash
#parameters

sniffer="9";
alias="1";
server="2";
server_port="9090"
network_1="172.1.1";
network_2="172.1.2";
cidr="/24";

# change ip alias
ifconfig wlan0:1 $network_1.$alias$cidr;
ifconfig wlan0:2 $network_2.$alias$cidr;

#delete defualt gateway
route del default;

#delete second default gateway
route del -net 192.168.43.0 gw 0.0.0.0 netmask 255.255.255.0

#promiscus mode (cambiare eth1 con interfaccia di rete giusta)
ip link set wlan0 promisc on

#Activate forwarding
sysctl -w net.ipv4.ip_forward=1;

# Filtering rules
#iptables -t filter -F;

#abilito solo forward dei pacchetti e chiudo input e output
#iptables -t filter -P INPUT DROP
#iptables -t filter -P OUTPUT DROP

#abilito il traffico localhost sia input che output
#iptables -t filter -A INPUT -i lo -j ACCEPT
#iptables -t filter -A OUTPUT -o lo -j ACCEPT

#mangle
#iptables -t mangle -A PREROUTING -p tcp --dport 2020 -j MARK --set-mark 1

iptables -t mangle -A POSTROUTING -j TEE --gateway $network_1.$sniffer
#iptables -t mangle -A PREROUTING -j TEE --gateway $network_1.$sniffer

iptables -t nat -A PREROUTING -p udp --dport 2020 -j DNAT --to-destination $network_2.$server:$server_port
#iptables -t nat -A PREROUTING -p tcp -m mark --mark 1 -j DNAT --to-destination $network_2.$server:$server_port
#iptables -I POSTROUTING -t mangle -m mark --mark 1 -j TEE --gateway $network_1.$sniffer:$server_port
