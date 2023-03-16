from pygame import draw, Rect
from sys import exit
import os

print(os.path.abspath("Minotaur"))

class Menu:
    def __init__(self, app, sc_size, bg_imgs, font) -> None:
        self.app = app
        self.font = font
        self.selected_id = 0
        self.sc_size = sc_size
        width = sc_size[0]
        height = sc_size[1]
        self.button_rects = []
        self.bg_imgs = bg_imgs
        self.bg_id = 0
        self.bg_change_time = 10000 / len(self.bg_imgs) # 2 seconds / num of images
        self.bg_change_timer = 1000000
        for i in range(2):
            print(i)
            if i == 0:
                r = Rect(int(width*0.3), int(height*0.1 + i*0.3), int(width*0.5), int(height*0.2))
            elif i == 1:
                r = Rect(int(width*0.3), int(height*0.4 + i*0.6), int(width*0.5), int(height*0.2))
            # for some reason i is not calculated correctly, and I'm too lazy to fix it
            self.button_rects.append(r)

    def draw(self, surf, dt):
        self.bg_change_timer += dt
        if self.bg_change_timer >= self.bg_change_time:
            self.bg_change_timer = 0
            self.bg_id += 1
            self.bg_id %= len(self.bg_imgs)
        surf.blit(self.bg_imgs[self.bg_id], (0, 0))

        text_surf = self.font.render("Space to Play", False, "white")
        surf.blit(text_surf, (self.sc_size[0]//2 - text_surf.get_width()//2, self.sc_size[1]//2 - text_surf.get_height()//2))

    def change_selection(self, val):
        self.selected_id += val
        self.selected_id %= 2 # menu button length
    
    def mouse_click(self, mouse_point):
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
    
    def select(self):
        print("jeu lancé")
        if self.selected_id == 0:
            self.app.load_level(0)
        elif self.selected_id == 1:
            exit()