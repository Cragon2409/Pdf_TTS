import pygame, ctypes
from random import randrange
import os

FPS = 60
SAVES_FOLDER = "saves/"
MANIFEST_FILE_DEST = "manifest.txt"
IMAGES_FOLDER_DEST = "images"
TEXT_FILE_DEST = "converted_text.txt"



pygame.init()
##screen =  pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

ctypes.windll.user32.SetProcessDPIAware()
# true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
tDW, tDH = 600,600
screen = pygame.display.set_mode((tDW, tDH))

pygame.display.set_caption("TTS Viewer")
clock = pygame.time.Clock()
dw, dh = pygame.display.get_surface().get_size()

pygame.font.init()
my_font = pygame.font.SysFont("monospace", 50)
my_font_smaller = pygame.font.SysFont("monospace", 40)
big_font = pygame.font.SysFont("calibri", 50)
big_font_bold = pygame.font.SysFont("calibri", 50, bold=True)
fancy_font_bigger = pygame.font.SysFont("calibri", 30)
fancy_font_underline = pygame.font.SysFont("calibri", 50); fancy_font_underline.set_underline(True)
fancy_font_bigger_bold = pygame.font.SysFont("calibri", 30,bold=True)
fancy_font = pygame.font.SysFont("calibri", 22)
fancy_font_bold = pygame.font.SysFont("calibri", 22, bold=True)
fancy_font_smaller = pygame.font.SysFont("calibri", 20)
title_font = pygame.font.SysFont("elephant",70,bold=True)
impact_font_big = pygame.font.SysFont("impact",70)
gab_font_big = pygame.font.SysFont("gabriola",100, bold=False)
arial_bigger = pygame.font.SysFont("arial",30)

black = (0,0,0); lightgray = (150,150,150); darklightgray = (100,100,100); white = (255,255,255); red = (255,0,0); green = (0,255,0); blue = (0,0,255); darkgray = (50,50,50); brown = (101,67,33); darkorange = (255,100,0); darkgreen = (0,100,0); darkred = (139,0,0); yellow = (255,255,0); whiteskin = (255,195, 170); yellow = (255,255,0); darkyellow = (204,204,0); purple = (128,0,128); lightblue = (50,50,255)
teal = (40,170,130); dark_teal = tuple([i*0.2 for i in teal])
dark_purple = (49,21,74)
magenta = (170,50,170)
navy_blue = (2,7,93)
baby_blue = (137,207,240)
pastel_pink = (255,197,211)
peach_red = (255,177,173)
title_blue = (20, 51, 117)

PAUSE_BUTTON_FONT = fancy_font_smaller
SMALL_BUTTON_SHADOW_OFFSET = (3,3)
SMALL_BUTTON_SHADOW_COL = dark_purple
BUTTON_OUTLINE_COLOUR = (50,50,50)

PLAY_BUTTON_FONT = big_font

MENU_BUTTON_FONT = fancy_font_bigger_bold
MENU_SHADOW_OFFSET = (5,5)
MENU_SHADOW_COL = dark_purple

BUTTON_HOVER_COL = peach_red
BUTTON_BACKGROUND_COL = white

GAME_BORDER_COL = (50,50,50)

MAIN_BACKGROUND_COL = teal

TEXT_BOX_OFFSET = (5,5)
LEVEL_LIST_GAP = 2
LEVEL_LIST_FONT = fancy_font_bigger
LEVEL_LIST_TEXT_OFFSET = (5,5)

