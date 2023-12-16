import sys
import collections
import numpy as np 
import heapq
import time


class PriorityQueue:
    # * Define a PriorityQueue data structure that will be used
    def __init__(self):
        self.Heap = []
        self.Count = 0


    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1


    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap)
        return item
    
    def IsEmpty(self):
        return len(self.Heap) == 0
    

# * Load puzzles and define the rules of sokoban
