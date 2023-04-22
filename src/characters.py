import pygame
from os import path
from src.agreements import *


# Class for character movement animation - stores sequence of images,
# giving correct animation. Frames_for image must be divisor of FPS // 2 = 60
# for every picture to be shown for equal amount of time
class CharacterAnimation:
    def __init__(self, frames_for_image):
        self.images = []
        self.frames_for_image = frames_for_image

    # Add image to sequence
    def append(self, char_type, animation_type, pic_order):
        self.images.append(pygame.image.load(
            path.join(DATA_PATH,
                      IMAGE_PATH,
                      TEXTURES_PATH,
                      CHARACTERS_PATH,
                      f'{char_type}_{animation_type}_{pic_order}.png')))

    # Get image from sequence
    def __getitem__(self, key):
        if key <= FPS // 4:
            return self.images[key // self.frames_for_image]
        else:
            return self.images[(FPS // 2 - key) // self.frames_for_image]

    # Get length of sequence
    def __len__(self):
        return len(self.images)


# Base character class - all other characters are derived from this class
class Human(pygame.sprite.Sprite):
    def __init__(self, coords, window=None, char_type='human'):
        super().__init__()
        self.window = window
        self.init_physics(coords, char_type)
        self.init_ability()
        self.init_image()

    # Initialize physic constants for character
    def init_physics(self, coords, char_type):
        self.char_type = char_type
        self.x, self.y = coords
        self.x_speed = 2.75
        self.x_vector, self.y_vector = 0, 0
        self.y_speed = 0
        self.y_vel = 60
        self.hp = 1
        self.hit_tick = 0
        self.invincibility_duration = 2000
        self.invincible = False
        self.in_air = False
        self.jump_amount = 0
        self.jump_speed = -2500
        self.jump_cooldown = 200
        self.can_jump = True
        self.jump_tick = None
        self.rect = pygame.Rect(self.x, self.y, 8, 25)

    # Initialize ability constants for character
    def init_ability(self):
        self.ability_duration = None
        self.ability_cooldown = None
        self.can_use_ability = None
        self.ability_use_tick = None

    # Initialize animations for character
    def init_image(self):
        self.stand_image = pygame.image.load(
            path.join(DATA_PATH,
                      IMAGE_PATH,
                      TEXTURES_PATH,
                      CHARACTERS_PATH,
                      f'{self.char_type}.png'))

        self.running_left_anim = CharacterAnimation(20)

        for i in range(1,
                       (FPS // 2) // self.running_left_anim.frames_for_image):
            self.running_left_anim.append(self.char_type, 'running_left', i)

        self.running_right_anim = CharacterAnimation(20)

        for i in range(1,
                       (FPS // 2) // self.running_right_anim.frames_for_image):
            self.running_right_anim.append(self.char_type, 'running_right', i)

        self.cur_running_left_anim = 0
        self.cur_running_right_anim = 0

        self.image = self.stand_image
        self.mask = pygame.mask.from_surface(self.image)

    # Update hitbox position
    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    # Update health. 'check' mode is required if character haven`t changed his
    # hp, but invincibility needs to be updated
    def update_hp(self, mode=''):
        if not self.invincible and mode != 'check':
            self.hp -= 1
            self.window.sound.play(
                pygame.mixer.Sound(path.join(DATA_PATH,
                                             SOUND_PATH,
                                             'classic_hurt.wav')))
            self.invincible = True
            self.hit_tick = pygame.time.get_ticks()
        else:
            tick = pygame.time.get_ticks()

            if tick - self.hit_tick >= self.invincibility_duration:
                self.invincible = False
            elif tick - self.hit_tick >= self.invincibility_duration // 4:
                self.image = pygame.image.load(
                    path.join(DATA_PATH,
                              IMAGE_PATH,
                              TEXTURES_PATH,
                              CHARACTERS_PATH,
                              f'{self.char_type}.png'))

    # Moves character by x and check if it can be moved - else returns x to
    # previous position
    def move_by_x(self, blocks, commands):
        previous_x = self.x

        if 'left' in commands:
            self.x -= self.x_speed
        if 'right' in commands:
            self.x += self.x_speed

        self.update_rect()

        colliding_with_blocks = pygame.sprite.spritecollide(self, blocks, False)

        if colliding_with_blocks:
            block = colliding_with_blocks[0]
            if previous_x > block.x:
                self.x = block.x + 25
            else:
                self.x = block.x - 8
            self.update_rect()

        self.x_vector = self.x - previous_x

    # Moves character by y and check if it can be moved - else returns y to
    # previous position and puts it on ground if
    # needed
    def move_by_y(self, blocks, commands):
        previous_y = self.y

        if 'jump' in commands:
            self.jump()

        if self.in_air:
            self.fall()

        colliding_with_blocks = pygame.sprite.spritecollide(self, blocks, False)

        if colliding_with_blocks:
            block = colliding_with_blocks[0]

            if previous_y > block.y:
                self.y = block.y + 25
            else:
                self.y = block.y - 25

            self.step_on_ground()
            self.update_rect()
            self.y_vector = 0
        else:
            if self.y_speed != 0:
                self.y_vector = self.y - previous_y
            else:
                self.y_vector = 0
            self.increase_fall_speed()

    # Restores constants as if character was on ground
    def step_on_ground(self):
        if self.y_speed > 0:
            self.jump_amount = 1
        self.y_speed = 0
        self.in_air = False

    # Increases fall speed
    def increase_fall_speed(self):
        self.in_air = True
        self.y_speed += self.y_vel

    # Moves player by y coordinate as if it is falling
    def fall(self):
        if self.in_air:
            self.y += self.y_speed / 1000

        self.update_rect()

    # Sets player state as if it jumps if possible
    def jump(self):
        if self.jump_amount > 0:
            if self.can_jump:
                self.jump_amount -= 1
                self.y_speed = self.jump_speed
                self.jump_tick = pygame.time.get_ticks()
                self.can_jump = False
            else:
                tick = pygame.time.get_ticks()

                if tick - self.jump_tick >= self.jump_cooldown:
                    self.can_jump = True

    # Check if player collides with spikes
    def check_spike_collision(self, spikes):
        for spike in spikes:
            if pygame.sprite.collide_mask(self, spike):
                self.update_hp()

    # Check if player collides with orbs
    def check_orb_collision(self, orbs):
        if pygame.sprite.spritecollide(self, orbs, True):
            self.jump_amount += 1

    # Method for ability usage - undefined for basic character
    def use_ability(self, mode=''):
        pass

    # Updates player animation depending on state
    def update_image(self):
        if -0.5 <= self.y_vector <= 0.5:
            if not self.in_air:
                self.load_run_image()
        else:
            self.load_fall_image()

    # Sets player image to running state
    def load_run_image(self, upside_down=False):
        if self.x_vector < 0:
            self.cur_running_left_anim = \
                (self.cur_running_left_anim + 1) % (FPS // 2)
            self.image = self.running_left_anim[self.cur_running_left_anim]
            if upside_down:
                self.image = pygame.transform.flip(self.image, False, True)
            self.cur_running_right_anim = 0
        elif self.x_vector > 0:
            self.cur_running_right_anim = \
                (self.cur_running_right_anim + 1) % (FPS // 2)
            self.image = self.running_right_anim[self.cur_running_right_anim]
            if upside_down:
                self.image = pygame.transform.flip(self.image, False, True)
            self.cur_running_left_anim = 0
        else:
            self.cur_running_right_anim = 0
            self.cur_running_left_anim = 0
            self.image = self.stand_image
            if upside_down:
                self.image = pygame.transform.flip(self.image, False, True)

    # Sets player image to falling state
    def load_fall_image(self, upside_down=False):
        if self.x_vector > 0:
            self.image = pygame.image.load(
                path.join(DATA_PATH,
                          IMAGE_PATH,
                          TEXTURES_PATH,
                          CHARACTERS_PATH,
                          f'{self.char_type}_jumping_right.png'))
            if upside_down:
                self.image = pygame.transform.flip(self.image, False, True)
        elif self.x_vector < 0:
            self.image = pygame.image.load(
                path.join(DATA_PATH,
                          IMAGE_PATH,
                          TEXTURES_PATH,
                          CHARACTERS_PATH,
                          f'{self.char_type}_jumping_left.png'))
            if upside_down:
                self.image = pygame.transform.flip(self.image, False, True)
        else:
            self.image = pygame.image.load(
                path.join(DATA_PATH,
                          IMAGE_PATH,
                          TEXTURES_PATH,
                          CHARACTERS_PATH,
                          f'{self.char_type}_jumping.png'))
            if upside_down:
                self.image = pygame.transform.flip(self.image, False, True)

    # Updates state of player
    def update(self, commands, blocks, spikes, orbs):
        self.move_by_x(blocks, commands)
        self.move_by_y(blocks, commands)
        self.check_spike_collision(spikes)
        self.check_orb_collision(orbs)
        self.update_hp(mode='check')
        self.use_ability(mode='check')

        if 'ability' in commands:
            self.use_ability()

        self.update_image()


# Character that has 3 hp instead of 1
class Jonathan(Human):
    def __init__(self, coords, parent=None):
        super().__init__(coords, parent, char_type='jonathan')
        self.hp = 3
        self.jump_speed = 1.5 * self.jump_speed


# Character that can change its gravity
class Pucci(Human):
    def __init__(self, coords, parent=None):
        super().__init__(coords, parent, char_type='pucci')
        self.ability_cooldown = 2000
        self.ability_use_tick = None
        self.can_use_ability = True
        self.upside_down = False

    def use_ability(self, mode=''):
        if self.can_use_ability and mode != 'check':
            self.y_vel = -self.y_vel
            self.jump_speed = -self.jump_speed
            self.can_use_ability = False
            self.window.field_screen._change_ability_icon(False)
            self.ability_use_tick = pygame.time.get_ticks()
            self._change_orientation()
        else:
            tick = pygame.time.get_ticks()

            if self.ability_use_tick is not None:
                if tick - self.ability_use_tick >= self.ability_cooldown:
                    self.can_use_ability = True
                    self.window.field_screen._change_ability_icon(True)

    def step_on_ground(self):
        if self.y_speed >= 0 and self.y_vel > 0 or self.y_speed <= 0 and \
                self.y_vel < 0:
            self.jump_amount = 1
        self.y_speed = 0
        self.in_air = False

    def update_image(self):
        if -0.5 <= self.y_vector <= 0.5:
            if not self.in_air:
                self.load_run_image(self.upside_down)
        else:
            self.load_fall_image(self.upside_down)

    def _change_orientation(self):
        if self.upside_down:
            self.upside_down = False
        else:
            self.upside_down = True


# Character that can increase its x speed for short amount of time
class Joseph(Human):
    def __init__(self, coords, parent=None):
        super().__init__(coords, parent, char_type='joseph')
        self.ability_duration = 230
        self.ability_cooldown = 2000
        self.can_use_ability = True
        self.ability_use_tick = None
        self.ability_ended = False

    def use_ability(self, mode=''):
        if self.can_use_ability and mode != 'check':
            self.x_speed *= 2
            self.can_use_ability = False
            self.window.field_screen._change_ability_icon(False)
            self.ability_use_tick = pygame.time.get_ticks()
            self.ability_ended = False
        else:
            tick = pygame.time.get_ticks()

            if self.ability_use_tick is not None:
                if tick - self.ability_use_tick >= self.ability_cooldown:
                    self.can_use_ability = True
                    self.window.field_screen._change_ability_icon(True)
                    self.ability_use_tick = None
                if not self.ability_ended:
                    if tick - self.ability_use_tick >= self.ability_duration:
                            self.x_speed = 2.75
                            self.ability_ended = True


# Character that gains invincibility for short amount of time
class Diavolo(Human):
    def __init__(self, coords, parent=None):
        super().__init__(coords, parent, char_type='diavolo')
        self.ability_duration = 5000
        self.ability_cooldown = 25000
        self.can_use_ability = True
        self.ability_use_tick = None

    def use_ability(self, mode=''):
        if self.can_use_ability and mode != 'check':
            self.invincible = True
            self.can_use_ability = False
            self.window.field_screen._change_ability_icon(False)
            self.ability_use_tick = pygame.time.get_ticks()
            if self.window.field_screen.music_playing:
                self.window.music.set_volume(SOUND_LEVEL / 2)
            self.window.sound.play(pygame.mixer.Sound(
                path.join(DATA_PATH,
                          SOUND_PATH,
                          'diavolo_ability.wav')))

    def update_hp(self, mode=''):
        if not self.invincible and mode != 'check':
            self.hp -= 1
            self.window.sound.play(pygame.mixer.Sound(
                path.join(DATA_PATH,
                          SOUND_PATH,
                          'classic_hurt.wav')))
            self.invincible = True
            self.hit_tick = pygame.time.get_ticks()
        else:
            tick = pygame.time.get_ticks()

            if not self.can_use_ability:
                if tick - self.ability_use_tick >= self.ability_duration:
                    self.can_use_ability = True
                    self.window.field_screen._change_ability_icon(True)
                    self.invincible = False
                    if self.window.field_screen.music_playing:
                        self.window.music.set_volume(SOUND_LEVEL)
            else:
                if tick - self.hit_tick >= self.invincibility_duration:
                    self.invincible = False
