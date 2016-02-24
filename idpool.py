#!/usr/bin/python

class IDPool:
	def __init__(self, used):
		self.used = set(used)	
		self.start = max(self.used) + 1
	def nextId(self):
		temp = self.start
		self.start += 1
		return temp	

if __name__ == '__main__':
	pool = [2,5,10]
	
	idpool = IDPool(pool)
	for i in range(10):
		print(idpool.nextId())

