import maze_dfs as dfs
import game_bar as gb
import pygame as pg
import random as rnd
import time


field_h = 800
field_w = 800
gm_bar_h = 150
margin_x = 70
margin_y = 70 
dft_row = 10
dft_col = 10
rc_l_bnd = 5
rc_h_bnd = 30
wall_w   = 5
unit_len = 1
plr_sz   = 10

bg_clr   = (0, 36, 81)      # muted indigo
plr_clr  = (255, 0, 0)      # red
txt_clr  = (153, 255, 255)  # azure
maze_clr = [(235, 187, 255), (255, 197, 143), (255, 238, 164), (115, 201, 145)]
# lavender, pastel orange, pastel yellow, avocado

def drawMaze(dfs_maze, screen, maze_row, maze_col):     # draws maze

    sp_x = (field_w - 2*margin_x)/maze_col
    sp_y = (field_h - 2*margin_y)/maze_row

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

def inRein(dfs_maze, x, y, maze_row, maze_col):     # returns true if the player position is legal
    sp_x = (field_w - 2*margin_x)/maze_col
    sp_y = (field_h - 2*margin_y)/maze_row
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

def winGame(x, y, maze_row, maze_col):
    sp_x = (field_w - 2*margin_x)/maze_col  
    sp_y = (field_h - 2*margin_y)/maze_row
    row = int((y - margin_y)/sp_y)
    col = int((x - margin_x)/sp_x)
    if(row+1 == maze_row and col+1 == maze_col):
        return True
    return False

