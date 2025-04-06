#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Add hosts and connect them to the switch
        for h in range(1, n + 1):
            host = self.addHost('h%d' % h,
                               ip='10.0.0.%d/24' % h,
                               mac='00:00:00:00:00:%02x' % h)
            self.addLink(host, switch)

topos = { 'single': SingleSwitchTopo }

def main():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=2)
    net = Mininet(topo=topo, controller=None)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()