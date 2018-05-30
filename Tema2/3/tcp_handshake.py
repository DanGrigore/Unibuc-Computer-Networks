from scapy.all import *
from struct import *

ip = IP()
ip.src = '198.13.0.15' #sursa     = mid1
ip.dst = '198.13.0.14' #destinatia = rt1
ip.tos = int('011110' + '11', 2) #DSCP && ECN

tcp = TCP()
tcp.sport = 7991
tcp.dport = 10000

optiune = 'MSS'
op_index = TCPOptions[1][optiune] 
op_format = TCPOptions[0][op_index] #!H
valoare = struct.pack(op_format[1], 2) # valoarea 2 a fost impachetata intr-un string de 2 byte
tcp.options = [(optiune, valoare)] #['MSS',2]

tcp.seq = 100

tcp.flags = 'S' 
raspuns_syn_ack = sr1(ip/tcp)

tcp.seq += 1
tcp.ack = raspuns_syn_ack.seq + 1

tcp.flags = 'A'
ACK = ip / tcp
send(ACK)

cuvant='carne'
for x in range(0, 3):
    tcp.flags = 'PAEC'
    tcp.ack = raspuns_syn_ack.seq + 1
    ch=cuvant[x]
    #print ch
    rcv = sr1(ip/tcp/ch)
    #print rcv[1]
    tcp.seq += 1

tcp.flags='R'
RES = ip/tcp
send(RES)

#python /elocal/laborator2/src/tcp_server_modificat.py #rulat pe rt1
#python /elocal/laborator3/src/tcp_handshake.py #rulat pe mid1
