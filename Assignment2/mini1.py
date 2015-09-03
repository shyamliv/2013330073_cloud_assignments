#!/usr/bin/python
from mininet.topo import Topo
from mininet.node import OVSController
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
X=0
Y=0
class LinearTopo(Topo):
	"Topology of Y switches, with two hosts per switch and all switches connected to each other in a loop."
	def __init__(self, k=Y, **opts):
		"""Init.
		k: number of switches (and hosts)
		hconf: host configuration options
		lconf: link configuration options"""
		super(LinearTopo, self).__init__(**opts)
		self.k =k
		lastSwitch =None
		t=1
		first=None
		for i in irange(1, k):
			host1 =self.addHost('h%s'%t)
			t=t+1
			host2=self.addHost('h%s'%t)
			t=t+1
			switch =self.addSwitch('s%s'%i)
			if i==1:
			    first=switch
			self.addLink(host1, switch, bw=1, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
			self.addLink(host2, switch, bw=2)

			if lastSwitch:
				self.addLink(switch, lastSwitch)
			lastSwitch =switch
		self.addLink(switch,first)
	        '''making the circular topology above'''

def perfTest():
		"Create network and run simple performance test"
		topo =LinearTopo(k=Y)
		net =Mininet(topo=topo, host=CPULimitedHost, link=TCLink,controller=OVSController)
		count=1
		for i in range(1,X+1,2):
			stri="h"
			stri2="127.0.0."
			stri2=stri2+str(count)
			count=count+1
			stri=stri+str(i)
			hi=net.get(stri)
			hi.setIP(stri2,24)
		count=1
		for i in range(2,X+1,2):
			stri="h"
			stri2="192.168.0."
			stri=stri+str(i)
			stri2=stri2+str(count)
			count=count+1
			hi=net.get(stri)
			hi.setIP(stri2,29)

		net.start()
		print "Dumping host connections"
		dumpNodeConnections(net.hosts)
		print "Testing network connectivity"
		net.pingAll()
		net.stop()

if __name__ =='__main__':
    X=int(raw_input("Enter number of hosts"))
    Y=int(raw_input("Enter number of switches"))
    setLogLevel('info')
    perfTest()
