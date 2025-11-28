import math
import os.path
import logging
import pygame
from pygamescenes.entity import AbstractEntity
import eden
from eden.gfxutil import render_text, loadimg
from eden.constants import TRANSPARENT, MV_LEFT, MV_JUMP, MV_RIGHT, CHUNK_WIDTH, CHUNK_HEIGHT, FALL_THROUGH
from eden.logic import LogicalPlayer
from .data import get_texturelocation

BRIAN_SIZE = (76, 168)
scr_w = 1280
scr_h = 720

logger = logging.getLogger(__name__)
brianlogger = logging.getLogger(__name__ + ".Brian")


class RenderedPlayer(AbstractEntity, LogicalPlayer):
    GRAVITY_ACCEL: float = 980.0
    JUMP_HEIGHT: float = 512.0
    BOUNCINESS: float = 0.45
    SPEED: float = 128.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_keystrokes(self, pressed_keys):
        #pressed_keys = pygame.key.get_pressed()
        self.mv.x *= 0.003
        speed = self.SPEED
        if not self.is_on_ground(): speed *= 1.25
        if pressed_keys[MV_JUMP]: speed *= 1.01
        if pressed_keys[MV_LEFT]:
            self.mv.x -= speed  # pixels per second
        if pressed_keys[MV_RIGHT]:
            self.mv.x += speed  # pixels per second
        if pressed_keys[MV_JUMP] and self.get_block_standing_on() != 0 and (self.logical_pos.y%1)<0.1:
            logger.debug(f"[JUMPING]: height above block {(self.logical_pos.y%1)}")
            self.mv.y -= self.JUMP_HEIGHT

    def update(self, dt: float = 1 / 50):
        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        #logger.info("Doing update method")
        if (self.logical_pos.x < 0) or (self.logical_pos.x > CHUNK_WIDTH):
                self.mv.y *= 0.1 # The Void dampens vertical movement or smth idk dude
        #mv = self.mv * dt
        if self.get_block_standing_on() != 0:
            if (self.logical_pos.y%1)<0.2 and (not mods&FALL_THROUGH):
                self.mv.y = -(abs(self.mv.y) * self.BOUNCINESS)
                self.rect.bottom = 704 - (math.floor(self.logical_pos.y)*64)
            else:
                self.mv.y += self.GRAVITY_ACCEL*dt
        else:
            self.mv.y += self.GRAVITY_ACCEL*dt
        self.process_keystrokes(keys)
        self.rect.move_ip(self.mv*dt)
        if self.rect.bottom >= 704:
            self.rect.bottom = 704 # prevents being under world
        #if (self.get_block_standing_on() != 0) and (self.logical_pos.x > 0) and (self.logical_pos.x < CHUNK_WIDTH):
        #    # no gravity outside the chunk
        #    self.mv.y = -(abs(self.mv.y) * self.BOUNCINESS)
        #    #self.logical_pos.y = 0.0
        #    #self.rect.bottom = 704
        #    #self.rect.bottom -= 16
        #    self.logical_pos.y = (704 - self.rect.bottom) / 64
        #    self.rect.bottom = 704 - (math.floor(self.logical_pos.y)*64)
        #    if self.is_on_ground(1.0):
        #        for i in range(1, CHUNK_HEIGHT):
        #            try:
        #                #logger.debug(f"Under floor logic: x: {self.logical_pos.x}, y: {self.logical_pos.y}, yoffset: {i}, ~y: {self.logical_pos.y+i}, blktype: {self.chunk[math.floor(self.logical_pos.y+i)][math.floor(self.logical_pos.x)]}")
        #                blktype = self.chunk[math.floor(self.logical_pos.y+i)][math.floor(self.logical_pos.x)]
        #                self.rect.bottom -= 16*i
        #                if blktype == 0: break
        #                #if self.is_on_ground(i): break
        #            except IndexError:
        #                logger.warning(f"Under floor logic triggered IndexError")
        #else:
        #    self.mv.y += self.GRAVITY_ACCEL * dt
        self.logical_pos.y = (704 - self.rect.bottom) / 64
        # note that logical_pos is an awful homemade
        # Vector2 class which lacks stuff and is slow
        self.logical_pos.x = self.rect.centerx / 64
        if self.logical_pos.x > CHUNK_WIDTH:
            #logger.debug(f"Moving right chunkwise. x: {self.logical_pos.x}")
            #self.logical_pos.x -= 16.0
            #self.rect.centerx = self.logical_pos.x * 64
            #self.chunkId += 1
            pygame.event.post(
                pygame.event.Event(eden.constants.START_PAN_EVENT, direction=1)
            )
        elif self.logical_pos.x < 0.0:
            #logger.debug(f"Moving left chunkwise. x: {self.logical_pos.x}")
            self.logical_pos.x += CHUNK_WIDTH
            self.rect.centerx = self.logical_pos.x * 64
            # self.chunkId -= 1
            pygame.event.post(
                pygame.event.Event(eden.constants.START_PAN_EVENT, direction=-1)
            )
        if self.logical_pos.y > 16:
            self.mv += self.GRAVITY_ACCEL*dt

    def render(self, chunkrenderoffset: int, surf: pygame.Surface) -> pygame.Rect:
        # collision debug
        pygame.draw.rect(surf, [25,255,2], pygame.Rect([math.floor(self.logical_pos.x)*64, 704 - math.floor(self.logical_pos.y)*64],[64,64]), 4)
        
        return surf.blit(self.surf, self.rect.move(chunkrenderoffset, 0))
    def tick(self) -> None:
        pass


class Brian(RenderedPlayer):
    mv: pygame.Vector2
    idleimg: pygame.Surface

    def __init__(self, trait: str = "Boring", pos: tuple[int, int] = (0, scr_h - 200)):
        super().__init__()
        self.init(trait, pos)
        self.surf = pygame.Surface(BRIAN_SIZE, TRANSPARENT)
        self.rect = self.surf.get_rect(center=pos)
        self.mv = pygame.Vector2(0.0, 0.0)

    def update(self, dt: float = 1 / 60):
        super().update(dt)
        self.surf.blit(self.idleimg, (0, 0))

    def render_nametag(self, surf: pygame.Surface):
        s = render_text(self.username.strip(" ") + " Brian")
        r = s.get_rect(bottom=self.rect.top, centerx=self.rect.centerx)
        surf.blit(s, r)


def init():
    idlebrianpath = os.path.join(
        get_texturelocation("entity.brian.root"),
        get_texturelocation("entity.brian.idle"),
    )
    if os.path.exists(idlebrianpath):
        Brian.idleimg = pygame.transform.scale_by(loadimg(idlebrianpath), 4)
    else:
        logger.error(f"Idle Brian Texture path {idlebrianpath!r} does not exist.")
        brianlogger.warn(
            f"Idle Brian Texture path {idlebrianpath!r} does not exist, using blank green surface."
        )
        Brian.idleimg = pygame.Surface(BRIAN_SIZE)
        Brian.idleimg.fill([0, 255, 0])
