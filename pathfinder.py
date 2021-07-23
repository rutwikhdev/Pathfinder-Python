from tkinter import *
from time import sleep


win = Tk()
c = Canvas(width=900, height=900)
gridsize = 25
start = ()
end = ()

###################################################### LOGIC ######################################################

class Maze:
    def __init__(self):
        self.grid = {}

    def addGridEdge(self, key, value):
        if self.grid.get(key) != None:
            edgeList = self.grid[key]
            edgeList.append(value)
        else:
            edgeList = []
            edgeList.append(value)
        self.grid[key] = edgeList

    # Breadth First Search
    def startSearch(self, start, end, visited, stack):
        queue = [[start]]
        global paths
        visited = set()

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                path = path[1:-1]
                for node in path:
                    win.update()
                    c.create_rectangle(node[0]-12.5, node[1]-12.5, node[0]+12.5, node[1]+12.5, fill="skyblue")
                    sleep(0.1)
                return
            elif node not in visited:
                for adjacent in self.grid[node][0]:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
                visited.add(node)

maze = Maze()

######################################################## GUI ######################################################

def validEdges(edges):
    validEdges = []
    for edge in edges:
        if edge[0] > 0 and edge[0] < 900 and edge[1] > 0 and edge[1] < 900:
            validEdges.append(edge)
    return validEdges

x,y = 0,0
for i in range(36):
    for j in range(36):
        c.create_rectangle(x, y, x+gridsize, y+gridsize,  fill="beige")
        edges = []

        midpointx = x + gridsize / 2
        midpointy = y + gridsize / 2

        key = (midpointx, midpointy)

        # ADJACENT NODES
        TS = (midpointx, midpointy - 25)
        BS = (midpointx, midpointy + 25)
        RS = (midpointx + 25, midpointy)
        LS = (midpointx - 25, midpointy)

        # DIAGONAL NODES
        LT = (midpointx - 25, midpointy - 25)
        RT = (midpointx + 25, midpointy - 25)
        RB = (midpointx + 25, midpointy + 25)
        LB = (midpointx - 25, midpointy + 25)

        edges = validEdges([TS,BS,RS,LS,LT,RT,RB,LB])

        maze.addGridEdge(key=key, value=edges)
        x = x + gridsize
    x = 0
    y = y + gridsize

def plotStartEnd(event,pick):
    global start
    global end

    x2 = event.x
    while x2%gridsize != 0:
        x2 += 1
    x1 = x2 - gridsize

    y2 = event.y
    while y2%gridsize != 0:
        y2 += 1
    y1 = y2 - gridsize

    if pick == 'start':
        c.create_rectangle(x1,y1,x2,y2,fill='#7ba659')
        s = (x1+gridsize/2, y1+gridsize/2)
        start = s
    elif pick == 'end':
        c.create_rectangle(x1,y1,x2,y2,fill='#c63939')
        e = (x1+gridsize/2, y1+gridsize/2)
        end = e

def drawPath(event):
    x2 = event.x
    while x2%gridsize != 0:
        x2 += 1
    x1 = x2 - gridsize

    y2 = event.y
    while y2%gridsize != 0:
        y2 += 1
    y1 = y2 - gridsize
    c.create_rectangle(x1,y1,x2,y2,fill='#333333')

    point = (x2-12.5, y2-12.5)
    if point in maze.grid.keys():
        deleteflist = maze.grid[point][0]
        maze.grid.pop(point)
        for el in deleteflist:
            maze.grid[el][0].remove(point)

def start_path():
    global start
    global end
    visited = set()
    maze.startSearch(start, end, visited, [])
    c.create_rectangle(start[0]-12.5, start[1]-12.5, start[1]+12.5, start[1]+12.5)

button = Button(win, text='Start',fg='white', bg='#5852ad',command=start_path)
button.pack(side=BOTTOM)

win.bind("<B1-Motion>", drawPath)
win.bind("<Control-Button-3>", lambda e: plotStartEnd(event=e, pick='end'))
win.bind("<Control-Button-1>", lambda e: plotStartEnd(event=e, pick='start'))

c.pack()
win.mainloop()
