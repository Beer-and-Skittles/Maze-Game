import maze_dfs as dfs
import pygame as pg
import random as rnd
import time


screen_h = 800
screen_w = 800
margin_x = 70
margin_y = 70
maze_row = 15
maze_col = 15
sp_x = (screen_w - 2*margin_x)/maze_col
sp_y = (screen_h - 2*margin_y)/maze_row
wall_w   = 3
unit_len = 2
plr_sz   = 10

bg_clr   = (0, 36, 81)      # muted indigo
plr_clr  =   (156, 36, 81)  # wine red
maze_clr = [(235, 187, 255), (255, 197, 143), (255, 238, 164), (115, 201, 145)]
# lavender, pastel orange, pastel yellowm, avocado

def drawMaze(dfs_maze, screen):     # draws maze

    for r in range(maze_row):
        for c in range(maze_col):

            crnt_cell = dfs_maze.maze[r][c]
            color = maze_clr[int(r/maze_row*len(maze_clr))]
            x = margin_x + c*sp_x
            y = margin_y + r*sp_y

            if(crnt_cell.walls[0]): # top wall
                pg.draw.line(screen, color, (x, y), (x+sp_x, y), wall_w)

            if(crnt_cell.walls[1]): # right wall
                pg.draw.line(screen, color, (x+sp_x, y), (x+sp_x, y+sp_y), wall_w)

            if(crnt_cell.walls[2]): # bottom wall
                pg.draw.line(screen, color, (x+sp_x, y+sp_y), (x, y+sp_y), wall_w)

            if(crnt_cell.walls[3]): # left wall
                pg.draw.line(screen, color, (x, y+sp_y), (x, y), wall_w)

def dis(a_x, a_y, b_x, b_y):    # returns distance between two points
    distance = (a_x-b_x)**2 + (a_y-b_y)**2
    distance = distance ** 0.5
    return distance

def inRein(dfs_maze, x, y):     # returns true if the player position is legal

    row = int((y - margin_y)/sp_y) 
    col = int((x - margin_x)/sp_x)
    crnt_cell = dfs_maze.maze[row][col]

    top_y = margin_y + row*sp_y
    btm_y = top_y + sp_y
    left_x = margin_x + col*sp_x
    right_x = left_x + sp_x

    # top
    if(y - plr_sz < top_y and crnt_cell.walls[0]):
        return False
    # bottom
    if(y + plr_sz > btm_y and crnt_cell.walls[2]):
        return False
    # left
    if(x - plr_sz < left_x and crnt_cell.walls[3]):
        return False
    # right
    if(x + plr_sz > right_x and crnt_cell.walls[1]):
        return False
    # top left
    if(dis(x,y,left_x,top_y) < plr_sz):
        return False
    # top right
    if(dis(x,y,right_x,top_y) < plr_sz):
        return False
    # bottom left
    if(dis(x,y,left_x,btm_y) < plr_sz):
        return False
    # bottom right
    if(dis(x,y,right_x,btm_y) < plr_sz):
        return False

    return True

def winGame(x, y):
    row = int((y - margin_y)/sp_y)
    col = int((x - margin_x)/sp_x)
    if(row+1 == maze_row and col+1 == maze_col):
        return True
    return False

def main():

    # init screen
    pg.init(),
    screen = pg.display.set_mode((screen_w ,screen_h))
    screen.fill(bg_clr)

    # init maze
    dfs_maze = dfs.Maze(maze_row, maze_col)
    dfs_maze.buildMaze()
    drawMaze(dfs_maze, screen)

    # init player
    plr_x = margin_x + sp_x/2
    plr_y = margin_y + sp_y/2
    pg.draw.circle(screen, plr_clr, (plr_x, plr_y), plr_sz)

    key_pressed = False
    game = True
    while(game):
        time.sleep(0.005)
        for event in pg.event.get():

            if(event.type == pg.QUIT):
                game = False
            
            if(event.type == pg.KEYUP):
                key_pressed = False

            if(event.type == pg.KEYDOWN):
                key_pressed = True

        if(key_pressed):    # a key is pressed
            if(event.key == pg.K_UP):
                if(inRein(dfs_maze, plr_x, plr_y-unit_len)):
                    plr_y -= unit_len

            elif(event.key == pg.K_DOWN):
                if(inRein(dfs_maze, plr_x, plr_y+unit_len)):
                    plr_y += unit_len

            elif(event.key == pg.K_RIGHT):
                if(inRein(dfs_maze, plr_x+unit_len, plr_y)):
                    plr_x += unit_len

            elif(event.key == pg.K_LEFT):
                if(inRein(dfs_maze, plr_x-unit_len, plr_y)):
                    plr_x -= unit_len
            
            if(winGame(plr_x, plr_y)):
                print("WIN GAME!")
            
            screen.fill(bg_clr)
            pg.draw.circle(screen, plr_clr, (plr_x, plr_y), plr_sz)

        drawMaze(dfs_maze, screen)
        pg.display.update()

if __name__ == '__main__':
    main()