def maskup(screen, maze_row, maze_col):
    sp_x = (field_w - 2*margin_x)/maze_col
    sp_y = (field_h - 2*margin_y)/maze_row
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

    # set screen
    pg.init()
    screen = pg.display.set_mode((field_w ,field_h + gm_bar_h))
    screen.fill(bg_clr)

    # set music
    folder_path = 'C:/Users/blake/Desktop/git/maze-game'
    sound_on = True
    pg.mixer.init()
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.load(folder_path + '/source/bg.mp3')
    # pg.mixer.music.play(-1)

    # set sound effects
    click_sound = pg.mixer.Sound(folder_path + '/source/click.mp3')
    hover_sound = pg.mixer.Sound(folder_path + '/source/hover.mp3')
    victr_sound = pg.mixer.Sound(folder_path + '/source/victory.mp3')
    swish_sound = pg.mixer.Sound(folder_path + '/source/swish.wav')
    

    # init state variables
    key_pressed = False
    new_game = False
    paused = False
    ps_clicked = False
    time_ref = 0
    time_sh = 0
    wins = 0
    mouse_x, mouse_y = pg.mouse.get_pos()

    # init maze
    maze_row = dft_row
    maze_col = dft_col
    dfs_maze = dfs.Maze(maze_row, maze_col)
    dfs_maze.buildMaze()
    drawMaze(dfs_maze, screen, maze_row, maze_col)

    # init player
    sp_x = (field_w - 2*margin_x)/maze_col
    sp_y = (field_h - 2*margin_y)/maze_row
    plr_x = margin_x + sp_x/2
    plr_y = margin_y + sp_y/2
    pg.draw.circle(screen, plr_clr, (plr_x, plr_y), plr_sz)

    # init texts
    t_dsp_txt = gb.Text(screen, "TIME:", 65, 875, txt_clr, 50, "LEFT")
    w_dsp_txt = gb.Text(screen, "VICTORIES:", 445, 875, txt_clr, 50, "LEFT")
    t_rec_txt = gb.Text(screen, "", 370, 875, txt_clr, 50, "RIGHT")
    w_rec_txt = gb.Text(screen, str(wins), 735, 875, txt_clr, 50, "RIGHT")

    # init hintbox
    hb_y = 828
    esr_hb = gb.HintBox(screen,  90, hb_y, "easier maze", 100)
    p_c_hb = gb.HintBox(screen, 220, hb_y, "pause/continue", 160)
    nwg_hb = gb.HintBox(screen, 340, hb_y, "new game", 90)
    msc_hb = gb.HintBox(screen, 460, hb_y, "music on/off", 160)
    clr_hb = gb.HintBox(screen, 580, hb_y, "discard records", 180)
    hdr_hb = gb.HintBox(screen, 700, hb_y, "harder maze", 105)

    # init icons
    name_dict = {"ESR":0, "P_C":1, "NWG":2, "MSC":3, "CLR":4, "HDR":5}
    p_img_path  = folder_path + '/source/pause.png'
    c_img_path  = folder_path + '/source/continue.png'
    icn_y = hb_y - 75
    easier_icon = gb.Icon(screen, folder_path+'/source/easier.png', 58, icn_y, 0.12, esr_hb)
    ps_cn_icon  = gb.Icon(screen, folder_path+'/source/pause.png', 185, icn_y, 0.12, p_c_hb)
    nwg_icon    = gb.Icon(screen, folder_path+'/source/new_game.png', 310, icn_y, 0.12, nwg_hb)
    music_icon  = gb.Icon(screen, folder_path+'/source/music.png', 430, icn_y, 0.12, msc_hb)
    clear_icon  = gb.Icon(screen, folder_path+'/source/clear.png', 550, icn_y, 0.12, clr_hb)
    harder_icon = gb.Icon(screen, folder_path+'/source/harder.png', 670, icn_y, 0.12, hdr_hb)
    all_icons = [easier_icon, ps_cn_icon, nwg_icon, music_icon, clear_icon, harder_icon]

    time_ref = time.time()
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
                pg.mixer.Sound.play(swish_sound)
            
            if(event.type == pg.MOUSEMOTION):
                mouse_x, mouse_y = pg.mouse.get_pos()
                for icns in all_icons:
                    if(icns.updateState(mouse_x, mouse_y, "MOUSEUP")):
                        pass
                        pg.mixer.Sound.play(hover_sound)
            
            if(event.type == pg.MOUSEBUTTONUP):
                for icns in all_icons:
                    icns.updateState(mouse_x, mouse_y, "MOUSEUP")
            
            if(event.type == pg.MOUSEBUTTONDOWN):
                for icns in all_icons:
                    icns.updateState(mouse_x, mouse_y, "MOUSEDOWN")
                    if(icns.state == "ACTIVE"):
                        pg.mixer.Sound.play(click_sound)

                # operations for clicked icons
                if(all_icons[name_dict["NWG"]].state == "ACTIVE"):
                    new_game = True
                
                elif(all_icons[name_dict["CLR"]].state == "ACTIVE"):
                    new_game = True
                    maze_row = dft_row
                    maze_col = dft_col
                    wins = 0
                    w_rec_txt.toggleTxt(str(wins)) 
                
                elif(all_icons[name_dict["MSC"]].state == "ACTIVE"):
                    if(sound_on):
                        pg.mixer.music.set_volume(0)
                    else:
                        pg.mixer.music.set_volume(0.5)

                    sound_on = not sound_on

                elif(all_icons[name_dict["P_C"]].state == "ACTIVE"):
                    ps_clicked = True

                elif(all_icons[name_dict["ESR"]].state == "ACTIVE"):
                    if(maze_row > rc_l_bnd):
                        new_game = True
                        maze_row -= 1
                        maze_col -= 1

                elif(all_icons[name_dict["HDR"]].state == "ACTIVE"):
                    if(maze_row < rc_h_bnd):
                        new_game = True
                        maze_row += 1
                        maze_col += 1
          
        if(ps_clicked):     # pause/continue icon clicked
            ps_clicked = False
            if(paused):     # game paused -> game continue
                print("pause image on")
                all_icons[name_dict["P_C"]].loadImg(p_img_path)
                key_pressed = False
                paused = False
                new_game = False
                time_ref = time.time()
            else:           # game ongoing -> pause game
                print("continue image on")
                all_icons[name_dict["P_C"]].loadImg(c_img_path)
                paused = True
                time_sh = time_sh + time.time() - time_ref

        if(new_game and not paused):       # start new game
            new_game = False
            key_pressed = False
            screen.fill(bg_clr)
            sp_x = (field_w - 2*margin_x)/maze_col
            sp_y = (field_h - 2*margin_y)/maze_row
            plr_x = margin_x + sp_x/2
            plr_y = margin_y + sp_y/2
            dfs_maze = dfs.Maze(maze_row, maze_col)
            dfs_maze.buildMaze()
            time_ref = time.time()
            time_sh = 0
        
        if(key_pressed):    # a key is pressed
            if(event.key == pg.K_UP):
                if(inRein(dfs_maze, plr_x, plr_y-unit_len, maze_row, maze_col)):
                    plr_y -= unit_len

            elif(event.key == pg.K_DOWN):
                if(inRein(dfs_maze, plr_x, plr_y+unit_len, maze_row, maze_col)):
                    plr_y += unit_len

            elif(event.key == pg.K_RIGHT):
                if(inRein(dfs_maze, plr_x+unit_len, plr_y, maze_row, maze_col)):
                    plr_x += unit_len

            elif(event.key == pg.K_LEFT):
                if(inRein(dfs_maze, plr_x-unit_len, plr_y, maze_row, maze_col)):
                    plr_x -= unit_len
            
            if(winGame(plr_x, plr_y, maze_row, maze_col)):  # current game is won
                pg.mixer.Sound.play(victr_sound)
                new_game = True
                wins += 1
                w_rec_txt.toggleTxt(str(wins))
            
        # draw game elements
        screen.fill(bg_clr)

        if(paused):
            maskup(screen, maze_row, maze_col)
            t_rec_txt.toggleTxt(str(round(time_sh, 2)))

        else:
            pg.draw.circle(screen, plr_clr, (plr_x, plr_y), plr_sz)
            drawMaze(dfs_maze, screen, maze_row, maze_col)
            t_rec_txt.toggleTxt(str(round(time_sh + time.time() - time_ref, 2)))

        for i in all_icons:
            i.draw()

        t_dsp_txt.draw()
        w_dsp_txt.draw()
        t_rec_txt.draw()
        w_rec_txt.draw()
        pg.display.update()

if __name__ == '__main__':
    main()