def sync_graphics():
    global QUIT_BUTTON_RECT, PAUSE_BUTTON_RECT, PLAY_BUTTON_RECT, LEVEL_BUTTON_RECT, SHOP_BUTTON_RECT, CREDIT_BUTTON_RECT, HELP_BUTTON_RECT, MENU_TEXT_POS, HINT_BUTTON_RECT, BIG_TEXT_RECT, LEVEL_LIST_RECT, LEVEL_LIST_ITEM_RECT, LEVEL_LIST_BUTTON_RECT, LEVEL_CREATE_RECT, IMAGE_PREVIEW_SIZE,LEVEL_PREVIEW_RECT,LEVEL_PREVIEW_RSET_RECT, LEVEL_PREVIEW_PLAY_RECT, LEVEL_PREVIEW_TEXT_RECT
    QUIT_BUTTON_RECT        = [dw-35,5,30,30]
    PAUSE_BUTTON_RECT       = [dw-70,5,30,30]
    HINT_BUTTON_RECT        = [dw-105,5,30,30]
    PLAY_BUTTON_RECT        = [dw//2-200,150+30,400,70]
    LEVEL_BUTTON_RECT       = [dw//2-200,230+30,190,50]
    SHOP_BUTTON_RECT        = [dw//2+10,230+30,190,50]
    CREDIT_BUTTON_RECT      = [dw//2-200,290+30,190,50]
    HELP_BUTTON_RECT        = [dw//2+10,290+30,190,50]
    BIG_TEXT_RECT           = [dw//6, dh//6, 4*dw//6, 4*dh//6]

    LEVEL_LIST_RECT         = [3*dw//12, dh//6, 4*dw//6, 4*dh//6]
    LEVEL_LIST_ITEM_RECT    = [5,5, LEVEL_LIST_RECT[2] - 10, 40]
    LEVEL_LIST_BUTTON_RECT  = [10,LEVEL_LIST_RECT[1], (3*dw//12)-15, 40]
    LEVEL_CREATE_RECT       = [LEVEL_LIST_RECT[0], LEVEL_LIST_RECT[1]+LEVEL_LIST_RECT[3]+5, LEVEL_LIST_RECT[2], 40]

    LEVEL_PREVIEW_RECT      = [dw//6, dh//6, 4*dw//6, 4*dh//6]
    LEVEL_PREVIEW_TEXT_RECT = [LEVEL_PREVIEW_RECT[0]+5, LEVEL_PREVIEW_RECT[1]+5, LEVEL_PREVIEW_RECT[2]//2-10, 40]
    LEVEL_PREVIEW_PLAY_RECT = [LEVEL_PREVIEW_RECT[0]+5, LEVEL_PREVIEW_RECT[1]+LEVEL_PREVIEW_RECT[3]//2+5, LEVEL_PREVIEW_RECT[2]-10, 40]
    LEVEL_PREVIEW_RSET_RECT = [LEVEL_PREVIEW_RECT[0]+5, LEVEL_PREVIEW_RECT[1]+LEVEL_PREVIEW_RECT[3]//2+5+45, LEVEL_PREVIEW_RECT[2]-10, 40]
    
    MENU_TEXT_POS           = [dw//2,100]
    IMAGE_PREVIEW_SIZE = (200,200)



#stolen code (from stackoverflow)
strcpy = ctypes.cdll.msvcrt.strcpy
ocb = ctypes.windll.user32.OpenClipboard    # Basic clipboard functions
ecb = ctypes.windll.user32.EmptyClipboard
gcd = ctypes.windll.user32.GetClipboardData
scd = ctypes.windll.user32.SetClipboardData
ccb = ctypes.windll.user32.CloseClipboard
ga = ctypes.windll.kernel32.GlobalAlloc    # Global memory allocation
gl = ctypes.windll.kernel32.GlobalLock     # Global memory Locking
gul = ctypes.windll.kernel32.GlobalUnlock
GMEM_DDESHARE = 0x2000

def retrieveClipboard(mode=1):
    ocb(None) # Open Clip, Default task
    pcontents = gcd(1) # 1 means CF_TEXT.. too lazy to get the token thingy...
    data = ctypes.c_char_p(pcontents).value
    ccb()
    if mode == 0: return data
    elif mode == 1: return str(data)[2:]

def insertToClipboard(data):
    data = str(data)
    ocb(None) # Open Clip, Default task
    ecb()
    hCd = ga(GMEM_DDESHARE, len(bytes(data,"ascii")) + 1)
    pchData = gl(hCd)
    strcpy(ctypes.c_char_p(pchData), bytes(data, "ascii"))
    gul(hCd)
    scd(1, hCd)
    ccb()




#===============================
# General 
#=============================== 

PDU = pygame.display.update

def text_objects(text,font,colour=white):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())
def simple_text(input_text,co=(0,0),colour=white, font = fancy_font):
    text = font.render(input_text, True, colour)
    screen.blit(text,co)
def simple_text_lines(input_text_lines, co=(0,0), colour=white, font= fancy_font):
    line_height = font.size('A')[1]
    for n,line in enumerate(input_text_lines):
        simple_text(line, dA(co,(0,n*line_height)),colour,font)
def cent_text(input_text,center,colour=white,font=my_font):#draws text to the screen anchored on the centre of the given position
    textSurf, textRect = text_objects(input_text,font,colour)#generates the text surface and rectangle
    textRect.center = center#centres the text
    screen.blit(textSurf,textRect)#blits the text to the screen
def in_rect(co,rect): return co[0] >= rect[0] and co[1] >= rect[1] and co[0] < rect[0]+rect[2] and co[1] < rect[1]+rect[3]
def rect_cent(rect): return dA(rect[:2],dSM(0.5,rect[2:]))

def dA(d1,d2): return (d1[0]+d2[0], d1[1]+d2[1])
def dS(d1,d2): return (d1[0]-d2[0], d1[1]-d2[1])
def dSM(s,d1): return (s*d1[0],s*d1[1])


def quit_all_func(): pygame.quit(); quit()
quit_none_func = ( lambda : None)
def run_menu(buttons, quit_func=quit_none_func, background_col=(0,0,0), menu_fps=30):
    ticks = 0
    down_press_button = None
    menu_exit = [False]
    while not menu_exit[0]:
        # keys_pressed = pygame.key.get_pressed()
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: 
                quit_func()
                menu_exit[0] = True
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(background_col)
        for b in buttons: b.draw(m_co)
        
        PDU()

        clock.tick(menu_fps)
        ticks += 1




def read_manifest(save_name):
    manifest_dest = SAVES_FOLDER + save_name + '/manifest.txt'
    with open(manifest_dest,'r') as f:
        lines = f.read().splitlines()
    manifest_dict = dict()
    for line in lines:
        key = line.split(':')[0]
        value = ':'.join(line.split(':')[1:])
        manifest_dict[key] = value
    return manifest_dict


#===============================
# Classes 
#=============================== 

class Settings:
    def __init__(self):
        pass

class Document:
    def __init__(self, save_name):
        self.save_name = save_name
        self.manifest = read_manifest(save_name)
        if self.manifest["converted"] == "false":
            self.convert_file()
        self.import_file()
        self.sync_structure()

    def convert_file(self):
        pass

    def import_file(self):
        with open(SAVES_FOLDER + self.save_name +'/' + TEXT_FILE_DEST,'r') as f:
            txt = f.read()
        self.raw_txt = txt
    def sync_structure(self):
        self.pages = []
        page_num = 0
        current_page = Page(self, page_num)
        for line in self.raw_txt.splitlines():
            if "<<NewPage>>" in line:
                self.pages.append(current_page)
                page_num += 1
                current_page = Page(self, page_num)
            elif "<<Image" in line:
                #add Image
                file_name = line[line.index("<<Image:") + 8 : line.index(">>") + 1]
                current_page.add_element(PageImage(current_page, file_name),"images")
            elif "<<Title" in line:
                current_page.add_element(TextTitle(current_page, line.replace('<<Title:','').replace('>>','')),"title")
            elif line == '':
                continue
            else: #text
                current_page.add_element(TextLine(current_page, line,"text"))



class Page:
    def __init__(self, p_doc, number):
        self.p_doc = p_doc
        self.lines = []
        self.number = number
    def is_empty(self):
        return (self.lines == [])
    def add_element(self,element,e_type): #e_type can be "text", "image"
        if e_type == "text" or "title":
            self.lines.append(element)
        elif e_type == "image":
            self.lines.append(element)
    def pre_render(self):
        pass
    def draw(self):
        pass

class TextLine:
    def __init__(self,p_page, raw_txt):
        self.p_page, self.raw_txt = p_page, raw_txt

class TextTitle:
    def __init__(self, p_page, raw_txt):
        self.p_page, self.raw_txt = p_page, raw_txt

class PageImage:
    def __init__(self, p_page, image_name):
        self.p_page,self.image_name = p_page, image_name




class Viewer:
    def __init__(self):
        pass
    def show(self):
        pass
    def update(self):
        pass
    def on_click(self,button,m_co):
        return False
    def on_key(self,key):
        return False
    

class AudioPlayer:
    def __init__(self):
        pass
    def play(self):
        pass
    def pause(self):
        pass
    def seek(self,time):
        pass
    def update(self):
        pass
    def show_gui(self):
        pass
    def on_click(self,button,m_co):
        return False
    def on_key(self,key):
        return False

class Menu:
    def __init__(self):
        pass
    def show(self):
        pass
    def update(self):
        pass
    def on_click(self,button,m_co):
        return False
    def on_key(self,key):
        return False
    
# Event Priority Order: Menu > Audio Player > Document

class AppInstance:
    def __init__(self, save_name):
        self.save_name = save_name
        self.doc = Document(save_name) #FIXME have unopened state and use menu to select file
        self.viewer = Viewer()
        self.audio = AudioPlayer()
        self.menu = Menu()
        self.settings = Settings

        self.event_priority_order = [self.menu, self.audio, self.document]
    def show(self):
        self.viewer.show()
        self.menu.show()
        self.audio.show_gui()
    def on_click(self,button,m_co):
        for child in self.event_priority_order:
            if self.on_click(button, m_co):
                return True
        return False
    def on_key(self,key):
        for child in self.event_priority_order:
            if self.on_key(key):
                return True
        return False
    def update(self, ticks):
        self.audio.update()
        self.viewer.update()
        self.menu.update()
        self.document.update()
        


def view_save(save_name):

    inst = AppInstance()    
    ticks = 0
    while 1:
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if inst.on_click(ev.button, m_co):
                    pass
                else:
                    pass
            elif ev.type == pygame.KEYDOWN:
                if inst.on_key(ev.key):
                    pass
                else:
                    pass
        
        inst.update(ticks)

        screen.fill(black)
        inst.show()
        PDU()

        clock.tick(FPS)
        ticks += 1



# Menu Items
class MenuItem:
    def __init__(self,rect,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL,background_col=BUTTON_BACKGROUND_COL):
        self.rect, self.rounding, self.shadow, self.shadow_col, self.background_col = rect, rounding, shadow, shadow_col, background_col
        if self.shadow != (0,0): self.shadow_rect = list(dA(self.rect[:2],self.shadow)) + list(self.rect[2:])
        self.syncCent()
    def inButton(self,m_co):
        return in_rect(m_co, self.rect)
    def syncCent(self):
        self.cent = rect_cent(self.rect)
    def onPressDown(self,m_co=None):
        self.pressed = True
    def onPressUp(self,m_co=None):
        self.pressed = False
    def onPressRelease(self):
        self.pressed = False
    def onScroll(self,s_di):
        pass
    def draw(self, m_co=None):
        if self.shadow != (0,0):
            pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
        pygame.draw.rect(screen,self.background_col,self.rect, border_radius = self.rounding)
        pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)

class MenuButton(MenuItem):
    def __init__(self,rect,text,func,font=fancy_font,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL):
        super().__init__(rect, rounding, shadow, shadow_col)
        self.text, self.func, self.font = text, func, font
        self.pressed = False
    def onPressUp(self,m_co=None):
        self.pressed = False
        if self.func != None: self.func()
        return True
    def draw(self, m_co):
        selCol = BUTTON_HOVER_COL if in_rect(m_co,self.rect) else BUTTON_BACKGROUND_COL
        if self.pressed:
            pygame.draw.rect(screen,selCol,self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.shadow_rect, 2, border_radius = self.rounding)
            cent_text(self.text,dA(self.cent,self.shadow), black,font=self.font)
        else:
            if self.shadow != (0,0):
                pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,selCol,self.rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)
            cent_text(self.text,self.cent, black,font=self.font)

class SelectionButton(MenuItem):
    def __init__(self,rect,text,func,font=fancy_font,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL):
        super().__init__(rect, rounding, shadow, shadow_col)
        self.text, self.func, self.font = text, func, font
        self.pressed = False
        #self.other_buttons needs to be set externally
    def set_other_buttons(self,other_buttons):
        self.other_buttons = other_buttons
    def onPressUp(self,m_co=None):
        pass
    def onPressRelease(self):
        pass
    def onPressDown(self,m_co=None):
        self.pressed = True
        for b in self.other_buttons: b.pressed = False
        if self.func != None: self.func(self)
    def draw(self, m_co):
        selCol = BUTTON_HOVER_COL if in_rect(m_co,self.rect) else BUTTON_BACKGROUND_COL
        if self.pressed:
            pygame.draw.rect(screen,selCol,self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.shadow_rect, 2, border_radius = self.rounding)
            cent_text(self.text,dA(self.cent,self.shadow), black,font=self.font)
        else:
            if self.shadow != (0,0):
                pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,selCol,self.rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)
            cent_text(self.text,self.cent, black,font=self.font)


class TextBox(MenuItem):
    def __init__(self,rect,text,font=fancy_font,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL):
        super().__init__(rect, rounding, shadow, shadow_col)
        self.text, self.font = text, font
        self.text_pos = dA(self.rect[:2],TEXT_BOX_OFFSET)
        self.text_lines = text.splitlines()
    def draw(self, m_co=None):
        if self.shadow != (0,0):
            pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
        pygame.draw.rect(screen,BUTTON_BACKGROUND_COL,self.rect, border_radius = self.rounding)
        pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)
        simple_text_lines(self.text_lines, self.text_pos,black)

class SavesList(MenuItem):
    def __init__(self, save_names):
        super().__init__(LEVEL_LIST_RECT,background_col=dark_teal)
        self.switch_list(save_names)
    def switch_list(self,save_names):
        self.items = save_names
    def draw(self,m_co):
        super().draw()
        for c,item in enumerate(self.items):
            pos = dA(dA(self.rect[:2], LEVEL_LIST_ITEM_RECT), dSM(c, (0, LEVEL_LIST_GAP+LEVEL_LIST_ITEM_RECT[3])))
            rect = list(pos) + LEVEL_LIST_ITEM_RECT[2:]
            sel_col = BUTTON_HOVER_COL if in_rect(m_co, rect) else BUTTON_BACKGROUND_COL
            pygame.draw.rect(screen, sel_col, rect)
            pygame.draw.rect(screen, black, rect, 2)
            simple_text(item[0], dA(pos,LEVEL_LIST_TEXT_OFFSET), black, font=LEVEL_LIST_FONT)
    def onPressDown(self,m_co):
        for c,item in enumerate(self.items):
            pos = dA(dA(self.rect[:2], LEVEL_LIST_ITEM_RECT), dSM(c, (0, LEVEL_LIST_GAP+LEVEL_LIST_ITEM_RECT[3])))
            rect = list(pos) + LEVEL_LIST_ITEM_RECT[2:]
            if in_rect(m_co, rect):
                raise NotImplemented
        
CONVERT_BUTTON_RECT = [100,300,500,150]
OPEN_SAVE_RECT = [100,100,500,150]

def convert_new_file():
    pass

def saves_menu():
    save_names = os.listdir(SAVES_FOLDER)


    pass

def main_menu():
    menu_buttons = [
        MenuButton(CONVERT_BUTTON_RECT, "Convert New File", convert_new_file, shadow=(3,3), rounding=2),
        MenuButton(OPEN_SAVE_RECT, "Saved Files", saves_menu, shadow=(3,3), rounding=2)
    ]
    run_menu(menu_buttons,quit_all_func, menu_fps=30)


# SAVE = 'D4RL'
# view_save(SAVE)

main_menu()

