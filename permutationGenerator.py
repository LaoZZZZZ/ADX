#!/usr/bin/python

import networkx as nx

class PermutationGenerator:
	def __init__(self, intervals, index):
		self.graph = nx.DiGraph()
		for i in range(len(index)):
			for j in range(i + 1, len(index)):
				if self.isValid(intervals[i], intervals[j]):
					self.graph.add_edge(index[i], index[j])
				if self.isValid(intervals[j], intervals[i]):
					self.graph.add_edge(index[j], index[i])
		self.permutations = []
		self.visited = set()
		self.path = []
	def isValid(self, in_1, in_2):
		return not (in_1[0] >= in_2[1])
	def permutate(self):
		for n in self.graph.nodes():
			for p in self.dfs(n):
				yield p
	def dfs(self, n):
		self.visited.add(n)
		self.path.append(n)
		for neib in self.graph.neighbors(n):
			if not neib in self.visited:
				for p in self.dfs(neib):
					yield p
		if len(self.path) == len(self.graph):
			yield self.path
		del self.path[-1]
		self.visited.remove(n)
	def next_permutation(self):
		for p in self.permutations:
		#for p in self.permutate():
			yield p
if __name__ == '__main__':
	
	intervals = [[0,1],[0,2],[3,7],[4,7]]
	index = [0,1,2,3]
	gen = PermutationGenerator(intervals, index)
	#for p in gen.next_permutation():
	for p in gen.permutate():
		print(p)	
		print([intervals[n] for n in p])
				
