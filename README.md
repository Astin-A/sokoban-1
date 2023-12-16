# sokoban 1
 

 A sokoban game solver
===========================
This project proposed a AI solver for sokoban (japanese for warehouse keeper) which is a difficult computational problem. The algorithm being used consisted of BFS (breadth first search), DFS (depth first search), UCS (uniform cost search) and A* (a star search).


## Table of contents

* [0. How to use](#0)


<a id="0"></a>
## 0. How to use

1. The libraries that need to be imported are: sys, collections, numpy, heapq, time

2. Download it locally and run the `sokoban.py` file.


### Visual help


```
$ python sokoban.py --help
```
```
Usage: sokoban.py [options]
Options:
  -h, --help            show this help message and exit
  -l SOKOBANLEVELS, --level=SOKOBANLEVELS
                        level of game to play (test1-10.txt, level1-5.txt)
  -m AGENTMETHOD, --method=AGENTMETHOD
                        research method (bfs, dfs, ucs, astar)
```

`-l`: The map is divided into test and level. Test is relatively simple, and level is more difficult.
`-m`: The search algorithm is bfs, dfs, ucs or astar.


### Run the examples

```
$ python sokoban.py -l test1.txt -m bfs
```
```
rUUdRdrUUluL
Runtime of bfs: 0.15 second.
```

The first line of output is the action of the box pusher. `u`, `d`, `l` and `r` represent the movements up, down, left and right respectively. The corresponding capital letters represent pushing the box in that direction. move. The second line of output is the running time of the program.

