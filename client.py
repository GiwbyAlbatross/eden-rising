import os
import sys
import math
import random
import logging
import argparse
import pygame  # ?
import pygamescenes
import eden
import eden.logic
import eden.client

eden.IS_SERVER = False
LOG_LOCATION = "eden-rising-client-latest.log"

logging.basicConfig(
    format="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
    filename="/dev/stdout" if sys.stdout.isatty() or (not __debug__) else LOG_LOCATION,
    level=(logging.DEBUG if __debug__ else logging.INFO),
)
logger = logging.getLogger(f"client({__name__})")


class EdenRisingClient(pygamescenes.game.BaseGame):
    TARGET_FPS: int = 50
    TICK_RATE = 1000 // eden.constants.TICK_RATE
    me: eden.client.player.RenderedPlayer
    twochunks: pygame.Surface
    lastchunkId: int
    chunk_render_offset: int  # in pixels
    ispanning: bool
    pandirection: int
    justdidflags: dict

    def init(self, **kwargs):
        self.me = eden.client.player.Brian(pos=(200, self.scr_h - 200))
        chunkId = self.me.chunkId
        self.rendered.add(self.me)
        self.ticked.add(self.me)
        self.lastchunkId = chunkId
        self.ispanning = False
        self.pandirection = 0
        self.chunk_render_offset = 0
        self.justdidflags = {"pan": False}
        logger.info("Rendering world (first time).")
        self.twochunks = pygame.Surface([640, 176])
        chunk = self.load_chunk(chunkId)
        self.me.chunk = chunk
        self.twochunks.blit(self.render_chunk(chunk), (0, 0))
        self.twochunks.blit(self.render_chunk(self.load_chunk(chunkId + 1)), (320, 0))
        self.registerhandler(eden.constants.START_PAN_EVENT, self.pan_event_handler)

    def update_tick(self) -> None:
        "tick entities and do network sync multiplayer stuff"
        for entity in self.ticked:
            entity.tick()

    def load_chunk(self, chunkId: int) -> list[list[int]]:
        return eden.logic.generate_chunk()

    def render_chunk(self, chunk: list[list[int]]) -> pygame.Surface:
        blocktyperoot = "assets/textures/block/"
        blocktypes = eden.client.data.get_texturelocation("block.blocks")
        # 1280,704 is size of chunk on screen, up to two chunks are loaded at once
        # chunks are 20x11 blocks, each block having a 16x16 texture, scaled up 4x later
        rendered = pygame.Surface([320, 176])
        # rendered.fill([0, 0, 0])  # TODO: render actual blocks in chunk *DONE*
        for y, blks in enumerate(chunk):
            for x, blktype in enumerate(blks):
                if blktype == 0:
                    continue  # air isn't loaded
                try:
                    blktxtr = eden.gfxutil.loadimg(
                        os.path.join(blocktyperoot, blocktypes[blktype]) + ".png"
                    )
                except IndexError:
                    logger.warning(
                        f"Unrecognised blocktype: {blktype!r}. Continuing, assuming server is modded."
                    )  # when individual block rendering doesn't exist, just clogs the terminal
                    blktxtr = eden.gfxutil.create_notfound([16, 16])
                rendered.blit(blktxtr, (x * 16, 176 - y * 16))
        return rendered

    def render_frame(self) -> pygame.surface.Surface:
        "render self.rendered entities to screen, doing terraria-like faux-camera movement stuff"
        scrollspeed = 0.1
        targetoffset = 0 if self.pandirection < 0 else -1280
        # targetoffset = 0
        chunkId = self.me.chunkId
        # if self.lastchunkId != chunkId and self.chunk_render_offset == round(targetoffset):
        #    logger.info("Rendering world (again).")
        #    self.twochunks.blit(self.render_chunk(self.load_chunk(chunkId)), (0, 0))
        #    self.twochunks.blit(
        #        self.render_chunk(self.load_chunk(chunkId + 1)), (320, 0)
        #    )
        #    self.lastchunkId = chunkId
        #    self.chunk_render_offset = 0
        self.justdidflags["pan"] = False
        if self.lastchunkId != chunkId:
            logger.info("Rendering world (again).")
            chunk = self.load_chunk(chunkId)
            self.me.chunk = chunk  # used by is_on_ground
            self.twochunks.blit(self.render_chunk(chunk), (0, 0))
            self.twochunks.blit(
                self.render_chunk(self.load_chunk(chunkId + 1)), (320, 0)
            )
            self.lastchunkId = chunkId
        if (
            self.pandirection > 0
            and self.chunk_render_offset < -1279
            and self.ispanning
        ):
            logger.debug(f"render_frame pandirection>0 handler triggered")
            self.me.chunkId += 1
            self.me.logical_pos.x -= eden.constants.CHUNK_WIDTH
            self.me.rect.centerx = self.me.logical_pos.x * 64
            self.chunk_render_offset = 0.0
            self.ispanning = False
            self.justdidflags["pan"] = True
            logger.debug(f"x: {self.me.logical_pos.x}")
        elif self.pandirection < 0 and self.chunk_render_offset > -1 and self.ispanning:
            logger.debug(f"render_frame pandirection<0 handler triggered")
            self.ispanning = False
            self.chunk_render_offset = 0.0
            self.justdidflags["pan"] = True
        self.scr.fill([0, 0, 0])
        self.scr.blit(
            pygame.transform.scale_by(self.twochunks, 4), (self.chunk_render_offset, 0)
        )
        for entity in self.rendered:
            entity.render(self.chunk_render_offset, self.scr)
        if self.ispanning:
            self.chunk_render_offset = (
                self.chunk_render_offset + targetoffset * scrollspeed
            ) / (1 + scrollspeed)
        self.render_debug_text()
        return self.scr

    def render_debug_text(self):
        strings = []
        strings.append(f"chunkId: {self.me.chunkId!r}")
        strings.append(f"logical_pos: {self.me.logical_pos!r}")
        strings.append(f"mv: {self.me.mv}")
        strings.append(f"render_pos: {self.me.rect.bottomleft}")
        strings.append(f"chunkrenderoffset: {self.chunk_render_offset:.3f}")
        strings.append(
            f"ispanning: {self.ispanning}, pandirection: {self.pandirection}"
        )
        strings.append(f"blktype: {self.me.get_block_standing_on()}")
        strings.append(f"blktype+1: {self.me.get_block_standing_in()}")
        strings.append(f"is_on_ground: {self.me.is_on_ground()}")
        # try:
        #    strings.append(f"blktype: {self.me.chunk[math.floor(self.me.logical_pos.y)][math.floor(self.me.logical_pos.x)]}")
        # except IndexError:
        #    strings.append(f"outOfChunk")
        # try:
        #    strings.append(f"blktype+1: {self.me.chunk[math.floor(self.me.logical_pos.y+1.0)][math.floor(self.me.logical_pos.x)]}")
        # except IndexError:
        #    strings.append(f"outOfChunk+1")
        f3txt = eden.gfxutil.render_text(", ".join(strings), 0, 12)
        f3rect = f3txt.get_rect(topleft=(16, 708))
        self.scr.fill([64, 64, 64], f3rect)
        self.scr.blit(f3txt, f3rect)

    def pan_event_handler(self, event: pygame.event.Event):
        direction = event.direction
        if self.ispanning or self.justdidflags["pan"]:
            if self.pandirection == direction:
                return
        self.pandirection = direction
        self.ispanning = True
        if direction > 0:
            # moving right
            self.chunk_render_offset = 0
        else:
            # moving left
            self.chunk_render_offset = -1280
            self.me.chunkId += direction
        logger.debug(f"Handled pan event: direction: {event.direction!r}")

    def update_frame(self, dt: float = 1 / 60) -> None:
        self.time += dt
        self.me.update(dt)
        # for entity in self.ticked:
        #    entity.update(dt)

    def handle_keydown(self, event: pygame.event.Event) -> None:
        pass

    def cleanup(self) -> None:
        pass


def initialiseall():
    pygame.init()  # TODO:
    pygame.font.init()  # - optimise this for what is in use
    pygame.mixer.init()  # - ...
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
