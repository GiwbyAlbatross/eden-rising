import sys
import logging
import argparse
import pygame  # ?
import pygamescenes
import eden

eden.IS_SERVER = False

logger = logging.getLogger(__name__)


class EdenRisingClient(pygamescenes.game.BaseGame):
    TICK_RATE = 1000 // eden.constants.TICK_RATE
    me: eden.player.RenderedPlayer

    def init(self, **kwargs):
        self.me = eden.client.player.Brian()

    def update_tick(self) -> None:
        "tick entities and do network sync multiplayer stuff"
        for entity in self.ticked:
            if entity not in self.entities:
                self.entities.add(entity)  # add unknown entity to entities list
            entity.tick()

    def load_chunk(self, chunkId: int) -> list[list[int]]:
        return []

    def render_chunk(self, chunk: list[list[int]]) -> pygame.Surface:
        # 1280,704 is size of chunk on screen, up to two chunks are loaded at once
        # chunks are 20x11 blocks, each block having a 16x16 texture, scaled up 2x later
        rendered = pygame.Surface([320, 176])
        rendered.fill((255, 0, 255))  # TODO: render actual blocks in chunk
        return rendered

    def render_frame(self) -> pygame.surface.Surface:
        "render self.rendered entities to screen, doing terraria-like faux-camera movement stuff"
        twochunks = pygame.Surface([2560, 704])
        self.scr.blit(self.backdrop, (0, 0))
        for entity in self.rendered:
            entity.render(self.scr)
        return self.scr


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # add arguments, etc
    args = parser.parse_args()
    game = EdenRisingClient(...)
    game.init()
    pygamescenes.run_game(game)
