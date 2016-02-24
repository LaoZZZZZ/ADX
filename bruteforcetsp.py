#!/usr/bin/python

import sys
from graph_loader import GraphGenerator
import itertools
class BFTSP:
	def __init__(self,v):
		assert(v > 0)
		self.v = v
	def opt(self, graph):
		optimal_weight = sys.maxint	
		path = []
		nodes = graph.nodes()
		nodes.sort()
		for p in itertools.permutations(nodes):
			tp = [n for n in p] 
			tp.append(tp[0]) 
			is_valid, total_weight = self.checkSolution(tp, graph)
			if is_valid:
				if optimal_weight > total_weight:
					optimal_weight = total_weight
					path = tp		
		return (optimal_weight, path)
	def checkSolution(self, path, graph):
		if len(path) <= 1:
			return True
		prev = path[0] 
		total_weight = 0
		time_interval = (graph.node[prev]['timespan'][0], graph.node[prev]['timespan'][1])
		for n in path[1:]:
			start,end = self.arriveTimeInterval(time_interval[0], time_interval[1],graph[prev][n]['weight'])	
			if not self.isOverlap((start,end), graph.node[n]['timespan']):
				return (False, sys.maxint)	
			total_weight += graph[prev][n]['weight']
			time_interval = (max(graph.node[n]['timespan'][0], time_interval[0]), max(graph.node[n]['timespan'][1], time_interval[1]))
			prev = n
		return (True, total_weight)
	def isOverlap(self, interval1, interval2):
		#return (interval1[0] >= interval2[0] and interval1[0] <= interval2[1]) or
		#	(interval1[1] >= interval2[0] and interval1[1] <= interval2[1])
		return not (interval1[0] > interval2[1]) 
	def arriveTimeInterval(self, start, end, distance):
		time = distance / self.v
		return (start + time, end + time)	
if __name__ == '__main__':
	#f = 'test_graph.csv'
	f = 'dimand_graph.csv'
	g = GraphGenerator(f).getGraph()
	#print(itertools.permutations(nodes))
	solver = BFTSP(10)
	weight, path = solver.opt(g)
	print("Total weight: " + str(weight))
	for p in path:
		print(g.node[p])	

