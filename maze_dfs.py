import numpy as np
import pygame

class Cells:
    def __init__(self):
        self.vst = False
        self.walls = [True, True, True, True]
    
class Maze:
    def __init__(self, rows, cols):
        self.r = rows
        self.c = cols

        self.maze = []
        for i in range(rows):
            self.maze.append([])
            for j in range(cols):
                new_cell = Cells()
                self.maze[-1].append(new_cell)

    def unvisitN(self, row, col):
        try:
            if(self.maze[row-1][col-1].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row][col-1].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row+1][col-1].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row-1][col+1].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row][col+1].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row+1][col+1].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row-1][col].vst == False):
                return True
        except:
            pass

        try:
            if(self.maze[row+1][col].vst == False):
                return True
        except:
            pass
        
        return False

    def buildMaze(self):
        current = [0, 0]



if __name__ == '__main__':
        maze = Maze(2,2)
        print(maze.unvisitN(2,2))
        print("hello!")