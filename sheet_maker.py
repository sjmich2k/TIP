
class SheetMaker:
    def __init__(self, pygame, sprite_width, sprite_height):
        self.pygame = pygame

        # Init background size to column size 15x and row size 5x
        self.s_width = sprite_width
        self.s_height = sprite_height
        self.num_col = 15
        self.num_row = 10
        self.background = None

        # Setup sprites
        self.sprites = []
        self.index_to_add = 0
        self.empty_sprite = self.pygame.image.load('tiles/W.png')
        self.green_sprite = self.pygame.image.load('tiles/G.png')

        # Setup debug display
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = self.pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill((0, 0, 0))

        self.render_sheet()

    def render_sheet(self, save=False):
        self.background = self.pygame.Surface((self.s_width * self.num_col, self.s_height * self.num_row))
        sprite_ind = 0
        for r in range(0, self.num_row):
            for c in range(0, self.num_col):
                x = self.s_width * c
                y = self.s_height * r

                # set background
                if sprite_ind < self.index_to_add:
                    self.background.blit(self.green_sprite, (x, y))
                if sprite_ind >= self.index_to_add:
                    self.background.blit(self.empty_sprite, (x, y))

                # add sprites
                if sprite_ind < self.index_to_add:
                    for i in range(0, len(self.sprites[sprite_ind])):
                        self.background.blit(self.sprites[sprite_ind][i], (x, y))

                sprite_ind += 1

        resized = self.pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.screen.blit(resized, (0, 0))
        self.pygame.display.flip()
        if save:
            self.pygame.image.save(self.background, "sheet.png")

    def add(self, to_add, offset=0):
        while self.index_to_add + offset >= len(self.sprites):
            self.sprites.append([])
        if to_add is not None:
            self.sprites[self.index_to_add + offset].append(to_add)

    def add_n(self):
        self.add(None)
        self.index_to_add += 1
        self.render_sheet()

    def add_sr(self):
        main = self.pygame.image.load('tiles/SR.png')
        echo1 = self.pygame.image.load('tiles/SR-Echo1.png')
        echo2 = self.pygame.image.load('tiles/SR-Echo2.png')
        self.add(main)
        self.add(echo1, 1)
        self.add(echo2, 3)
        self.index_to_add += 1
        self.render_sheet()

    def add_sl(self):
        main = self.pygame.image.load('tiles/SL.png')
        echo1 = self.pygame.image.load('tiles/SL-Echo1.png')
        echo2 = self.pygame.image.load('tiles/SL-Echo2.png')
        self.add(main)
        self.add(echo1, 1)
        self.add(echo2, 3)
        self.index_to_add += 1
        self.render_sheet()

    def add_su(self):
        main = self.pygame.image.load('tiles/SU.png')
        echo = self.pygame.image.load('tiles/SU-Echo.png')
        self.add(main)
        for i in range(1, 6):
            self.add(echo, 2*i)
        self.index_to_add += 1
        self.render_sheet()

    def add_sd(self):
        main = self.pygame.image.load('tiles/SD.png')
        echo = self.pygame.image.load('tiles/SD-Echo.png')
        self.add(main)
        for i in range(1, 6):
            self.add(echo, 2*i)
        self.index_to_add += 1
        self.render_sheet()

    def add_scru(self):
        main = self.pygame.image.load('tiles/SCRU.png')
        echo = self.pygame.image.load('tiles/SCRU-Echo.png')
        self.add(main)
        for i in range(1, 6):
            self.add(echo, 2*i)
        self.index_to_add += 1
        self.render_sheet()

    def add_scrd(self):
        main = self.pygame.image.load('tiles/SCRD.png')
        echo = self.pygame.image.load('tiles/SCRD-Echo.png')
        self.add(main)
        for i in range(1, 6):
            self.add(echo, 2*i)
        self.index_to_add += 1
        self.render_sheet()

    def add_zi(self):
        main = self.pygame.image.load('tiles/ZI.png')
        self.add(main)
        self.index_to_add += 1
        self.render_sheet()

    def add_zo(self):
        main = self.pygame.image.load('tiles/ZO.png')
        self.add(main)
        self.index_to_add += 1
        self.render_sheet()

    def add_tl(self):
        main = self.pygame.image.load('tiles/TL.png')
        echo = self.pygame.image.load('tiles/T-Echo.png')
        self.add(main)
        self.add(echo, 1)
        self.index_to_add += 1
        self.render_sheet()

    def add_tr(self):
        main = self.pygame.image.load('tiles/TR.png')
        echo = self.pygame.image.load('tiles/T-Echo.png')
        self.add(main)
        self.add(echo, 1)
        self.index_to_add += 1
        self.render_sheet()

    def add_tb(self):
        main = self.pygame.image.load('tiles/TB.png')
        self.add(main)
        self.index_to_add += 1
        self.render_sheet()

    def add_ss(self):
        main = self.pygame.image.load('tiles/SS.png')
        echo = self.pygame.image.load('tiles/SS-Echo.png')
        self.add(main)
        self.add(echo, 1)
        self.index_to_add += 1
        self.render_sheet()

    def save(self):
        self.render_sheet(True)
