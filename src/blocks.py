import pygame
from os import path
from src.agreements import *


# Standard block
class Block(pygame.sprite.Sprite):
    def __init__(self, coords, type):
        super().__init__()
        self.x, self.y = coords
        self.rect = pygame.Rect(self.x, self.y, 25, 25)
        self.image = pygame.image.load(path.join(DATA_PATH,
                                                 IMAGE_PATH,
                                                 TEXTURES_PATH,
                                                 BLOCKS_PATH,
                                                 f'{type}.png'))


# Standard spike - colliding with it reduces hp if character isn`t invincible
class Spike(pygame.sprite.Sprite):
    def __init__(self, coords, type):
        super().__init__()
        self.x, self.y = coords
        self.rect = pygame.Rect(self.x, self.y, 25, 25)
        self.image = pygame.image.load(path.join(DATA_PATH,
                                                 IMAGE_PATH,
                                                 TEXTURES_PATH,
                                                 OBSTACLES_PATH,
                                                 f'{type}.png'))
        self.mask = pygame.mask.from_surface(self.image)


# Standard orb - colliding with it gives extra jump
class Orb(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.x, self.y = coords
        self.rect = pygame.Rect(self.x, self.y, 25, 25)
        self.image = pygame.image.load(path.join(DATA_PATH,
                                                 IMAGE_PATH,
                                                 TEXTURES_PATH,
                                                 OBSTACLES_PATH,
                                                 'o.png'))


# Standard portal - colliding with it finishes the level
class EndPortal(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.x, self.y = coords
        self.rect = pygame.Rect(self.x, self.y, 25, 25)
        self.image = pygame.image.load(path.join(DATA_PATH,
                                                 IMAGE_PATH,
                                                 TEXTURES_PATH,
                                                 OBSTACLES_PATH,
                                                 'e.png'))
        self.orig_image = self.image.copy()
        self.rot_angle = 0

    # Rotates portal
    def update(self):
        self.image = pygame.transform.rotate(self.orig_image, self.rot_angle)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rot_angle += 0.5
