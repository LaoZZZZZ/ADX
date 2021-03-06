#!/usr/bin/python

import networkx as nx
from graph_loader import GraphGenerator as GG
class tspSolver:
	def __init__(self, complete_graph):
		self.completeGraph = complete_graph
	def traverse(self, graph, start):
		self.reset()
		self.graph = nx.minimum_spanning_tree(graph)
		self.dfs(start)
		for n in self.graph.nodes():
			if n != start:
				self.dfs(n)
		return (self.total, self.path) 		
	def reset(self):
		self.total = 0
		self.visited = set() 
		self.last_visited = None
		self.path = []
	def dfs(self, n):
		if n in self.visited:
			return
		else:
			if self.last_visited != None:
				self.total += self.completeGraph[self.last_visited][n]['weight']
			self.last_visited = n		
			self.path.append(self.last_visited)
			self.visited.add(n)
			for neib in self.graph.neighbors(n):
				self.dfs(neib) 	
if __name__ == '__main__':
	f = 'mst_test.csv'
	l = GG(f)
	complete_graph = l.getGraph()
	solver = tspSolver(complete_graph)
	print(solver.traverse(complete_graph))
