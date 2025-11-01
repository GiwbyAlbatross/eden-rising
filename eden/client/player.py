import os.path
import logging
import pygame
from pygamescenes.entity import AbstractEntity
from eden.gfxutil import render_text, loadimg
from eden.logic import LogicalPlayer
from .data import get_texturelocation

BRIAN_SIZE = (64, 128)
scr_w = 1280
scr_h = 720

logger = logging.getLogger(__name__)
brianlogger = logging.getLogger(__name__ + ".Brian")


class RenderedPlayer(AbstractEntity, LogicalPlayer):
    GRAVITY_ACCEL: float = 98.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt: float = 1 / 60):
        mv = self.mv * dt
        self.rect.move_ip(mv)
        self.logical_pos.y = (
            0 - self.rect.centery / 64
        )  # note that logical_pos is an awful homemade
        self.logical_pos.x = (
            0 - self.rect.centerx / 64
        )  # Vector2 class which lacks stuff and is slow


class Brian(RenderedPlayer):
    mv: pygame.Vector2
    idleimg: pygame.Surface

    def __init__(self, trait: str = "Boring", pos: tuple[int, int] = (0, scr_h - 16)):
        super().__init__()
        self.init(trait)
        self.surf = pygame.Surface(BRIAN_SIZE)
        self.rect = self.surf.get_rect(center=pos)
        self.mv = pygame.Vector2(0.0, 0.0)

    def render_nametag(self, surf: pygame.Surface):
        s = render_text(self.username.strip(" ") + " Brian")
        r = s.get_rect(bottom=self.rect.top, centerx=self.rect.centerx)
        surf.blit(s, r)


def init():
    idlebrianpath = os.path.join(
        get_texturelocation("entity.brian.root"),
        get_texturelocation("etity.brian.idle"),
    )
    if os.path.exists(idlebrianpath):
        Brian.idleimg = loadimg(idlebrianpath)
    else:
        logger.error(f"Idle Brian Texture path {idlebrianpath!r} does not exist.")
        brianlogger.warn(
            f"Idle Brian Texture path {idlebrianpath!r} does not exist, using blank pink surface."
        )
        Brian.idleimg = pygame.Surface(BRIAN_SIZE)
