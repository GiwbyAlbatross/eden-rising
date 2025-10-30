import sys
import argparse
import pygame  # ?
import pygamescenes
import eden

eden.IS_SERVER = False

class EdenRisingClient(pygamescenes.game.BaseGame):
    TICK_RATE = 1000 // eden.constants.TICK_RATE
    def update_tick(self) -> None:
        "tick entities and do network sync multiplayer stuff"
        for entity in self.ticked:
            if entity not in self.entities:
                self.entities.add(entity)  # add unknown entity to entities list
            entity.tick()
    def render_chunk(self, chunk: list[list[int]]) -> pygame.Surface:
        # 1280,704 is size of chunk on screen, up to two chunks are loaded at once
        rendered = pygame.Surface([1280,704])
    def render_frame(self) -> pygame.surface.Surface:
        "render self.rendered entities to screen, doing terraria-like faux-camera movement stuff"
        self.scr.blit(self.backdrop, (0, 0))
        for entity in self.rendered:
            entity.render(self.scr)
        return self.scr

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # add arguments, etc
    args = parser.parse_args()
    game = EdenRisingClient(...)
    game.init()
    pygamescenes.run_game(game)
