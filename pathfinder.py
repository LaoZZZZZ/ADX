#!/usr/bin/python

import sys
import os

import networkx as nx

from graph_loader import GraphGenerator as GG
from deltabimatching import DeltaBiMatching as DBM
from tsptraverser import tspSolver
from mstcutter import MSTCutter
from idpool import IDPool
from operator import itemgetter

class PathFinder:
	def __init__(self, graph, c1, c2, B, L, delta = None):
		self.graph = graph
		self.completeGraph = graph.copy()
		if not delta:
			self.delta = 4 * c2/c1
		else:
			self.delta = delta
		self.c1 = c1
		self.c2 = c2
		self.L = L
		self.B = B
		self.fixGraph = nx.Graph()
		self.floating_nodes = []
		self.duplicates = {}
		self.path = []
		self.comp_index = {}
	# check if the nodes has the fixed time span
	def isFixed(self, n):
		return self.graph.node[n]['timespan'][0] == 0 and self.graph.node[n]['timespan'][1] == self.L

	# find all floating nodes that have same time interval
	# Only keep one such nodes for each duplicate group
	# remove all others from the original graph
	def duplicateNode(self):
		duplicates = {}
		for n in self.graph.nodes():
			if self.isFixed(n):
				continue
			x,y = self.graph.node[n]['timespan']	
			key = '-'.join([str(x), str(y)])
			duplicates.setdefault(key, [])
			duplicates[key].append(n)
		# remove the duplicate nodes and its edgeds
		# only keep one copy.
		for key, nodes in duplicates.items():
			for n in range(1,len(nodes)):
				self.graph.remove_node(nodes[n])
			self.duplicates[nodes[0]] = nodes

	# Color all fixed range nodes as green.
	# Color all floating range nodes as red. 
	def colorGraph(self):
		for n in self.graph.nodes():
			if self.isFixed(n):
				self.graph.node[n]['color'] = 'green'
				self.fixGraph.add_node(n, position = self.graph.node[n]['position'], timespan = self.graph.node[n]['timespan']
)
			else:
				self.graph.node[n]['color'] = 'red' 
				self.floating_nodes.append(n)
		for n in self.fixGraph.nodes():
			for left in self.fixGraph:
				if left < n:
					self.fixGraph.add_edge(n, left, weight = self.graph[n][left]['weight'])

	# Form a minimum spanning tree for those fixed nodes
	# Cut this mst into pieces.
	def cutGraph(self):
		# Starts to cut the MST
		mst = nx.minimum_spanning_tree(self.fixGraph)
		mst_cutter = MSTCutter(self.c1 * self.B, self.c2*self.B)
		#components,num_invalid_comp = mst_cutter.findCuts(tsp)	
		num_invalid_comp,components, weights = mst_cutter.cutFromTSP(mst,self.completeGraph)	
		#print("Number of invalid pieces: " + str(num_invalid_comp))
		#print("Weights at each pieces: " + ','.join(map(str, weights)))
		#print("Cutted pieces:")
		self.id_pool = IDPool(self.graph.nodes())
		for c in components:
			self.comp_index[self.id_pool.nextId()] = c

	# Build the bipartie graph.
	# Find the maximum bipartie matching.
	def matching(self):
		# build the initial bipartie graph
		self.bi_graph = nx.Graph()
		for red_node in self.floating_nodes:
			self.bi_graph.add_node(red_node, color = 'red')
			for index, com in self.comp_index.items():
				shortest_dist = sys.maxint
				for fixed_node in com:
					shortest_dist = min(shortest_dist, self.graph[red_node][fixed_node]['weight'])
				if self.B >= shortest_dist:
					self.bi_graph.add_edge(red_node, index)  		
		matcher = DBM(self.delta)	
		matched_com = matcher.match(self.bi_graph)
		self.sub_region = {}
		for connected_com in matched_com:
			sub = []
			head = None
			for c in connected_com:
				if c in self.comp_index:
					sub += self.comp_index[c]
				else:
					assert(head == None)
					head = c
					sub += self.duplicates[c]
			self.sub_region[head] = sub	

	# traverse each components
	def traversePath(self):
		self.total_cost = 0
		prev = None
		tsp_solver = tspSolver(self.completeGraph)
		start = None
		headers = [(n,self.completeGraph.node[n]) for n in self.duplicates.keys()]
		headers.sort(key = lambda x :x[1]['timespan'][0]) 
		self.block_weight = []
		for head in headers:
			if prev:
				self.total_cost += self.completeGraph[prev][head[0]]['weight']
				self.block_weight.append(self.completeGraph[prev][head[0]]['weight'])
			else:
				start = head[0]
				prev = head[0]
			sub = []
			if head[0] in self.sub_region:
				sub = self.sub_region[head[0]]
			else:
				sub = self.duplicates[head[0]]
			cost,path = tsp_solver.traverse(self.buildSubGraph(sub), head[0])
			self.block_weight.append(cost)
			self.total_cost += cost
			self.path += path
			prev = self.path[-1]		
	def buildSubGraph(self, nodes):
		graph = nx.Graph()
		for n in nodes:
			graph.add_node(n)
			for k in nodes:
				if n < k and self.completeGraph.has_edge(n,k):
					graph.add_edge(n,k, weight = self.completeGraph[n][k]['weight'])	
		return graph
	
	def findPath(self):
		self.duplicateNode()
		self.colorGraph()	
		self.cutGraph()
		self.matching()
		self.traversePath()
		return self.total_cost

if __name__ == '__main__':
	#f = 'test_graph.csv'
	import time
	start = time.time()
	f = 'input3.csv'
	#f = 'input2.csv'
	gg = GG(f)
	graph = gg.getGraph()
	c1 = 1
	c2 = 2 
	B = 110 
	L = 4 
	finder = PathFinder(graph, c1, c2, B, L, None) 	
	finder.findPath()
	print(finder.total_cost)
	print(finder.path)
	for p in finder.path:
		print(finder.completeGraph.node[p])
	print(finder.block_weight)
	print(time.time() - start)

