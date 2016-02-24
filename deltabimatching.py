#!/usr/bin/python

import networkx as nx
from idpool import IDPool
class DeltaBiMatching:
	def __init__(self, delta):
		self.delta = delta
	def match(self, graph):
		red_nodes = []
		green_nodes = []
		self.mapping = {}
		delta_graph = graph.copy()
		idpool = IDPool(graph.nodes())	
		for n in graph.nodes():
			if 'color' not in graph.node[n] or graph.node[n]['color'] != 'red':
				continue
			# floating nodes
	
			self.mapping[n] = n
			for i in range(self.delta):
				nextid = idpool.nextId()
				delta_graph.add_node(nextid)
				self.mapping[nextid] = n
				for neib in graph.neighbors(n):
					delta_graph.add_edge(nextid, neib)
		matched_pair = nx.bipartite.maximum_matching(delta_graph)	
		return self.findConnected([(self.mapping[s],e) for s,e in matched_pair.items() if s in self.mapping])
	def findConnected(self, matched_pair):
		g = nx.Graph()
		g.add_edges_from(matched_pair)
		components = nx.connected_components(g)
		flattened_g = []
		for c in components:
			flattened_g.append([n for n in c])
		return flattened_g		

if __name__ == '__main__':
	g = nx.Graph()
	g.add_node(1,color = 'red')
	g.add_node(2,color = 'red')
	g.add_node(3,color = 'red')
	g.add_edge(1,5)
	g.add_edge(1,6)
	g.add_edge(3,5)
	g.add_edge(3,10)
	g.add_edge(2,7)
	g.add_edge(2,9)
	delta = 3 
	matcher = DeltaBiMatching(delta)
	components = matcher.match(g)
	print(components)
					
				
		
				
				
