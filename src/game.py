import pygame
from os import path
from src.menu import MainMenu
from src.rules import Rules
from src.agreements import *
from src.field import Field
from src.end import End


# Main class for game processing
class Game:
    def __init__(self):
        pygame.init()
        self._init_sound()
        self._init_font()
        self._init_screen()
        self._init_game_process()

    # Initialize sounds
    def _init_sound(self):
        pygame.mixer.init()
        self.music = pygame.mixer.Channel(0)
        self.sound = pygame.mixer.Channel(1)
        self.music.set_volume(SOUND_LEVEL)
        self.sound.set_volume(SOUND_LEVEL)

    # Initialize fonts
    def _init_font(self):
        pygame.font.init()

    # Initializes screen
    def _init_screen(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Through the Time and Space')
        self.cur_screen = 'start_screen'
        self.start_screen = MainMenu(window=self)
        self.rules_screen = Rules(window=self)
        self.field_screen = Field(window=self)
        self.end_screen = End(window=self)

    # Initializes game processing
    def _init_game_process(self):
        self.clock = pygame.time.Clock()
        self.running = False
        self.start_screen.start_music()

    # Main loop
    def run(self):
        self.running = True

        while self.running:
            self._process_events()
            self._draw_screen()
            self.update()
            pygame.display.flip()

            self.clock.tick(120)

        self._shut_down()

    # Process user inputs
    def _process_events(self):
        if self.cur_screen == 'start_screen':
            self.start_screen._process_events()
        elif self.cur_screen == 'rules_screen':
            self.rules_screen._process_events()
        elif self.cur_screen == 'game_screen':
            self.field_screen._process_events()
        elif self.cur_screen == 'end_screen':
            self.end_screen._process_events()

    # Draws screen
    def _draw_screen(self):
        if self.cur_screen == 'start_screen':
            self.start_screen._draw_screen()
        elif self.cur_screen == 'rules_screen':
            self.rules_screen._draw_screen()
        elif self.cur_screen == 'game_screen':
            self.field_screen._draw_screen(self.screen)
        elif self.cur_screen == 'end_screen':
            self.end_screen._draw_screen(self.screen)

    # Forces screen to update
    def update(self):
        if self.cur_screen == 'start_screen':
            pass
        elif self.cur_screen == 'rules_screen':
            pass
        elif self.cur_screen == 'game_screen':
            self.field_screen._update()
        elif self.cur_screen == 'end_screen':
            pass

    # Shuts down processes when exiting
    def _shut_down(self):
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()
