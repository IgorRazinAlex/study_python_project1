import pygame
from os import path
from src.agreements import *


# End screen class
class End:
    def __init__(self, window=None):
        self.window = window
        self._init_text()

    # Initializes text on screen
    def _init_text(self):
        self.title = 'Congratulations!'
        self.subtitle1 = 'You won! Press ESC for another try'
        self.subtitle2 = 'Game made by igor_kiiisliy'
        self.title_font = pygame.font.Font(
            pygame.font.match_font('lucidasans'), 72)
        self.subtitle_font = pygame.font.Font(
            pygame.font.match_font('lucidaconsole'), 20)

    # Processes player inputs
    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                self.window.cur_screen = 'start_screen'
                self._reload_music()

    # Reloads music
    def _reload_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path.join(DATA_PATH,
                                          SOUND_PATH,
                                          'start_screen.wav'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    # Draws screen
    def _draw_screen(self, screen):
        screen.fill(pygame.Color('black'))
        self._draw_text(screen)

    # Draws text
    def _draw_text(self, screen):
        string_title = self.title_font.render(
            self.title, True, pygame.Color('white'))
        rect_title = string_title.get_rect()
        rect_title = rect_title.move(240, 30)
        screen.blit(string_title, rect_title)

        string_subtitle1 = self.title_font.render(
            self.subtitle1, True, pygame.Color('white'))
        rect_subtitle1 = string_subtitle1.get_rect()
        rect_subtitle1 = rect_subtitle1.move(100, 220)
        screen.blit(string_subtitle1, rect_subtitle1)

        string_subtitle2 = self.subtitle_font.render(
            self.subtitle2, True, pygame.Color('white'))
        rect_subtitle2 = string_subtitle2.get_rect()
        rect_subtitle2 = rect_subtitle2.move(40, 570)
        screen.blit(string_subtitle2, rect_subtitle2)
