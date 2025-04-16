from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel

class DualQoSTopo(Topo):
    def build(self):
        # Network 1 (no QoS)
        s1 = self.addSwitch('s1')
        h1a = self.addHost('h1a')
        h1b = self.addHost('h1b')
        h1c = self.addHost('h1c')
        self.addLink(h1a, s1)
        self.addLink(h1b, s1)
        self.addLink(h1c, s1)
        # Network 2 (with QoS)
        s2 = self.addSwitch('s2')
        h2a = self.addHost('h2a')
        h2b = self.addHost('h2b')
        h2c = self.addHost('h2c')
        self.addLink(h2a, s2)
        self.addLink(h2b, s2)
        self.addLink(h2c, s2)

def run():
    net = Mininet(topo=DualQoSTopo(), controller=RemoteController, link=TCLink)
    net.start()
    print("Networks are up. You can now run your traffic generation scripts.")
    net.interact()

if __name__ == '__main__':
    setLogLevel('info')
    run()