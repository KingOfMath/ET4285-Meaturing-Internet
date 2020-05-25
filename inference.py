#!/usr/bin/env python3

import os
import numpy as np
import gym
from stable_baselines import PPO1
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, decode
from mininet.log import info, setLogLevel
from mininet.cli import CLI
from time import sleep, time
from select import poll, POLLIN
from subprocess import Popen, PIPE
from functools import partial

from fairness.benchmark import run

def monitorFiles(outfiles, seconds, timeoutms):
    "Monitor set of files and return [(host, line)...]"
    devnull = open('/dev/null', 'w')
    tails, fdToFile, fdToHost = {}, {}, {}
    for h, outfile in outfiles.items():
        tail = Popen(['tail', '-f', outfile],
                     stdout=PIPE, stderr=devnull)
        fd = tail.stdout.fileno()
        tails[h] = tail
        fdToFile[fd] = tail.stdout
        fdToHost[fd] = h
    # Prepare to poll output files
    readable = poll()
    for t in tails.values():
        readable.register(t.stdout.fileno(), POLLIN)
    # Run until a set number of seconds have elapsed
    endTime = time() + seconds
    while time() < endTime:
        fdlist = readable.poll(timeoutms)
        if fdlist:
            for fd, _flags in fdlist:
                f = fdToFile[fd]
                host = fdToHost[fd]
                # Wait for a line of output
                line = f.readline().strip()
                yield host, decode(line)
        else:
            # If we timed out, return nothing
            yield None, ''
    for t in tails.values():
        t.terminate()
    devnull.close()  # Not really necessary


def binding(net):
    "Test bind mounts"
    privateDirs = [('/var/log', '/tmp/%(name)s/var/log'),
                   ('/var/run', '/tmp/%(name)s/var/run'),
                   '/var/mn']
    directories = [directory[0] if isinstance(directory, tuple)
                   else directory for directory in privateDirs]
    info('Private Directories:', directories, '\n')


def monitor(net, seconds=3):
    hosts = net.hosts
    print("Starting test...")
    server = hosts[0]
    outfiles, errfiles = {}, {}
    for h in hosts:
        # Create and/or erase output files
        outfiles[h] = '/tmp/%s.out' % h.name
        errfiles[h] = '/tmp/%s.err' % h.name
        h.cmd('echo >', outfiles[h])
        h.cmd('echo >', errfiles[h])
        # Start pings
        h.cmdPrint('ping', server.IP(),
                   '>', outfiles[h],
                   '2>', errfiles[h],
                   '&')
    print("Monitoring output for", seconds, "seconds")
    f = open('/tmp/date.out', 'w')
    for h, line in monitorFiles(outfiles, seconds, timeoutms=500):
        if h:
            print('%s: %s' % (h.name, line))
            f.write(str(h.name + ": " + line + "\n"))
    for h in hosts:
        h.cmd('kill %ping')

def parameters(net, link):
    # flush out latency from reactive forwarding delay
    net.pingAll()

    print( '\n*** Configuring one intf with bandwidth of 5 Mb\n' )
    link.intf1.config( bw=5 )
    print( '\n*** Running iperf to test\n' )
    net.iperf()

    print( '\n*** Configuring one intf with delay of 15ms\n' )
    link.intf1.config( delay='15ms' )
    print( '\n*** Run a ping to confirm delay\n' )
    net.pingPairFull()

    print( '\n*** Done testing\n' )


def main():
    # Load a .zip model file
    model_name = os.path.join(os.getcwd(), "ppo1_cc_0.zip")
    model = PPO1.load(model_name)

    # TODO start the mininet network
    sr = 10

    class SingleSwitchTopo(Topo):

        def build(self, count=1):
            hosts = [self.addHost('h%d' % i)
                     for i in range(1, count + 1)]
            s1 = self.addSwitch('s1')
            for h in hosts:
                self.addLink(h, s1, bw=sr, delay='5ms', loss=2,
                             max_queue_size=1000, use_htb=True)

    # link rate = 10, max queue zie= 1000, loss percentage= 2%
    state = []

    for i in range(0, 1):
        net = Mininet(topo=SingleSwitchTopo(3))
        net.start()
        dumpNodeConnections(net.hosts)
        h1, h4 = net.get('h1', 'h3')
        s1 = net.get('s1')
        a = net.pingFull([h1, h4])
        net.monitor()
        perf_array = net.iperf((h1, h4))
        link = net.addLink(h1, s1)


        # Q: Monitoring RTT(MS)? Average RTT how many packets?
        monitor(net, seconds= 10)
        binding(net)
        # Q: loss-based? Dynamically change the delay and loss?
        parameters(net,link)

        net.stop()

        # Q: fairness running
        run()

        latency_grad = 0  # (a[0][2][2]-a[0][2][0])/
        latency_rat = a[0][2][1] / a[0][2][0]
        sending_rat = sr / float(perf_array[0].rsplit(' ', 1)[0])
        print(perf_array[0])
        print(a[0][2][2])
        print(latency_rat)
        state.append(latency_grad)
        state.append(latency_rat)
        state.append(sending_rat)

    # this model takes as state an input 30x1
    # TODO: this needs to be replaced with real values from the network later on
    # state = np.ones((30,), dtype=np.float32)
    # state = np.asarray(state)
    # np.reshape(state, (30,))
    # TODO start traffic

    # monitorTest()

    # run inference for some steps
    # count = 0
    # # while (time.time()-start) < 3:
    # while count < 1:
    #
    #     # The action is an increment to the current sending rate: sending_rate_t+1 = sending_rate_t + action
    #     action, _ = model.predict(state)
    #     print("RL model predicted: %s" % action)
    #     sr=action
    #     state=[]
    #     for i in range(0,10):
    #         net = Mininet( topo=SingleSwitchTopo( 3 ) )
    #         net.start()
    #         dumpNodeConnections(net.hosts)
    #         h1,h4=net.get('h1','h3')
    #         a=net.pingFull([h1,h4])
    #         net.monitor()
    #         perf_array=net.iperf((h1,h4))
    #         net.stop()
    #         latency_grad=0 #(a[0][2][2]-a[0][2][0])/
    #         latency_rat=a[0][2][1]/a[0][2][0]
    #         sending_rat=sr/float(perf_array[0].rsplit(' ',1)[0])
    #         print(perf_array[0])
    #         print(a[0][2][2])
    #         print(latency_rat)
    #         state.append(latency_grad)
    #         state.append(latency_rat)
    #         state.append(sending_rat)
    #     # Update the state to account for effects of action
    #     # TODO: this needs to be replaced with real values from the network later on
    #     #state = state * 1.1
    #     #count += 1
    #     state=np.asarray(state)
    #     np.reshape(state,(30,))


if __name__ == '__main__':
    main()
