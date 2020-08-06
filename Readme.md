TCP:

iperf3 commands :

iperf3 -s 

Modprobe  -a tcp_bbr

sudo bash -c 'echo vegas > /proc/sys/net/ipv4/tcp_congestion_control'

run iperf3 client command

run ping for latency data
