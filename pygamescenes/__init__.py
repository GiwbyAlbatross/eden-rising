"an object-oriented interface for making simple to complex pygame games"
# intentionally left otherwise blank (for now)

import pygame

from . import game
from . import scene
from . import entity


def run_game(game: game.AbstractGame, *init_args, **init_kwargs) -> int:
    game.init(*init_args, **init_kwargs)
    while game.running:
        dt = game.clk.tick(game.TARGET_FPS)
        print(f"FPS: {game.clk.get_fps():.3f}", end="\r")
        game.process_events(pygame.event.get())
        game.update_frame(dt * 0.001)
        game.render_frame()
        pygame.display.flip()
    game.cleanup()
