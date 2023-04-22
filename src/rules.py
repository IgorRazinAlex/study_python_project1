import pygame
from os import path
from src.agreements import *


# Class for rules screen
class Rules:
    def __init__(self, window=None):
        self.window = window
        self._init_text()

    # Initializes text
    def _init_text(self):
        pygame.font.init()
        self.title = 'Rules:'
        self.rules = ['1. Move with arrow keys',
                      '2. Jump with space bar',
                      '3. Use ability on X key',
                      '4. Press "M" key to mute/unmute the music',
                      '5. Press "N" key to mute/unmute sound effects',
                      '',
                      'Press any key to continue']
        self.title_font = pygame.font.Font(
            pygame.font.match_font('lucidasans'), 72)
        self.rules_font = pygame.font.Font(
            pygame.font.match_font('lucidaconsole'), 20)
        self._set_text_coord()

    def _set_text_coord(self):
        self.text_coord = 180

    # Processes player inputs
    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self.window.cur_screen = 'game_screen'
                self.window.field_screen.start_music()

    # Draws screen
    def _draw_screen(self):
        self.window.screen.fill(pygame.Color('black'))
        self._draw_text(self.window.screen)

    # Draws text
    def _draw_text(self, screen):
        string_title = self.title_font.render(
            self.title, True, pygame.Color('white'))
        rect_title = string_title.get_rect()
        rect_title = rect_title.move(40, 30)
        screen.blit(string_title, rect_title)

        for line in self.rules:
            self._render_rules(line, screen)
            self.text_coord += 30

        self._set_text_coord()

    # Renders rules on screen
    def _render_rules(self, line, screen):
        string = self.rules_font.render(line, True, pygame.Color('white'))
        rect = string.get_rect()
        rect = rect.move((40, self.text_coord))
        screen.blit(string, rect)
