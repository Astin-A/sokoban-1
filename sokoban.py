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

def PosOfPlayer(GameState): # * Return the position of agent
    return tuple(np.argwhere(GameState == 2)[0]) #! for example (2, 2)


def PosOfBoxes(GameState): # * Return the positions of boxes
    return tuple(tuple(x) for x in np.argwhere((GameState == 3) | (GameState == 5))) #! for example ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5))


def PosOfWalls(GameState): # * Return the positions of walls
    return tuple(tuple(x) for x in np.argwhere(GameState == 1)) #! like those above


def PosOfGoals(GameState): # * Return the positions of goals
    return tuple(tuple(x) for x in np.argwhere((GameState == 4) | (GameState == 5))) #! like those above


def IsEndState(PosBox): # * Check if all boxes are on the goals (that is pass the game)
    return sorted(PosBox) == sorted(PosGoals)

def IsLeagalAction(action, PosPlayer, PosBox): # * Check if the given action is legal
    xPlayer, yPlayer = PosPlayer
    if action[-1].isupper(): #! the move was a push
        x1 , y1 = xPlayer + 2 * action[0], yPlayer + 2 * action[1]
    else:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
    return (x1,y1) not in PosBox + PosWalls

def LeagalActions(PosPlayer, PosBox): # * Return all legal actions for the agent in the current game state
    AllActions = [[-1,0,'u','U'],[1,0,'d','D'],[0,-1,'l','L'],[0,1,'r','R']]
    xPlayer, yPlayer = PosPlayer
    LeagalActions = []
    for action in AllActions:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
        if (x1, y1) in PosBox: #! the move was a push
            action.pop(2) #! drop the little letter
        else:
            action.pop(3) #! drop the upper letter
        if IsLeagalAction(action, PosPlayer, PosBox):
            LeagalActions.append(action)
        else:
            continue
    return tuple(tuple(x) for x in LeagalActions) #! for example ((0, -1, 'l'), (0, 1, 'R'))


def UpdateState(PosPlayer, PosBox, action): # * Return updated game state after an action is taken
    xPlayer, yPlayer = PosPlayer #! the previous position of player
    NewPosPlayer = [xPlayer + action[0], yPlayer + action[1]] #? the current position of player
    PosBox = [list(x) for x in PosBox]
    if action[-1].isupper(): #! if pushing, update the position of box
        PosBox.remove(NewPosPlayer)
        PosBox.append([xPlayer + 2 * action[0], yPlayer + 2 * action[1]])
    PosBox = tuple(tuple(x) for x in PosBox)
    NewPosPlayer = tuple(NewPosPlayer)
    return NewPosPlayer, PosBox


def IsFailed(PosBox): # * This function used to observe if the state is potentially failed, then prune the search
    RotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
    
    FlipPattern = [[2,1,0,5,4,3,8,7,6],
                    [0,3,6,1,4,7,2,5,8],
                    [2,1,0,5,4,3,8,7,6][::-1],
                    [0,3,6,1,4,7,2,5,8][::-1]]
    
    AllPatterns = RotatePattern + FlipPattern

    for box in PosBox:
        if box not in PosGoals:
            board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                    (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
            for pattern in AllPatterns:
                NewBoard = [board[i] for i in pattern]
                if NewBoard[1] in PosWalls and NewBoard[5] in PosWalls: return True
                elif NewBoard[1] in PosBox and NewBoard[2] in PosWalls and NewBoard[5] in PosWalls: return True
                elif NewBoard[1] in PosBox and NewBoard[2] in PosWalls and NewBoard[5] in PosBox: return True
                elif NewBoard[1] in PosBox and NewBoard[2] in PosBox and NewBoard[5] in PosBox: return True
                elif NewBoard[1] in PosBox and NewBoard[6] in PosBox and NewBoard[2] in PosWalls and NewBoard[3] in PosWalls and NewBoard[8] in PosWalls: return True
        return False
    
    
#* Implement all approcahes


def BreadthFirstSearch(): #* Implement breadthFirstSearch approach
    beginBox = PosOfBoxes(GameState)
    beginPlayer = PosOfPlayer(GameState)

    StartState = (beginPlayer, beginBox) #! for example ((2, 2), ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5)))
    frontier = collections.deque([[StartState]]) #! store states
    actions = collections.deque([[0]]) #! store actions
    ExplordSet = set()
    while frontier:
        node = frontier.popleft()
        node_action = actions.popleft()
        if IsEndState(node[-1][-1]):
            print(','.join(node_action[1:]).replace(',',''))
            break
        if node[-1] not in ExplordSet:
            ExplordSet.add(node[-1])
            for action in LeagalActions(node[-1][0], node[-1][1]):
                NewPosPlayer, NewPosBox = UpdateState(node[-1][0], node[-1][1], action)
                if IsFailed(NewPosBox):
                    continue
                frontier.append(node + [(NewPosPlayer, NewPosBox)])
                actions.append(node_action + [action[-1]])


def DepthFirstSearch(): #* Implement depthFirstSearch approach
    beginBox = PosOfBoxes(GameState)
    beginPlayer = PosOfPlayer(GameState)

    StartState = (beginPlayer, beginBox)
    frontier = collections.deque([[StartState]])
    ExplordSet = set()
    actions = [[0]]
    while frontier:
        node = frontier.pop()
        node_action = actions.pop()
        if IsEndState(node[-1][-1]):
            print(','.join(node_action[1:]).replace(',',''))
            break
        if node[-1] not in ExplordSet:
            ExplordSet.add(node[-1])
            for action in LeagalActions(node[-1][0], node[-1][1]):
                NewPosPlayer, NewPosBox = UpdateState(node[-1][0], node[-1][1], action)
                if IsFailed(NewPosBox):
                    continue
                frontier.append(node + [(NewPosPlayer, NewPosBox)])
                actions.append(node_action + [action[-1]])



def heuristic(PosPlayer, PosBox): #* A heuristic function to calculate the overall distance between the else boxes and the else goals
    distance = 0
    completes = set(PosGoals) & set(PosBox)
    SortPosBox = list(set(PosBox).difference(completes))
    SortPosGoals = list(set(PosGoals).difference(completes))
    for i in range(len(SortPosBox)):
        distance += (abs(SortPosBox[i][0] - SortPosGoals[i][0])) + (abs(SortPosBox[i][1] - SortPosGoals[i][1]))
    return distance
