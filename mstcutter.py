#!/usr/bin/python

import networkx as nx
import sys

class MSTCutter:
	def __init__(self, L, U):
		self.u = U
		self.l = L
		self.path = []
		self.visited = set()
		self.unvisited = set()
		self.cum = 0
		self.path = []
		self.comp = []
		self.invalid = False
	def findCuts(self, mst):
		# first remove all edges that the weight is larger than the upper bound
		pieces = []
		num_invalid = 0
		num_invalid = self.topDownCut(mst, pieces, num_invalid)
		if num_invalid > 1:
			print("Can not find a valid split!")
		return (pieces,num_invalid)
	#botom up cut
	def bottomUpCut(self, g):
		pass		
	#Top to bottom cut 
	def topDownCut(self, g, pieces, num_invalid):
		size = 0
		for e in g.edges():
			size += g[e[0]][e[1]]['weight']
		if size <= self.u:
			pieces.append(g.nodes())
			num_invalid += (size < self.l)
		else:				
			smallest = sys.maxint 
			opt_cut = []
			edges = g.edges()
			for e in edges:
				temp = num_invalid
				temp_pieces = []
				w = g[e[0]][e[1]]['weight']
				g.remove_edge(*e)
				components = nx.connected_components(g)
				sub_graphs = []
				for c in components:
					sub_graphs.append(self.buildSubGraph(c,g))
				temp = self.topDownCut(sub_graphs[0], temp_pieces, temp)
				if temp <= smallest:
					temp = self.topDownCut(sub_graphs[1], temp_pieces, temp)
					if temp < smallest:
						opt_cut = temp_pieces
						smallest = temp
				g.add_edge(*e,weight = w)	
			if smallest <= 1:
				pieces += opt_cut
				num_invalid = smallest
			else:
				pieces.append(g.nodes())
				num_invalid += 1
		return num_invalid
	def buildSubGraph(self, nodes, g):
		graph = nx.Graph()
		for n in nodes:
			graph.add_node(n)
			for k in nodes:
				if n < k and g.has_edge(n,k):
					graph.add_edge(n,k, weight = g[n][k]['weight'])	
		return graph
	
if __name__ == '__main__':
	from graph_loader import GraphGenerator as GG
	test_file = "mst_cut_test.csv"
	l = GG(test_file)
	mst = nx.minimum_spanning_tree(l.getGraph())
	l = 5 
	u = 10 
	cutter = MSTCutter(l,u)
	pieces, num_invalid = cutter.findCuts(mst)
	print("# of invalid pieces: " + str(num_invalid))
	for p in pieces:
		print(p)
	#cutter.findCuts(mst)
	#print(cutter.comp)
