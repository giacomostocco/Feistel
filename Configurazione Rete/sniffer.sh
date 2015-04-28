#!/bin/bash

#ricevo come parametro l'indirizzo dell'host della rete
case $# in
 2 ) ip=$1; interface=$2 ;;
 *) echo "chiamare il programma sudo sh host ip interface(wlan0:1, eth1:2)"; exit;;
esac

echo $ip $interface; 

gw=1;
cidr=/24;

ifconfig $interface $ip$cidr;

#delete default gateway
route del default gw 192.168.43.1;

#add gateway depending of sub network
oct1=$(echo ${ip} | tr "." " " | awk '{ print $1 }')
oct2=$(echo ${ip} | tr "." " " | awk '{ print $2 }')
oct3=$(echo ${ip} | tr "." " " | awk '{ print $3 }')
oct4=$(echo ${ip} | tr "." " " | awk '{ print $4 }')
route add default gw 172.1.$oct3.1 

#delete second default gateway
route del -net 192.168.43.0 gw 0.0.0.0 netmask 255.255.255.0

ip link set wlan0 promisc on
sysctl -w net.ipv4.ip_forward=1;

iptables -t nat -A PREROUTING -p tcp --dport 2020 -j DNAT --to-destination $1:9093
