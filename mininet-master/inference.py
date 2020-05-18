#!/usr/bin/env python3

import os
import numpy as np
import gym
from stable_baselines import PPO1
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.cli import CLI


def main():

    # Load a .zip model file
    model_name = os.path.join(os.getcwd(), "ppo1_cc_0.zip")
    model = PPO1.load(model_name)

    # TODO start the mininet network
    sr=10
    class SingleSwitchTopo( Topo ):                                                                                               
                                                                                                      
      def build( self, count=1 ):                                                                                      
        hosts = [ self.addHost( 'h%d' % i )                                                                                   
                  for i in range( 1, count + 1 ) ]                                                                                
        s1 = self.addSwitch( 's1' )                                                                                           
        for h in hosts:                                                                                                       
            self.addLink( h, s1, bw=sr, delay='5ms', loss=2,
                          max_queue_size=1000, use_htb=True )                                                                                             
    # link rate = 10, max queue zie= 1000, loss percentage= 2%
    state=[]
    for i in range(0,10):
        net = Mininet( topo=SingleSwitchTopo( 3 ) )                                                                               
        net.start()                                                                                                               
        dumpNodeConnections(net.hosts)
        h1,h4=net.get('h1','h3')
        a=net.pingFull([h1,h4])
        net.monitor()
        perf_array=net.iperf((h1,h4))                                                                                                                
        net.stop()   
        latency_grad=0 #(a[0][2][2]-a[0][2][0])/
        latency_rat=a[0][2][1]/a[0][2][0]
        sending_rat=sr/float(perf_array[0].rsplit(' ',1)[0])
        print(perf_array[0])
        print(a[0][2][2])
        print(latency_rat)
        state.append(latency_grad)
        state.append(latency_rat)
        state.append(sending_rat)
    
    # this model takes as state an input 30x1
    # TODO: this needs to be replaced with real values from the network later on
    #state = np.ones((30,), dtype=np.float32)
    state=np.asarray(state)
    np.reshape(state,(30,))
    # TODO start traffic

    # run inference for some steps
    count = 0
    # while (time.time()-start) < 3:
    while count < 10:

        # The action is an increment to the current sending rate: sending_rate_t+1 = sending_rate_t + action
        action, _ = model.predict(state)
        print("RL model predicted: %s" % action)
        sr=action
        state=[]
        for i in range(0,10):
            net = Mininet( topo=SingleSwitchTopo( 3 ) )                                                                               
            net.start()                                                                                                               
            dumpNodeConnections(net.hosts)
            h1,h4=net.get('h1','h3')
            a=net.pingFull([h1,h4])
            net.monitor()
            perf_array=net.iperf((h1,h4))                                                                                                                
            net.stop()   
            latency_grad=0 #(a[0][2][2]-a[0][2][0])/
            latency_rat=a[0][2][1]/a[0][2][0]
            sending_rat=sr/float(perf_array[0].rsplit(' ',1)[0])
            print(perf_array[0])
            print(a[0][2][2])
            print(latency_rat)
            state.append(latency_grad)
            state.append(latency_rat)
            state.append(sending_rat)
        # Update the state to account for effects of action
        # TODO: this needs to be replaced with real values from the network later on
        #state = state * 1.1
        #count += 1
        state=np.asarray(state)
        np.reshape(state,(30,))

if __name__ == '__main__':
    main()
