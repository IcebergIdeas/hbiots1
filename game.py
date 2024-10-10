import random

import pygame

from constants import MAGENTA, DARK_GREY, BASE_FONT, WHITE, BLACK, RED, GREEN, BLUE, GRID_LINE
from direct_connection import DirectConnection
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
        self.client_bots = []

    def add_bot(self, client_bot):
        self.client_bots.append(client_bot)

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
                        color = self.aroma_color(entity.holding.aroma)
                    else:
                        color = GREEN
                if name == 'B':
                    color = self.aroma_color(entity.aroma)
                self.text((scale_x + 1, scale_y + 1), name, 16, color, BLACK)

    def aroma_color(self, aroma):
                    match aroma:
                        case 0:
                            return RED
                        case 1:
                            return BLUE
                        case 2:
                            return WHITE
                        case 3:
                            return MAGENTA
                        case _:
                            return GREEN

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
            for _ in range(10):
                self.run_one_bot_cycle()
            self.draw_world()
            pygame.display.update()
        self.on_cleanup()

    def run_one_bot_cycle(self):
        for client_bot in self.client_bots:
            connection = DirectConnection(world)
            client_bot.do_something(connection)

    @staticmethod
    def on_cleanup():
        pygame.quit()


def build_block_square():
    # global y, x, block
    for y in range(10):
        for x in range(10):
            world.add_block(x + 15, y + 15)


def build_random_blocks():
    # global _, x, y, block
    for _ in range(150):
        x = random.randint(0, world.width - 1)
        y = random.randint(0, world.height - 1)
        world.add_block(x, y, None)


if __name__ == "__main__":
    world = World(40, 40)
    build_random_blocks()
    # build_block_square()
    # world.add(Block(0, 0))
    # world.add(Block(0, world.height))
    # world.add(Block(world.width , 0))
    # world.add(Block(world.width, world.height))

    game = Game(world)
    connection = DirectConnection(world)
    for _ in range(20):
        client_bot =  connection.add_bot(10, 20)
        game.add_bot(client_bot)
    game.on_execute()
