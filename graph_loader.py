#!/usr/bin/python

import networkx as nx
from distance_metric import euclideanDistance as distance
class GraphGenerator:
	def __init__(self, file):
		self.file = file
		self.load()
		self.generate()
	def getGraph(self):
		return self.graph
	def generate(self):
		self.graph = nx.Graph()
		for index in range(len(self.nodes)):
			self.graph.add_node(index)
			self.graph.node[index]['position'] = self.nodes[index][0:2]
			self.graph.node[index]['timespan'] = self.nodes[index][2:4]		
			for left in range(index + 1, len(self.nodes)):
				dist = distance(self.nodes[index][0:2], self.nodes[left][0:2])
				self.graph.add_edge(index, left,weight = dist)	
	def load(self):
		self.nodes = []
		for line in open(self.file,'r'):
			node = map(float,line.strip().split(','))
			self.nodes.append(node)	
	def buildSubGraph(self, nodes):
		g = nx.Graph()
		for s in range(len(nodes)):
			g.add_node(nodes[s])
			for e in range(s + 1, len(nodes)):
				g.add_edge(nodes[s], nodes[e], weight = self.graph[nodes[s]][nodes[e]]['weight'])
		return g
if __name__ == '__main__':
	f = "test_graph.csv"
	gen = GraphGenerator(f)
	g = gen.getGraph()
	subset = []
	for n in g.nodes():
		if n % 2:
			subset.append(n)
		print(g.node[n])
	subgraph = gen.buildSubGraph(subset)
	
	for e in subgraph.edges(data = 'weight'):
		print(e)
		print(subgraph[e[1]][e[0]])
			
