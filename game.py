import random

import pygame

from block import Block
from constants import DARK_GREY, BASE_FONT, WHITE, BLACK, RED, GREEN, GRID_LINE
from world import World


class Game:
    def __init__(self, world):
        self.world = world
        self._running = True
        self._display_surf = None
        self.scale = 20
        self.size = (self.width, self.height) = ((world.width + 1) * self.scale, (world.height + 1) * self.scale)
        self.timer_event = None
        self.clock = 0

    def on_init(self):
        pygame.init()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        pygame.display.set_caption('Robot World')
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(DARK_GREY)
        self.draw_grid()

    def clear_screen(self):
        self._display_surf.fill(DARK_GREY)

    def draw_grid(self):
        for x in range(0, self.width, self.scale):
            pygame.draw.line(self._display_surf, GRID_LINE, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.scale):
            pygame.draw.line(self._display_surf, GRID_LINE, (0, y), (self.width, y), 1)

    def draw_world(self):
        for entity in self.world.map:
            x = entity.x
            y = entity.y
            if x is not None and y is not None and x >= 0 and y >= 0:
                name = entity.name
                scale_x = x * self.scale
                scale_y = y * self.scale
                color = WHITE
                if name == 'R':
                    if entity.holding:
                        color = RED
                    else:
                        color = GREEN
                self.text((scale_x + 1, scale_y + 1), name, 16, color, BLACK)

    def text(self, location, phrase, size, front_color, back_color):
        font = pygame.font.Font(BASE_FONT, size)
        font.set_bold(True)
        text = font.render(phrase, True, front_color, back_color)
        text_rect = text.get_rect()
        text_rect.topleft = location
        self._display_surf.blit(text, text_rect)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self._running = False

    def on_execute(self):
        if self.on_init() is False:
            self._running = False
        while self._running:
            pygame.time.delay(100)
            for event in pygame.event.get():
                self.on_event(event)
            self.clear_screen()
            self.draw_grid()
            for _ in range(1):
                self.run_one_bot_cycle()
            self.draw_world()
            pygame.display.update()
        self.on_cleanup()

    def run_one_bot_cycle(self):
        robots = []
        for entity in self.world.map:
            if entity.name == 'R':
                robots.append(entity)
        for bot in robots:
            bot.do_something()

    @staticmethod
    def on_cleanup():
        pygame.quit()


def build_block_square():
    global y, x, block
    for y in range(10):
        for x in range(10):
            block = Block(x + 15, y + 15)
            world.add(block)


def build_random_blocks():
    global _, x, y, block
    for _ in range(50):
        x = random.randint(0, world.width - 1)
        y = random.randint(0, world.height - 1)
        block = Block(x, y)
        world.add(block)


if __name__ == "__main__":
    world = World(40, 40)
    build_random_blocks()
    # build_block_square()
    # world.add(Block(0, 0))
    # world.add(Block(0, world.height))
    # world.add(Block(world.width , 0))
    # world.add(Block(world.width, world.height))

    for _ in range(20):
        bot =  world.add_bot(10, 20)
    game = Game(world)
    game.on_execute()
