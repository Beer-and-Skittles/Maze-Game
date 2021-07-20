import random as rnd

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.vst = False
        self.walls = [True, True, True, True]
        # corresonding to the four walls of the cell: top, right, bottom, left

    def visit(self):
        if(not self.vst):
            self.vst = True

    def removeWall(self, dir):

        if(dir == "top"):
            self.walls[0] = False

        elif(dir == "right"):
            self.walls[1] = False

        elif(dir == "bottom"):
            self.walls[2] = False

        elif(dir == "left"):
            self.walls[3] = False

    
class Maze:
    def __init__(self, rows, cols):
        self.r = rows
        self.c = cols

        self.maze = []
        for i in range(rows):
            self.maze.append([])
            for j in range(cols):
                new_cell = Cell(i, j)
                self.maze[-1].append(new_cell)

    def unvisitN(self, cell):   # returns unvisited neighbors
        unvisited = []
        row = cell.row
        col = cell.col
        
        if(col-1>=0):       # checks left
            if(self.maze[row][col-1].vst == False):
                unvisited.append(self.maze[row][col-1])
    
        if(col+1<self.c):  # checks right
            if(self.maze[row][col+1].vst == False):
                unvisited.append(self.maze[row][col+1])

        if(row-1>=0):       # checks top
            if(self.maze[row-1][col].vst == False):
                unvisited.append(self.maze[row-1][col])
        
        if(row+1<self.r):  # checks bottom
            if(self.maze[row+1][col].vst == False):
                unvisited.append(self.maze[row+1][col])
       
        return unvisited

    def removeWall(self, a, b):
        if(a.row > b.row):      # b is top of a
            a.removeWall("top")
            b.removeWall("bottom")

        elif(a.row < b.row):    # b is bottom of a
            a.removeWall("bottom")
            b.removeWall("top")

        elif(a.col > b.col):    # b is left of a
            a.removeWall("left")
            b.removeWall("right")

        elif(a.col < b.col):    # b is right of a
            a.removeWall("right")
            b.removeWall("left")

    def buildMaze(self):

        # choose the initial cell, mark it as visited and push it to stack
        current = self.maze[0][0]
        current.visit()
        cell_stack = []
        cell_stack.append(current)

        while(cell_stack):

            current = cell_stack[-1]
            cell_stack.pop()

            unvisited = self.unvisitN(current)
            if(unvisited):
                cell_stack.append(current)
                chosen = unvisited[rnd.randint(0, len(unvisited)-1)]
                chosen.visit()
                cell_stack.append(chosen)
                self.removeWall(current, chosen)

def main():

    maze_rows = 10
    maze_cols = 10
    maze = Maze(maze_rows,maze_cols)
    maze.buildMaze()

 
if __name__ == '__main__':
        main()
        print("hello")
