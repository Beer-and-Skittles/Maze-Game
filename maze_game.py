import maze_dfs as dfs
import game_bar as gb
import pygame as pg
import random as rnd
import time


field_h = 800
field_w = 800
gm_bar_h = 200
margin_x = 70
margin_y = 70 
maze_row = 5
maze_col = 5
sp_x = (field_w - 2*margin_x)/maze_col
sp_y = (field_h - 2*margin_y)/maze_row
wall_w   = 3
unit_len = 1
plr_sz   = 10

bg_clr   = (0, 36, 81)      # muted indigo
plr_clr  = (156, 36, 81)    # wine red
txt_clr  = (153, 255, 255)  # azure
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
    return pow( pow(a_x-b_x, 2) + pow(a_y-b_y, 2), 0.5)

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

def maskup(screen):
    for r in range(maze_row):
        for c in range(maze_col):
            color = maze_clr[int(r/maze_row*len(maze_clr))]
            x = margin_x + c*sp_x
            y = margin_y + r*sp_y

            pg.draw.line(screen, color, (x, y), (x+sp_x, y), wall_w)
            pg.draw.line(screen, color, (x+sp_x, y), (x+sp_x, y+sp_y), wall_w)
            pg.draw.line(screen, color, (x+sp_x, y+sp_y), (x, y+sp_y), wall_w)
            pg.draw.line(screen, color, (x, y+sp_y), (x, y), wall_w)

def colorSwap(img, old_clr, new_clr):
    new_img = pg.Surface(img.get_size())
    new_img.fill(new_clr)
    img.set_colorkey(old_clr)
    new_img.blit(img, (0,0))
    return new_img

def main():

    # init screen
    pg.init(),
    screen = pg.display.set_mode((field_w ,field_h + gm_bar_h))
    screen.fill(bg_clr)

    # init state variables
    key_pressed = False
    new_game = False
    paused = False
    ps_clicked = False
    mouse_x, mouse_y = pg.mouse.get_pos()

    # init maze
    dfs_maze = dfs.Maze(maze_row, maze_col)
    dfs_maze.buildMaze()
    drawMaze(dfs_maze, screen)

    # init player
    plr_x = margin_x + sp_x/2
    plr_y = margin_y + sp_y/2
    pg.draw.circle(screen, plr_clr, (plr_x, plr_y), plr_sz)

    # init texts
    time_txt = gb.Text(screen, "time:", 165, 900, txt_clr, 50, "LEFT")
    wins_txt  = gb.Text(screen, "wins:", 165, 960, txt_clr, 50, "LEFT")

    # # init buttons
    # ng_btn = gb.Button(screen, "new game", 400, 820, 150, 50)
    # ps_btn = gb.Button(screen, "pause", 165, 820, 150, 50)
    # cl_btn = gb.Button(screen, "clear rcd", 635, 820, 150, 50)

    # init icons
    folder_path = 'C:/Users/blake/Desktop/git/maze-game'
    icons = []
    easier_icon = gb.Icon(screen, folder_path+'/source/easier.png', 60, 800, 0.15)
    ps_cn_icon  = gb.Icon(screen, folder_path+'/source/pause.png', 180, 800, 0.15)
    nwg_icon    = gb.Icon(screen, folder_path+'/source/new_game.png', 290, 800, 0.15)
    music_icon  = gb.Icon(screen, folder_path+'/source/music.png', 400, 800, 0.15)
    clear_icon  = gb.Icon(screen, folder_path+'/source/clear.png', 535, 800, 0.15)
    harder_icon = gb.Icon(screen, folder_path+'/source/harder.png', 660, 800, 0.15)
    
    icons.append(clear_icon)
    icons.append(ps_cn_icon)
    icons.append(easier_icon)
    icons.append(harder_icon)
    icons.append(music_icon)
    icons.append(nwg_icon)


    game = True
    while(game):
        time.sleep(0.002)
        for event in pg.event.get():

            if(event.type == pg.QUIT):
                game = False
            
            if(event.type == pg.KEYUP):
                key_pressed = False

            if(event.type == pg.KEYDOWN and not paused):
                key_pressed = True
            
            # if(event.type == pg.MOUSEMOTION):
                # mouse_x, mouse_y = pg.mouse.get_pos()
                # ng_btn.updateState(mouse_x, mouse_y, "MOUSEUP")
                # ps_btn.updateState(mouse_x, mouse_y, "MOUSEUP")
                # cl_btn.updateState(mouse_x, mouse_y, "MOUSEUP")
            
            # if(event.type == pg.MOUSEBUTTONUP):
                # ng_btn.updateState(mouse_x, mouse_y, "MOUSEUP")
                # ps_btn.updateState(mouse_x, mouse_y, "MOUSEUP")
                # cl_btn.updateState(mouse_x, mouse_y, "MOUSEUP")
            
            # if(event.type == pg.MOUSEBUTTONDOWN):
                # ng_btn.updateState(mouse_x, mouse_y, "MOUSEDOWN")
                # ps_btn.updateState(mouse_x, mouse_y, "MOUSEDOWN")
                # cl_btn.updateState(mouse_x, mouse_y, "MOUSEDOWN")

                # if(ng_btn.state == "ACTIVE"):
                #     new_game = True
                # elif(ps_btn.state == "ACTIVE"):
                #     ps_clicked = True

        # if(ps_clicked):     # pause/continue button clicked
        #     ps_clicked = False
        #     if(paused):     # game paused -> game continue
        #         ps_btn.toggleTxt("pause")
        #         key_pressed = False
        #         paused = False
        #         new_game = False
        #     else:           # game ongoing -> pause game
        #         ps_btn.toggleTxt("continue")
        #         paused = True

        # if(new_game and not paused):       # start new game
        #     new_game = False
        #     key_pressed = False
        #     screen.fill(bg_clr)
        #     plr_x = margin_x + sp_x/2
        #     plr_y = margin_y + sp_y/2
        #     dfs_maze = dfs.Maze(maze_row, maze_col)
        #     dfs_maze.buildMaze()
        
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
                new_game = True
            
        # draw game elements
        screen.fill(bg_clr)

        if(paused):
            maskup(screen)
        else:
            pg.draw.circle(screen, plr_clr, (plr_x, plr_y), plr_sz)
            drawMaze(dfs_maze, screen)

        # ng_btn.draw()
        # ps_btn.draw()
        # cl_btn.draw()
        for i in icons:
            i.draw()
        time_txt.draw()
        wins_txt.draw()
        pg.display.update()

if __name__ == '__main__':
    main()