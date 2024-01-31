import os
from src.game import Game


if __name__ == '__main__':
    os.environ['SDL_AUDIODRIVER'] = 'alsa'
    os.environ['AUDIODEV'] = 'pulse'
    game = Game()
    game.run()
