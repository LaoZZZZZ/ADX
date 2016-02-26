#!/usr/bin/python

class IntervalPermutation:
	def __init__(self, intervals, index):
		self.intervals = []
		self.index = []
		temp = zip(intervals, index)
		def compare(x,y):
			if x[0][1] < y[0][1]:
				return -1 
			elif x[0][1] == y[0][1]:
				return -1 
			else:
				return 1 
		temp.sort(cmp = compare)
		for e in temp:
			self.intervals.append(e[0])
			self.index.append(e[1])
		self.permutate()
	def permutate(self):
		self.permutations = []
		self.dfs(0)
	def next_permutation(self):
		for p in self.permutations:
			yield p
	def dfs(self, start):
		if start >= len(self.intervals) - 1:
			self.permutations.append([n for n in self.index])
		else:
			for index in range(start, len(self.index)):
				self.index[start], self.index[index] = self.index[index],self.index[start]
				#print(self.index,[self.intervals[n] for n in self.index], start, index,self.checkValid(start,index))
				if self.checkValid(start, index):
					self.dfs(start + 1) 
				self.index[start], self.index[index] = self.index[index],self.index[start]
	def isValid(self, interval_1, interval_2):
		return not (interval_1[0] >= interval_2[1])
	def checkValid(self, start, end):
		for i in range(start, end):
			if not self.isValid(self.intervals[self.index[i]], self.intervals[self.index[i + 1]]):
				return False
		return True

if __name__ == '__main__':
	#intervals = [[1,2],[0,2],[3,4],[7,8],[5,6]]
	#intervals = [[1,2],[0,2],[0,1],[3,4],[5,6],[2,7],[4,6]]
	#index = [0,1,2,3,4,5,6]

	intervals = [[1,2],[0,1],[3,4],[5,6],[2,7]]
	index = [0,1,2,3, 4]
	
	#intervals = [[1,2],[3,4],[5,6]]
	#index = [0,1,2]
	perGen = IntervalPermutation(intervals[:], index[:])
	for p in perGen.next_permutation():
		print(p)
		instance = [intervals[n] for n in p]
		print(instance)
