import numpy as np
import random as rnd
import pygame as pg
from enum import Enum

class Nbr(Enum):
    TOP = 0
    RIGHT = 1
    BTM = 2
    LEFT = 3

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.vst = False
        self.walls = [True, True, True, True]
        # corresonding to the four walls of the cell: top, right, bottom, left
    
class Maze:
    def __init__(self, rows, cols):
        self.r = rows
        self.c = cols

        self.maze = []
        for i in range(rows):
            self.maze.append([])
            for j in range(cols):
                new_cell = Cell(i,j)
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
            a.walls[0] = False
            b.walls[2] = False

        elif(a.row < b.row):    # b is bottom of a
            a.walls[2] = False
            b.walls[0] = False

        elif(a.col > b.col):    # b is left of a
            a.walls[3] = False
            b.walls[1] = False

        elif(a.col < b.col):    # b is right of a
            a.walls[1] = False
            b.walls[3] = False

    def buildMaze(self):

        # choose the initial cell, mark it as visited and push it to stack
        current = self.maze[0][0]
        current.vst = True
        cell_stack = []
        cell_stack.append(current)

        while(cell_stack):

            current = cell_stack[-1]
            cell_stack.pop()

            unvisited = self.unvisitN(current)
            if(unvisited):
                chosen = unvisited[rnd.randint(0, len(unvisited)-1)]
                chosen.vst = True
                cell_stack.append(chosen)
                self.removeWall(current, chosen)


if __name__ == '__main__':
        maze = Maze(30,20)
        maze.buildMaze()
        print("hello!")