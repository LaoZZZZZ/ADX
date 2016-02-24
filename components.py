#!/usr/bin/python

import networkx as nx
#from distance_metric import euclideanDistance as distance
class Component:
	def __init__(self, cid):
		self.graph = nx.Graph()
		self.size = 0
		self.cid = cid
	def add_node(self, n):
		self.graph.add_node(n)
	def add_edge(self, start, end, w):
		self.graph.add_edge(start, end, weight = w)	
		self.size += w
	def edges(self):
		for e in self.graph.edges():
			yield (e[0], e[1], self.graph[e[0]][e[1]]) 
	def __len__(self):
		return self.size
	def nodes(self):
		for n in self.graph:
			yield n
	def componentID(self):
		return self.cid	
	def edge(self,n1,n2):
		return self.graph[n1][n2]
	
if __name__ == '__main__':
	com = Component(0)
	print(com.componentID())
	com.add_node(10)
	com.add_node(11)
	com.add_edge(10, 11, 1)
	com.add_node(12)
	com.add_edge(10, 12, 2)
	print(len(com))
	for n in com.nodes():
		print(n)				
	print(com.edge(10,11))
	for e in com.edges():
		print(e)
	
