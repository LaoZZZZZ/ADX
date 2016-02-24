#!/usr/bin/python

import scipy.spatial.distance as dlib 
from components import Component
import sys
def euclideanDistance(x,y):
	return dlib.euclidean(x,y)
def pairDistance(node1, node2, graph):
	return graph[node1][node2]['weight']
def shortestDistance(node1, comp, graph):
	shortest = sys.maxint   
	for n in comp.nodes():
		shortest = min(graph[n][node1]['weight'], shortest)
	return shortest
if __name__ == '__main__':
	x = [1,2,3]
	y = [1,2,4]
	print(euclideanDistance(x,y))
