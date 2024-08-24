import pygame

from block import Block
from bot import Bot
from constants import GREY, DARK_GREY, LT_BLUE, BASE_FONT, WHITE, BLACK
from world import World


class Game:
    def __init__(self, world, bot):
        self.world = world
        self.bot = bot
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
            pygame.draw.line(self._display_surf, LT_BLUE, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.scale):
            pygame.draw.line(self._display_surf, LT_BLUE, (0, y), (self.width, y), 1)

    def draw_world(self):
        for entity in self.world.map:
            x = entity.x
            y = entity.y
            name = entity.name
            scale_x = x * self.scale
            scale_y = y * self.scale
            self.text((scale_x + 1, scale_y + 1), name, 16, WHITE, BLACK)

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
            pygame.time.delay(1000)
            for event in pygame.event.get():
                self.on_event(event)
            self.clear_screen()
            self.draw_grid()
            self.bot.do_something()
            self.draw_world()
            pygame.display.update()
        self.on_cleanup()

    @staticmethod
    def on_cleanup():
        pygame.quit()


if __name__ == "__main__":
    world = World(40, 40)
    block = Block(20, 20)
    world.add(block)
    bot = Bot(10, 20)
    world.add(bot)
    game = Game(world, bot)
    game.on_execute()
