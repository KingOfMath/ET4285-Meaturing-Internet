%%
%read data
bbrpcc = importdata('clientpccbbr.txt',',');
bbrtcp = importdata('clienttcpbbr.txt',',');
cubicpcc = importdata('clientpcccubic.txt',',');
cubictcp = importdata('clienttcpcubic.txt',' ');
vegaspcc = importdata('clientpccvegas.txt',',');
vegastcp = importdata('clienttcpvegas.txt',' ');
bbrtcprtt = importdata('clienttcpbbrrtt.txt',',');
cubictcprtt = importdata('clienttcpcubicrtt.txt',',');
vegastcprtt = importdata('clienttcpvegasrtt.txt',',');

%%
%pick out throughput and RTT, all RTT in ms, all throughput in Mbits/sec
pccbbr = struct;
pccbbr.throughput = bbrpcc(1:590,2);
pccbbr.RTT = bbrpcc(1:590,3);
pcccubic = struct;
pcccubic.throughput = cubicpcc(1:590,2);
pcccubic.RTT = cubicpcc(1:590,3);
pccvegas = struct;
pccvegas.throughput = vegaspcc(1:590,2);
pccvegas.RTT = vegaspcc(1:590,3);

tcpvegas =  struct;
tcpvegas.throughput = vegastcp.textdata(1:590,4);
tcpvegas.throughput = str2double(tcpvegas.throughput);
   index_vegas = find(contains(vegastcp.textdata(1:590,5),'Kbits/sec'));
tcpvegas.throughput(index_vegas) = tcpvegas.throughput(index_vegas)/1024;
tcpvegas.RTT = vegastcprtt(1:590,2);

tcpcubic =  struct;
tcpcubic.throughput = cubictcp.textdata(1:590,4);
tcpcubic.throughput = str2double(tcpcubic.throughput);
   index_cubic = find(contains(cubictcp.textdata(1:590,5),'Kbits/sec'));
tcpcubic.throughput(index_cubic) = tcpcubic.throughput(index_cubic)/1024;
tcpcubic.RTT = cubictcprtt(1:590,2);

tcpbbr =  struct;
tcpbbr.throughput = bbrtcp.textdata(1:590,4);
tcpbbr.throughput = str2double(tcpbbr.throughput);
   index_cubic = find(contains(bbrtcp.textdata(1:590,5),'Kbits/sec'));
tcpbbr.throughput(index_cubic) = tcpbbr.throughput(index_cubic)/1024;
tcpbbr.RTT = bbrtcprtt(1:590,2);
%%
%compute Jain's fairness index
J_cubic_TP = Jain(tcpcubic.throughput,pcccubic.throughput);
mean(J_cubic_TP)
var(J_cubic_TP)
J_cubic_RTT = Jain(tcpcubic.RTT,pcccubic.RTT);
mean(J_cubic_RTT)
var(J_cubic_RTT)
J_vegas_TP = Jain(tcpvegas.throughput,pccvegas.throughput);
mean(J_vegas_TP)
var(J_vegas_TP)
J_vegas_RTT = Jain(tcpvegas.RTT,pccvegas.RTT);
mean(J_vegas_RTT)
var(J_vegas_RTT)
J_bbr_TP = Jain(tcpbbr.throughput,pccbbr.throughput);
mean(J_bbr_TP)
var(J_bbr_TP)
J_bbr_RTT = Jain(tcpbbr.RTT,pccbbr.RTT);
mean(J_bbr_RTT)
var(J_bbr_RTT)

%%
%throughput plots
figure
hold on
plot(pcccubic.throughput);
plot(tcpcubic.throughput);
hold off
title('Throughput Aurora and Cubic');
legend('Aurora','Cubic');
xlabel('Time (sec)');
ylabel('Throughput (Mbits/sec)');
figure
hold on
plot(pcccubic.RTT);
plot(tcpcubic.RTT);
hold off
title('RTT Aurora and Cubic');
legend('Aurora','Cubic');
xlabel('Time (sec)');
ylabel('RTT (ms)');

figure
hold on
plot(pccvegas.throughput);
plot(tcpvegas.throughput);
hold off
title('Throughput Aurora and Vegas');
legend('Aurora','Vegas');
xlabel('Time (sec)');
ylabel('Throughput (Mbits/sec)');
figure
hold on
plot(pccvegas.RTT);
plot(tcpvegas.RTT);
hold off
title('RTT Aurora and Vegas');
legend('Aurora','Vegas');
xlabel('Time (sec)');
ylabel('RTT (ms)');

figure
hold on
plot(pccbbr.throughput);
plot(tcpbbr.throughput);
hold off
title('Throughput Aurora and BBR');
legend('Aurora','BBR');
xlabel('Time (sec)');
ylabel('Throughput (Mbits/sec)');
figure
hold on
plot(pccbbr.RTT);
plot(tcpbbr.RTT);
hold off
title('RTT Aurora and BBR');
legend('Aurora','BBR');
xlabel('Time (sec)');
ylabel('RTT (ms)');

%%
%fairness plots
figure
plot(J_cubic_TP);
title('Throughput fairness Aurora and Cubic')
xlabel('Time (sec)');
ylabel('Jain fairness index');
ylim(0:1);
figure
plot(J_cubic_RTT);
title('RTT fairness Aurora and Cubic')
xlabel('Time (sec)');
ylabel('Jain fairness index');
ylim(0:1);
figure
plot(J_vegas_TP);
title('Throughput fairness Aurora and Vegas')
xlabel('Time (sec)');
ylabel('Jain fairness index');
ylim(0:1);
figure
plot(J_vegas_RTT);
title('RTT fairness Aurora and Vegas')
xlabel('Time (sec)');
ylabel('Jain fairness index');
ylim(0:1);
figure
plot(J_bbr_TP);
title('Throughput fairness Aurora and BBR')
xlabel('Time (sec)');
ylabel('Jain fairness index');
ylim(0:1);
figure
plot(J_bbr_RTT);
title('RTT fairness Aurora and BBR')
xlabel('Time (sec)');
ylabel('Jain fairness index');
ylim(0:1);


