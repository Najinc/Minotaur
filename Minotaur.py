import pygame as pg
pg.mixer.init()
import sys
import MazeCustom as maze
import random
from menu import Menu
import os
from random import randint

pg.font.init()

def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class App:
    def __init__(self):
        self.chemin=os.path.dirname(__file__)
        self.size = 5
        self.tilesize = 32
        self.SCREEN_SIZE = ((self.size*2+1)*self.tilesize, (self.size*2+1)*self.tilesize) #(600, 600)  
        self.screen = pg.display.set_mode(self.SCREEN_SIZE, pg.RESIZABLE | pg.SCALED | pg.FULLSCREEN)
        self.playerimg = pg.image.load(resource_path("assets/minotaur.png")).convert_alpha() #self.chemin+"\\assets\\minotaur.png"
        self.clock = pg.time.Clock()
        self.wallhit_sounds = ["algogole.mp3"]
        self.lifeUp_sounds = ["ameno.mp3", "powerup.mp3"]
        self.back_sounds = ["retourne-cuisine.mp3", "cheh.mp3","sad.mp3", "concentretoi.mp3"]
        self.reverse_sounds = ["cri.mp3", "ratiosandron.mp3"]
        self.menu_music = pg.mixer.Sound(resource_path("Minotaur/sounds/external-8bits.mp3")) #"self.chemin+"\\sounds\\external-8bits.mp3"
        self.final_sound = pg.mixer.Sound(resource_path("Minotaur/sounds/psycho.mp3")) #self.chemin+"\\sounds\\psycho.mp3"
        self.score = 0
        self.font = pg.font.Font(resource_path("Minotaur/assets/ARCADE.ttf"), 50) #self.chemin+"\\assets\\ARCADE.ttf"
        self.player_x = 1
        self.player_y = 1
        self.end_x = None
        self.end_y = None
        self.level = None #0
        self.levels = []
        self.state = "start"
        self.reverseCmds = 0
        self.health = 3
        self.level_amount = 7
        self.create_levels(self.level_amount)
        self.bg_images = []
        self.mpos = [0, 0]
        self.levelfinishsed = False
        self.dt = 0
        self.generate_images(resource_path("Minotaur/images")) # self.chemin+"\\images"
        self.move_timer = 0 # milliseconds
        self.item1_img = pg.image.load(resource_path("Minotaur/assets/reverseCmds.png")).convert_alpha() # self.chemin+"\\assets/reverseCmds.png"
        self.item2_img = pg.image.load(resource_path("Minotaur/assets/health.png")).convert_alpha() # self.chemin+"\\assets/health.png"
        self.menu = Menu(self, self.SCREEN_SIZE, self.bg_images, self.font)
        self.campos = (0, 0)
        self.zoomfactor = 2

    def generate_images(self, foldername: str): # folder containing the images
        for g in os.listdir(foldername):
            img = pg.image.load(foldername+"\\"+g).convert()
            img = pg.transform.smoothscale(img, self.SCREEN_SIZE)
            self.bg_images.append(img)

    def create_levels(self, amount):
        for i in range(amount):
            level, rawdata = maze.generate_map((i+1)*self.size, (i+1)*self.size)
            self.levels.append(level)
            self.rawdata = rawdata

    def update(self):
        keys = pg.key.get_pressed()
        self.move_timer += self.dt
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    sys.exit()
                if self.state == "game":
                    for val in range(self.level_amount): # Instead of writing if pyxel.btnp 9 times I use this
                        if event.key == eval("pg.K_" + str(val)):
                            self.load_level(val)
                if self.state == "start":
                    if event.key == pg.K_w:
                        self.menu.change_selection(1)
                    if event.key == pg.K_s:
                        self.menu.change_selection(-1)
                    if event.key == pg.K_SPACE:
                        print("ENTER")
                        self.menu.select()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.state == "start":
                    self.menu.mouse_click()

        if self.state == "game":
            pg.mixer.music.stop()
            if self.player_x == 1 and self.player_y == 1:
                self.health = 3

            if self.health == 0: # Si la vie est à 0, on revient au début
                self.player_x = 1 ## On remet le joueur au début
                self.player_y = 1
                pg.mixer.stop()
                pg.mixer.Sound(resource_path(f"Minotaur/sounds/{self.back_sounds[randint(0, len(self.back_sounds)-1)]}")).play()

            if self.reverseCmds>0: # Si le joueur a mangé un item, il peut inverser les commandes
                if keys[pg.K_UP]:
                    self.move_player(0, 1)
                if keys[pg.K_LEFT]:
                    self.move_player(1, 0)
                if keys[pg.K_DOWN]:
                    self.move_player(0, -1)
                if keys[pg.K_RIGHT]:
                    self.move_player(-1, 0)
            else : # Sinon, les commandes sont normales
                if keys[pg.K_LEFT]:
                    self.move_player(-1, 0)
                if keys[pg.K_DOWN]:
                    self.move_player(0, 1)
                if keys[pg.K_RIGHT]:
                    self.move_player(1, 0)
                if keys[pg.K_UP]:
                    self.move_player(0, -1)

        elif self.state == "start":
            self.menu_music.play()

    def load_level(self, level):
        print("new level", level)
        if level == len(self.levels):
            print("THE LAST LEVEL")
            self.state="fin"
            pg.draw.rect(self.screen, "black", (0, 0, self.screen.get_width(), self.screen.get_height()))
            pg.mixer.stop()
            self.final_sound.play()
            return
        self.level = level
        self.score = 0
        self.health = 3
        self.levelfinished = False
        self.player_x = 1
        self.player_y = 1
        self.state = "game"
        current_level = self.levels[self.level]
        self.end_x = len(current_level[0])-2
        self.end_y = len(current_level)-2
        current_level[self.end_y][self.end_x] = 2 # Arrivée
        self.spawn_items(3, (level+1)*5) # Important: 3 c'est l'ID de l'item, 5 c'est le montant
        self.spawn_items(4, (level+1)*3)
        self.draw_maze(current_level)

    def move_player(self, x, y):
        current_level = self.levels[self.level]
        if self.move_timer >= 200: # milliseconds
            self.move_timer = 0
            current_level = self.levels[self.level]
            newy = self.player_y + y
            newx = self.player_x + x
            iswall = current_level[newy][newx]
            self.reverseCmds-=1
            if iswall == 1:
                print("WALL, can't move")
                self.health -= 1
                pg.mixer.stop()
                pg.mixer.Sound(resource_path(f"Minotaur/sounds/{self.wallhit_sounds[randint(0, len(self.wallhit_sounds)-1)]}")).play()
            elif iswall == 0:
                print("MOVEMENT")
                self.player_x = newx
                self.player_y = newy
            elif iswall == 2:
                print("NEW LEVEL")
                self.load_level(self.level + 1)
            elif iswall == 3: # REVERSE COMMANDS ITEM
                self.player_x = newx
                self.player_y = newy
                current_level[newy][newx] = 0
                self.reverseCmds=randint(3,15)
                pg.mixer.stop()
                pg.mixer.Sound(resource_path(f"Minotaur/sounds/{self.reverse_sounds[randint(0, len(self.reverse_sounds)-1)]}")).play()
            elif iswall == 4: # HEALTH ITEM
                self.health += 1
                self.player_x = newx
                self.player_y = newy
                current_level[newy][newx] = 0
                pg.mixer.stop()
                pg.mixer.Sound(resource_path(f"Minotaur/sounds/{self.lifeUp_sounds[randint(0, len(self.lifeUp_sounds)-1)]}")).play()
        self.draw_maze(current_level)
        camx = (self.zoomfactor + -self.player_x)*self.tilesize*self.zoomfactor
        camy = (self.zoomfactor + -self.player_y)*self.tilesize*self.zoomfactor
        self.campos = (camx, camy)

    def draw(self):
        self.screen.fill("black") # nettoyage de l'écran avec un index de couleur
        text_surf = self.font.render(f"HP:{self.health}", False, "white")        

        if self.state == "start":
            self.menu.draw(self.screen, self.dt)
        if self.state == "game":
            # self.draw_maze(self.levels[self.level])
            self.surf_to_draw = pg.transform.scale_by(self.maze_surf, self.zoomfactor)
            self.screen.blit(self.surf_to_draw, self.campos)
            self.screen.blit(text_surf, (0,0))
        if self.state=="fin":
            surf=pg. display. set_mode((0, 0), pg. FULLSCREEN)
            text_surf = self.font.render("Bravo, vous avez aide le Minotaur a sortir du labyrinthe", False, "Red")
            surf.blit(text_surf, (0,self.screen.get_height()//3))
            text_surf2 = self.font.render("Il va maintenant pouvoir tout detruire", False, "Red")
            surf.blit(text_surf2, (0,self.screen.get_height()//1.75))

    def run(self):
        while True:
            self.update()
            self.draw()
            self.dt = self.clock.tick(60)
            pg.display.update()

    def draw_maze(self, level):
        self.maze_surf = pg.surface.Surface((len(level[0])*self.tilesize, len(level)*self.tilesize))
        for y, line in enumerate(level):
            for x, tile in enumerate(line):
                if tile < 3 and tile >= 0:
                    if tile == 0:
                        color = (246,240,114)
                    if tile == 1:
                        color = (110,120,112)
                    if tile == 2: 
                        color = "white"
                    pg.draw.rect(self.maze_surf, color, (x*self.tilesize, y*self.tilesize, self.tilesize, self.tilesize))
                else:
                    if tile == 3:
                        self.adapt_item1_img = pg.transform.scale(self.item1_img, (self.item1_img.get_width(),
                                                                                   self.item1_img.get_height()))
                        pg.draw.rect(self.maze_surf, (246,240,114), (x*self.tilesize, y*self.tilesize, self.tilesize, self.tilesize))
                        self.maze_surf.blit(self.adapt_item1_img, (x*self.tilesize, y*self.tilesize))
                    elif tile == 4:
                        self.adapt_item2_img = pg.transform.scale(self.item2_img, (self.item2_img.get_width(),
                                                                                   self.item2_img.get_height()))
                        pg.draw.rect(self.maze_surf, (246,240,114), (x*self.tilesize, y*self.tilesize, self.tilesize, self.tilesize))
                        self.maze_surf.blit(self.adapt_item2_img, (x*self.tilesize, y*self.tilesize))
        self.adapt_playerimg = pg.transform.scale(self.playerimg, (self.playerimg.get_width(), self.playerimg.get_height()))
        self.maze_surf.blit(self.adapt_playerimg, (self.player_x*self.tilesize, self.player_y*self.tilesize))

    def spawn_items(self, itemid: int, amount: int):
        current_level = self.levels[self.level]
        while amount!=0:
            x = random.randint(2, len(current_level[0])-2)
            y = random.randint(2, len(current_level)-2)
            if current_level[y][x] == 0:
                current_level[y][x] = itemid
                amount -= 1
                
app = App()
app.run()