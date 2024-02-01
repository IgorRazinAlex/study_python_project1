import pygame
from src.menu import MainMenu


def test_title_movement():
    try:
        pygame.init()
    except Exception as err:
        raise Exception("Failed to load pygame")

    try:
        menu = MainMenu()
        assert menu.title_y == 30
        assert menu.title_speed == 0.01

        menu._move_title()

        assert menu.title_y == 30.0101
        assert menu.title_speed == 0.0101
    except Exception as err:
        pygame.quit()
        raise Exception("Title movement error")
