import time
import random as rnd
import pygame as pg

line_clr = (255,157,156)
vst_clr = (0,52,110)
un_clr = (0,28,64)
bg_clr = (0,36,81)


class Cell:
    def __init__(self, row, col, scrn, pos, sz):
        self.row = row
        self.col = col
        self.scrn = scrn
        self.pos = pos
        self.sz = sz
        self.lw = 3
        self.vst = False
        self.walls = [True, True, True, True]
        # corresonding to the four walls of the cell: top, right, bottom, left

        pg.draw.rect(scrn, un_clr, pg.Rect(pos[0], pos[1], sz[0], sz[1]))
        pg.draw.line(scrn, line_clr, (pos[0],pos[1]), (pos[0]+sz[0],pos[1]), self.lw)
        pg.draw.line(scrn, line_clr, (pos[0]+sz[0],pos[1]), (pos[0]+sz[0],pos[1]+sz[1]), self.lw)
        pg.draw.line(scrn, line_clr, (pos[0]+sz[0],pos[1]+sz[1]), (pos[0],pos[1]+sz[1]), self.lw)
        pg.draw.line(scrn, line_clr, (pos[0],pos[1]+sz[1]), (pos[0],pos[1]), self.lw)
    
    def visit(self):
        if(not self.vst):
           
            scrn = self.scrn
            pos = self.pos
            sz = self.sz
            lw = self.lw

            self.vst = True
            pg.draw.rect(scrn, vst_clr, pg.Rect(pos[0], pos[1], sz[0], sz[1]))
            pg.draw.line(scrn, line_clr, (pos[0],pos[1]), (pos[0]+sz[0],pos[1]), lw)
            pg.draw.line(scrn, line_clr, (pos[0]+sz[0],pos[1]), (pos[0]+sz[0],pos[1]+sz[1]), lw)
            pg.draw.line(scrn, line_clr, (pos[0]+sz[0],pos[1]+sz[1]), (pos[0],pos[1]+sz[1]), lw)
            pg.draw.line(scrn, line_clr, (pos[0],pos[1]+sz[1]), (pos[0],pos[1]), lw)

    def removeWall(self, dir):
        scrn = self.scrn
        pos = self.pos
        sz = self.sz
        lw = self.lw

        if(dir == "top"):
            self.walls[0] = False
            pg.draw.line(scrn, vst_clr, (pos[0],pos[1]), (pos[0]+sz[0],pos[1]), lw)

        elif(dir == "right"):
            self.walls[1] = False
            pg.draw.line(scrn, vst_clr, (pos[0]+sz[0],pos[1]), (pos[0]+sz[0],pos[1]+sz[1]), lw)

        elif(dir == "bottom"):
            self.walls[2] = False
            pg.draw.line(scrn, vst_clr, (pos[0]+sz[0],pos[1]+sz[1]), (pos[0],pos[1]+sz[1]), lw)

        elif(dir == "left"):
            self.walls[3] = False
            pg.draw.line(scrn, vst_clr, (pos[0],pos[1]+sz[1]), (pos[0],pos[1]), lw)
    
class Maze:
    def __init__(self, rows, cols, scrn, scrn_sz, margin):
        self.r = rows
        self.c = cols
        self.scrn = scrn

        spacing = ((scrn_sz[0]-margin[0]*2)/cols, (scrn_sz[1]-margin[1]*2)/rows)
        self.maze = []
        for i in range(rows):
            self.maze.append([])
            for j in range(cols):
                new_cell = Cell(i, j, scrn, (margin[0]+spacing[0]*j, margin[1]+spacing[1]*i), spacing)
                self.maze[-1].append(new_cell)
        pg.display.flip()

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
                pg.display.flip()
                time.sleep(0.02)


def main():

    maze_rows = 10
    maze_cols = 10
    scrn_sz = (600,600)
    margin = (50,50)

    pg.init()
    screen = pg.display.set_mode(scrn_sz)
    screen.fill(bg_clr)
    pg.display.update()
    maze = Maze(maze_rows,maze_cols,screen,scrn_sz,margin)
    maze.buildMaze()

    game = True
    while(game):
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                game = False
 
if __name__ == '__main__':
        main()
        print("hello")
