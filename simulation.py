#!/usr/bin/python

import os
import sys
import getopt
import time

from graph_loader import GraphGenerator
from pathfinder import PathFinder
from bruteforcetsp import BFTSP

def simulation():
	inputfile = ''
	c1 = 1
	c2 = 2
	delta = 4
	B = 0
	L = 0 
	try:
		opt, args = getopt.getopt(sys.argv[1:],"f:c:d:v:l:h",["help"])
	except:
		print("Invalid parameters!")
		sys.exit()
	for o, a in opt:
		if o == '-f':
			inputfile = a
		elif o == 'c':
			c1,c2 = map(float,a.split(','))
		elif o == '-d':
			try:
				d = float(a)
			except:
				print("invalid delta parameter!")
				sys.exit()
		elif o == '-v':
			try:
				B = float(a)
			except:
				print("Invalid speed specification!")
				sys.exit()
		elif o == '-l':
			try:
				L = float(a)
			except:
				print("Invalid time interval bound!")
				sys.exit()
		elif o in ['-h','--help']:
			usage()
			sys.exit()
	# Get the optimum solution
	complete_graph = GraphGenerator(inputfile).getGraph()
	'''
	start = time.time()
	opt_alg = BFTSP(B)
	opt_weight, opt_path = opt_alg.opt(complete_graph)
	print("Optimal running time : ", time.time() - start)
	print("Optimal weight, " + str(opt_weight))
	print("Optimal path, " + ','.join(map(str,opt_path)))	
	'''
	# Get the approximate solution
	start = time.time()
	path_finder = PathFinder(complete_graph, c1, c2, B, L, delta)
	print("Approximate algorithm running time: ", time.time() - start)
	aprox_weight = path_finder.findPath()
	aprox_path = path_finder.path
	accumulate_weight = path_finder.block_weight
	print("Appoximate weight, " + str(aprox_weight))
	print("Approximate path, " + ','.join(map(str,aprox_path)))	
	print("Accumulate weight, " + ','.join(map(str,accumulate_weight)))	
	
def usage():
	print ('-f: the input graph file. This file should have four columns, which are x,y,start,end respectively')
	print ('-c: The C parameters. c1 and c2 and separated by a comma')
	print ('-d: The delta valud. default equals 4 * c2 / c1')
	print ('-v: Speed parameter')
	print ('-l: The right end for the fixed time interval')
if __name__ == '__main__':
	simulation()		
