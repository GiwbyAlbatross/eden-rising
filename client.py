import sys
import logging
import argparse
import pygame  # ?
import pygamescenes
import eden
import eden.client

eden.IS_SERVER = False
LOG_LOCATION = 'eden-rising-client-latest.log'

logging.basicConfig(
    format="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s", datefmt="%H:%M:%S",
    filename='/dev/stdout' if sys.stdout.isatty() or (not __debug__) else LOG_LOCATION,
    level=(logging.DEBUG if __debug__ else logging.INFO)
)
logger = logging.getLogger(__name__)


class EdenRisingClient(pygamescenes.game.BaseGame):
    TICK_RATE = 1000 // eden.constants.TICK_RATE
    me: eden.client.player.RenderedPlayer
    twochunks: pygame.Surface
    lastchunkId: int
    chunk_render_offset: int # in pixels
    pandirection: int

    def init(self, **kwargs):
        self.me = eden.client.player.Brian()
        chunkId = self.me.chunkId
        self.rendered.add(self.me)
        self.ticked.add(self.me)
        self.lastchunkId = chunkId
        self.pandirection = 0
        self.chunk_render_offset = 0
        logger.info("Rendering world (first time).")
        self.twochunks = pygame.Surface([640, 176])
        self.twochunks.blit(self.render_chunk(self.load_chunk(chunkId)), (0, 0))
        self.twochunks.blit(self.render_chunk(self.load_chunk(chunkId + 1)), (320, 0))
        self.registerhandler(eden.constants.START_PAN_EVENT, self.pan_event_handler)

    def update_tick(self) -> None:
        "tick entities and do network sync multiplayer stuff"
        for entity in self.ticked:
            entity.tick()

    def load_chunk(self, chunkId: int) -> list[list[int]]:
        return [[0 for _ in range(20)] for _ in range(11)]

    def render_chunk(self, chunk: list[list[int]]) -> pygame.Surface:
        blocktypes = [] # paths to block textures, TODO: use eden.client.data
        # 1280,704 is size of chunk on screen, up to two chunks are loaded at once
        # chunks are 20x11 blocks, each block having a 16x16 texture, scaled up 4x later
        rendered = pygame.Surface([320, 176])
        rendered.fill([255, 0, 200])  # TODO: render actual blocks in chunk
        for y, blks in enumerate(chunk):
            for x, blktype in enumerate(blks):
                try:
                    blktxtr = eden.gfxutil.loadimg(blocktypes[blktype])
                except IndexError:
                    #logger.warning(f"Unrecognised blocktype: {blktype!r}. Continuing, assuming server is modded.") # when individual block rendering doesn't exist, just clogs the terminal
                    blktxtr = eden.gfxutil.create_notfound([16,16])
                rendered.blit(blktxtr, (x*16, y*16))
        return rendered

    def render_frame(self) -> pygame.surface.Surface:
        "render self.rendered entities to screen, doing terraria-like faux-camera movement stuff"
        scrollspeed = 0.1
        targetoffset = 1280 if self.pandirection>0 else 0
        chunkId = self.me.chunkId
        if self.lastchunkId != chunkId and self.chunk_render_offset == targetoffset:
            logger.info("Rendering world (again).")
            self.twochunks.blit(self.render_chunk(self.load_chunk(chunkId)), (0, 0))
            self.twochunks.blit(
                self.render_chunk(self.load_chunk(chunkId + 1)), (320, 0)
            )
            self.lastchunkId = chunkId
            self.chunk_render_offset = 0
        self.scr.fill([0,0,0])
        self.scr.blit(pygame.transform.scale_by(self.twochunks, 4), (self.chunk_render_offset, 0))
        for entity in self.rendered:
            entity.render(self.scr)
        f3txt = eden.gfxutil.render_text(f"chunkId: {chunkId!r}, logical_pos: {self.me.logical_pos!r}, render_pos: {self.me.rect.center}", 0, 12)
        f3rect= f3txt.get_rect(topleft=(16, 704))
        self.scr.fill([64,64,64], f3rect)
        self.scr.blit(f3txt, f3rect)
        self.chunk_render_offset = (self.chunk_render_offset+targetoffset*scrollspeed) / 1+scrollspeed
        return self.scr

    def pan_event_handler(self, event: pygame.event.Event):
        direction = event.direction
        self.pandirection = direction
        if direction > 0:
            # moving right
            self.chunk_render_offset = 0
        else:
            # moving left
            self.chunk_render_offset = 1280
        logger.info(f"Handled pan event: direction: {event.direction!r}")

    #def update_frame(self, dt: float = 1 / 60) -> None:
    #    pass

    def cleanup(self) -> None:
        pass

def initialiseall():
    pygame.init()       # TODO:
    pygame.font.init()  # - optimise this for what is in use
    pygame.mixer.init() # - ...
    logger.debug("Initialised pygame.font and pygame.mixer")
    eden.client.player.init()
    logger.debug("Initialised brian textures.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # add arguments, etc
    initialiseall()
    args = parser.parse_args()
    game = EdenRisingClient(
        [1280, 720], open_window=True, tick_rate=eden.constants.TICK_RATE
    )
    pygamescenes.run_game(game)
