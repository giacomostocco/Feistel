#!/bin/bash
#questo file configura le reti virtuali per il pc server (.2.2), client(.1.2) e sniffing. Cambiare solo l'indirizo di rete inserito da parametro che devono essere diversi

#ricevo come parametro l'indirizzo dell'host della rete e l'interfaccia
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
