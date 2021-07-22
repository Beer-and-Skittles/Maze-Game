import pygame as pg

btn_dft_clr = (235, 187, 255)   # lavendar
btn_hvr_clr = (239, 105, 102)   # light vermillion
btn_act_clr = (255, 167, 105)   # pastel orange
btn_txt_clr = (  0,  52, 110)   # china blue

hnt_txt_clr = (  0,  36,  81)  # black blue
hnt_box_clr = (153, 255, 255)  # azure

icn_nul_clr = (255, 255, 255)   # white
icn_dft_clr = (235, 187, 255)   # lavendar
icn_hvr_clr = (255, 238, 164)   # pastel yellow
icn_act_clr = (255, 197, 143)   # pastel orange

bg_clr   = (0, 36, 81)      # muted indigo

class Icon():
    
    def __init__(self, screen, image_path, x_pos, y_pos, factor):
        self.state = "DEFAULT"  # DEFAULT, HOVER, ACTIVE
        self.scrn = screen
        self.fct = factor
        self.x = x_pos
        self.y = y_pos
        self.w, self.h, self.clr, self.icon = None, None, None, None
        self.loadImg(image_path)
        self.scrn.blit(self.icon, (self.x, self.y))

    def loadImg(self, image_path):  # load image into icon
   
        icon = pg.image.load(image_path)
        scale = icon.get_size()
        self.w = int( scale[0] * self.fct )
        self.h = int( scale[1] * self.fct )
        icon = pg.transform.scale(icon, (self.w,self.h))
        icon = self.colorSwap(icon, (0,0,0), bg_clr)
        icon = self.colorSwap(icon, icn_nul_clr, icn_dft_clr)
        self.clr = icn_dft_clr
        self.icon = icon

    def updateState(self, mouse_x, mouse_y, state):

        if(mouse_x>=self.x and mouse_x<=self.x+self.w and mouse_y>=self.y and mouse_y<=self.y+self.h):
            if(state == "MOUSEUP"):
                self.state = "HOVER"
            elif(state == "MOUSEDOWN"):
                self.state = "ACTIVE"
        else:
            self.state = "DEFAULT"

    def colorSwap(self, img, old_clr, new_clr): # change one color in icon to another

        new_img = pg.Surface(img.get_size())
        new_img.fill(new_clr)
        img.set_colorkey(old_clr)
        new_img.blit(img, (0,0))
        return new_img    
    
    def draw(self): # draw icon

        color = None
        if(self.state == "ACTIVE"):
            color = icn_act_clr

        elif(self.state == "HOVER"):
            color = icn_hvr_clr

        elif(self.state == "DEFAULT"):
            color = icn_dft_clr

        self.icon = self.colorSwap(self.icon, self.clr, color)
        self.clr = color
        self.scrn.blit(self.icon, (self.x, self.y))
    
    

class Text():
    def __init__(self, screen, text, x_pos, y_pos, color, size, a):
        self.scrn = screen
        self.font = pg.font.SysFont('calibri', size)
        self.clr  = color 
        self.txt  = self.font.render(text, 1, color)
        self.x_ref = x_pos
        self.y_ref = y_pos

        self.a = a
        self.x, self.y = self.align()
        self.scrn.blit(self.txt, (self.x, self.y))
    
    def align(self):
        x, y = None, None
        if(self.a == "MID"):
            x = self.x_ref - self.txt.get_width()/2
 
        elif(self.a == "LEFT"):
            x = self.x_ref

        elif(self.a == "RIGHT"):
            x = self.x_ref - self.txt.get_width()
        y = self.y_ref 
        return x,y

    def toggleTxt(self, text):
        self.txt = self.font.render(text, 1, self.clr)
        self.x, self.y = self.align()
    
    def draw(self):
        self.scrn.blit(self.txt, (self.x, self.y))
    
    def len(self):
        return self.txt.get_width()

class Button():
    def __init__(self, screen, text, x_pos, y_pos, width, height):
        self.state = "DEFAULT"  # DEFAULT, HOVER, ACTIVE
        self.scrn = screen
        self.w = width
        self.h = height
        self.x = x_pos
        self.y = y_pos
        
        pg.draw.rect(self.scrn, btn_dft_clr, (self.x-self.w/2, self.y-self.h/2, self.w, self.h))
        pg.draw.circle(self.scrn, btn_dft_clr, (self.x-self.w/2, self.y), self.h/2)
        pg.draw.circle(self.scrn, btn_dft_clr, (self.x+self.w/2, self.y), self.h/2)
        self.btn_txt = Text(self.scrn, text, self.x, self.y, btn_dft_clr, int(self.h*0.8), "MID")
    
    def dis(self, a_x, a_y, b_x, b_y):
        return pow( pow(a_x-b_x, 2) + pow(a_y-b_y, 2), 0.5)
    
    def toggleTxt(self, text):
        self.btn_txt.toggleTxt(text)
    
    def updateState(self, mouse_x, mouse_y, state):

        in_button = False
        if(mouse_x >= self.x-self.w/2 and mouse_x <= self.x+self.w/2\
        and mouse_y >= self.y-self.h/2 and mouse_y <= self.y+self.h/2):
            in_button = True

        elif(self.dis(mouse_x, mouse_y, self.x-self.w/2, self.y) < self.h/2\
        or self.dis(mouse_x, mouse_y, self.x+self.w/2, self.y) < self.h/2):
            in_button = True
        
        if(in_button):
            if(state == "MOUSEUP"):
                self.state = "HOVER"
            elif(state == "MOUSEDOWN"):
                self.state = "ACTIVE"
        else:
            self.state = "DEFAULT"
    
    def draw(self):

        color = ()
        if(self.state == "DEFAULT"):
            color = btn_dft_clr
        elif(self.state == "HOVER"):
            color = btn_hvr_clr
        elif(self.state == "ACTIVE"):
            color = btn_act_clr
        
        pg.draw.rect(self.scrn, color, (self.x-self.w/2, self.y-self.h/2, self.w, self.h))
        pg.draw.circle(self.scrn, color, (self.x-self.w/2, self.y), self.h/2)
        pg.draw.circle(self.scrn, color, (self.x+self.w/2, self.y), self.h/2)
        self.btn_txt.draw()

class HintBox():
    def __init__(self, screen, x_pos, y_pos, text, txt_size):
        self.scrn = screen
        self.x = x_pos
        self.y = y_pos
        self.hint = Text(self.scrn, text, self.x, self.y, hnt_txt_clr, 20 , "MID")
        self.w = self.hint.len() * 1.2
        self.h = txt_size * 1.2
    
    def show(self):
        pg.draw.rect(self.scrn, hnt_box_clr, (self.x, self.y, self.w, self.h))
        self.hint.draw()

