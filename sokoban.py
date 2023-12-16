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
    
def TransferGameStateI(layout):
    # * Transfer the layout of initial puzzle
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    MaxColsNum = max([len(x) for x in layout])
    for IRow in range(len(layout)):
        for ICol in range(len(layout[IRow])):
            if layout[IRow][ICol] == ' ': layout[IRow][ICol] = 0  # * free space
            elif layout[IRow][ICol] == '#': layout[IRow][ICol] = 1  # * wall
            elif layout[IRow][ICol] == '&': layout[IRow][ICol] = 2  # * player
            elif layout[IRow][ICol] == 'B': layout[IRow][ICol] = 3  # * box
            elif layout[IRow][ICol] == '.': layout[IRow][ICol] = 4  # * goal
            elif layout[IRow][ICol] == 'X': layout[IRow][ICol] = 5  # * box on goal
        ColsNum = len(layout[IRow])
        if ColsNum < MaxColsNum:
            layout[IRow].extend([1 for _ in range(MaxColsNum - ColsNum)])
    return np.array(layout)
