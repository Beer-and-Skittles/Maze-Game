import random as rnd

class Maze:

    def __init__(self, rows, cols):
        self.r = rows
        self.c = cols
        self.maze = []
        self.walls = []
        self.psg  = []

        # True for walls, False for passeges
        for i in range(rows):
            self.maze.append([])
            for j in range (cols):
                self.maze[-1].append(True)
    
    def addWalls(self, pos):   # append walls of the given cell to self.wall

        row = pos[0]
        col = pos[1]

        if(row-1>=0 and self.maze[row-1][col]):         # top
            self.walls.append([row-1, col])
        if(col+1<self.c and self.maze[row][col+1]):     # right
            self.walls.append([row, col+1])
        if(row+1<self.r and self.maze[row+1][col]):     # bottom
            self.walls.append([row+1, col])
        if(col-1>=0 and self.maze[row][col-1]):         # left
            self.walls.append([row, col-1])

    def vst(self, pos):    # returns random unvisited cell if only one neighbor is visited
        visited = 0
        unvisited = []
        row = pos[0]
        col = pos[1]

        if(row-1>=0 ):    
            if(self.maze[row-1][col]): 
                unvisited.append([row-1, col])
            else:
                visited += 1

        if(col+1<self.c):
            if(self.maze[row][col+1]):
                unvisited.append([row, col+1])
            else:
                visited += 1

        if(row+1<self.r):
            if(self.maze[row+1][col]):
                unvisited.append([row+1, col])
            else:
                visited += 1

        if(col-1>=0):
            if(self.maze[row][col-1]):
                unvisited.append([row, col-1])
            else:
                visited += 1

        if(visited == 1):
            return unvisited[rnd.randint(0,len(unvisited)-1)]
        return False

    def printMaze(self):
        for row in range(self.r):
            for col in range(self.c):
                if(self.maze[row][col]):    # True:  is wall
                    print('#',end=" ")
                else:                       # False: is passege
                    print(' ',end=" ")
            print()

    def buildMaze(self):

        row = rnd.randint(0, self.r-1 )
        col = rnd.randint(0, self.c-1 )
        self.maze[row][col] = False
        self.addWalls([row, col])

        while(self.walls):
            crnt = self.walls[rnd.randint(0, len(self.walls)-1 )]
            goto = self.vst(crnt)
            if(goto):
                self.maze[crnt[0]][crnt[1]] = False
                self.addWalls(goto)
                self.addWalls(crnt)
            self.walls.remove(crnt)

        self.printMaze()

def main():
    maze = Maze(10,10)
    maze.buildMaze()

if __name__ == '__main__':
    main()