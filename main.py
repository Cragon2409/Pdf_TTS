import pygame, ctypes
from random import randrange

FPS = 60


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

myfont = pygame.font.SysFont("monospace", 20)
fancyFont = pygame.font.SysFont("monospace", 20)


black = (0,0,0)
lightgray = (150,150,150)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkgray = (50,50,50)
brown = (101,67,33)
darkorange = (255,100,0)
darkgreen = (0,100,0)
darkred = (139,0,0)
yellow = (255,255,0)
darkyellow = (204,204,0)


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



#===============================
# Classes 
#=============================== 

class Settings:
    def __init__(self):
        pass

class Document:
    def __init__(self, file_dest):
        self.file_dest = file_dest
        self.import_file(file_dest)

    def convert_file(self):
        pass
    def import_file(self, file_dest):
        pass

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
    def __init__(self):
        self.doc = Document(FILE_DEST) #FIXME have unopened state and use menu to select file
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
        

FILE_DEST = ""
def main_loop():

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

main_loop()