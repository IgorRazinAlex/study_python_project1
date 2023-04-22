from os import path, listdir
from src.characters import *
from src.blocks import *
import csv
from src.agreements import *


# Class for level
class Field:
    def __init__(self, window=None):
        self.window = window
        self._init_icons()
        self._init_game_process()

    def start_music(self):
        self.window.music.stop()
        self.window.music.play(pygame.mixer.Sound(
            path.join(DATA_PATH, SOUND_PATH, 'arcadia.wav')), loops=-1)
        self.window.music.set_volume(SOUND_LEVEL)

    # Initialize icons
    def _init_icons(self):
        self.music_icons = [pygame.image.load(path.join(DATA_PATH,
                                                        IMAGE_PATH,
                                                        TEXTURES_PATH,
                                                        ICONS_PATH,
                                                        'music.png')),
                            pygame.image.load(path.join(DATA_PATH,
                                                        IMAGE_PATH,
                                                        TEXTURES_PATH,
                                                        ICONS_PATH,
                                                        'no_music.png'))]
        self.cur_music_icon = self.music_icons[0]
        self.music_icon_coords = (0, 575)


        self.sound_icons = [pygame.image.load(path.join(DATA_PATH,
                                                        IMAGE_PATH,
                                                        TEXTURES_PATH,
                                                        ICONS_PATH,
                                                        'sound.png')),
                            pygame.image.load(path.join(DATA_PATH,
                                                        IMAGE_PATH,
                                                        TEXTURES_PATH,
                                                        ICONS_PATH,
                                                        'no_sound.png'))]
        self.cur_sound_icon = self.sound_icons[0]
        self.sound_icon_coords = (50, 575)

        self.ability_icons = [pygame.image.load(
            path.join(DATA_PATH,
                      IMAGE_PATH,
                      TEXTURES_PATH,
                      ICONS_PATH,
                      'can_use_ability.png')),
                              pygame.image.load(
            path.join(DATA_PATH,
                      IMAGE_PATH,
                      TEXTURES_PATH,
                      ICONS_PATH,
                      'can_not_use_ability.png'))]
        self.cur_ability_icon = self.ability_icons[0]
        self.ability_icon_coords = (100, 575)

    # Initialize game processes
    def _init_game_process(self):
        self._init_music()
        self.commands = []
        self.level = 1
        self.field_translator = FieldTranslator()
        self.init_level()

    # Initialize music
    def _init_music(self):
        self.music_playing = True
        self.sound_playing = True
        self.music_change_tick = None
        self.sound_change_tick = None
        self.music_change_pause = 250
        self.sound_change_pause = 250

    # Initialize level loader
    def init_level(self):
        if self.level <= len(listdir(path.join(DATA_PATH, LEVEL_PATH))) - 1:
            self.level_objects = None
            self.read_level_data()
            self.init_obj_groups()
            self.set_objects()
            if self.music_playing:
                self.window.music.set_volume(SOUND_LEVEL)
        else:
            self.level = 0
            self.window.cur_screen = 'end_screen'
            self.window.music.stop()

    # Read data from level file
    def read_level_data(self):
        self.field_translator.read_file(f'{self.level}.csv')
        self.level_objects = self.field_translator.get_objects()

    # Initialize groups for objects
    def init_obj_groups(self):
        self.blocks = pygame.sprite.Group()
        self.orbs = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()

    # Spawns objects. Respawn parameter needed if level needs to be reset
    def set_objects(self, respawn=False):
        for obj in self.level_objects:
            obj_type, coords = obj['type'], (obj['x'], obj['y'])
            if not respawn:
                if obj_type in CHARACTERS:
                    self.spawn_player(obj_type, coords)
                elif obj_type.startswith('s'):
                    self.spawn_spike(obj_type, coords)
                elif obj_type.startswith('o'):
                    self.spawn_orb(coords)
                elif obj_type.startswith('b'):
                    self.spawn_block(obj_type, coords)
                elif obj_type.startswith('p'):
                    self.spawn_portal(coords)
            else:
                if obj_type.startswith('o'):
                    is_spawned = False
                    for orb in self.orbs.sprites():
                        if coords == (orb.x, orb.y):
                            is_spawned = True

                    if not is_spawned:
                        self.spawn_orb(coords)

    # Spawns player
    def spawn_player(self, name, coords):
        self.player_name = name
        self.player_start = coords

        if name == 'hum':
            self.player = pygame.sprite.GroupSingle(
                Human(coords, self.window))
        elif name == 'jon':
            self.player = pygame.sprite.GroupSingle(
                Jonathan(coords, self.window))
        elif name == 'jos':
            self.player = pygame.sprite.GroupSingle(
                Joseph(coords, self.window))
        elif name == 'puc':
            self.player = pygame.sprite.GroupSingle(
                Pucci(coords, self.window))
        elif name == 'dia':
            self.player = pygame.sprite.GroupSingle(
                Diavolo(coords, self.window))

    # Spawns spike
    def spawn_spike(self, spike_type, coords):
        self.spikes.add(Spike(coords, spike_type))

    # Spawns orb
    def spawn_orb(self, coords):
        self.orbs.add(Orb(coords))

    # Spawns block
    def spawn_block(self, block_type, coords):
        self.blocks.add(Block(coords, block_type))

    # Spawns portal
    def spawn_portal(self, coords):
        self.portal = pygame.sprite.GroupSingle(EndPortal(coords))

    # Processes inputs of player
    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.commands.append('left')
        if keys[pygame.K_RIGHT]:
            self.commands.append('right')
        if keys[pygame.K_SPACE]:
            self.commands.append('jump')
        if keys[pygame.K_x]:
            self.commands.append('ability')
        if keys[pygame.K_m]:
            self._mute_or_unmute_music()
        if keys[pygame.K_n]:
            self._mute_or_unmute_sound()

    # Draws screen
    def _draw_screen(self, screen):
        screen.fill(pygame.Color('black'))
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.spikes.draw(screen)
        self.orbs.draw(screen)
        self.portal.draw(screen)
        self._draw_icons(screen)

    # Draws icons
    def _draw_icons(self, screen):
        screen.blit(self.cur_music_icon, self.music_icon_coords)
        screen.blit(self.cur_sound_icon, self.sound_icon_coords)
        screen.blit(self.cur_ability_icon, self.ability_icon_coords)

    # Main logic in loop of updating game state
    def _update(self):
        self.player.update(self.commands, self.blocks, self.spikes, self.orbs)
        self.commands.clear()
        self.portal.sprite.update()

        if self.player.sprite.hp <= 0:
            self.spawn_player(self.player_name, self.player_start)
            self.set_objects(respawn=True)
            self._change_ability_icon(True)

        if self._player_out_of_bounds():
            self.spawn_player(self.player_name, self.player_start)
            self.set_objects(respawn=True)
            self._change_ability_icon(True)

        if self._player_reached_end():
            self._change_ability_icon(True)
            self.level = self.level + 1
            self.init_level()

    # bool statement if player is out of screen bounds
    def _player_out_of_bounds(self):
        if self.player.sprite.x > WINDOW_SIZE[0] - 25 or \
                self.player.sprite.x < 0:
            return True
        if self.player.sprite.y > WINDOW_SIZE[1] - 25 or \
                self.player.sprite.y < 0:
            return True

        return False

    # bool statement if player has reached end
    def _player_reached_end(self):
        return pygame.sprite.collide_rect(self.player.sprite,
                                          self.portal.sprite)

    # Mutes or unmutes music. Has a time period when player can`t mute or unmute
    # music after muting or unmuting it
    def _mute_or_unmute_music(self):
        if self.music_change_tick is None:
            if self.window.music.get_volume() == 0:
                self.window.music.set_volume(SOUND_LEVEL)
                self.cur_music_icon = self.music_icons[0]
            else:
                self.window.music.set_volume(0)
                self.cur_music_icon = self.music_icons[1]

            self.music_change_tick = pygame.time.get_ticks()
        else:
            tick = pygame.time.get_ticks()

            if tick - self.music_change_tick >= self.music_change_pause:
                self.music_change_tick = None
                self._mute_or_unmute_music()

    # Mutes or unmutes sounds. Has a time period when player can`t mute or
    # unmute sound after muting or unmuting it
    def _mute_or_unmute_sound(self):
        if self.sound_change_tick is None:
            if self.window.sound.get_volume() == 0:
                self.window.sound.set_volume(SOUND_LEVEL)
                self.cur_sound_icon = self.sound_icons[0]
            else:
                self.window.sound.set_volume(0)
                self.cur_sound_icon = self.sound_icons[1]

            self.sound_change_tick = pygame.time.get_ticks()
        else:
            tick = pygame.time.get_ticks()

            if tick - self.sound_change_tick >= self.sound_change_pause:
                self.sound_change_tick = None
                self._mute_or_unmute_sound()

    # Changes ability icon depending on if you can use it or not
    def _change_ability_icon(self, can_use):
        if can_use:
            self.cur_ability_icon = self.ability_icons[0]
        else:
            self.cur_ability_icon = self.ability_icons[1]


# Class that reads level from source file
class FieldTranslator:
    def __init__(self):
        self.field = []

    # Reads level data from file
    def read_file(self, file_name):
        self.field.clear()
        file_full_name = path.join(DATA_PATH, LEVEL_PATH, file_name)

        with open(file_full_name, mode='r', encoding='utf-8') as level:
            reader = csv.reader(level, delimiter=',')

            for i, line in enumerate(reader):
                obj_type, x, y = line[0], int(line[1]), int(line[2])
                obj = {'type': obj_type,
                       'x': 25 * x,
                       'y': 25 * y}
                self.field.append(obj)

    # Getter for data
    def get_objects(self):
        return self.field
