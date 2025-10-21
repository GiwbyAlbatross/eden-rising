import pygame
from pygamescenes.entity import AbstractEntity
from .gfxutil import render_text
from .logic import LogicalPlayer

BRIAN_SIZE = (64,128)
scr_w = 1280
scr_h = 720

class RenderedPlayer(AbstractEntity, LogicalPlayer):
    GRAVITY_ACCEL: float = 98.0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Brian(RenderedPlayer):
    mv: pygame.Vector2
    def __init__(self, trait: str='Boring', pos: tuple[int,int] = (0,scr_h-16)):
        super().__init__()
        self.init(trait)
        self.surf = pygame.Surface(BRIAN_SIZE)
        self.rect = self.surf.get_rect(center=pos)
        self.mv = pygame.Vector2(0.0, 0.0)
    def update(self, dt: float=1/60):
        mv = self.mv * dt
        self.rect.move_ip(mv)
        self.logical_pos.y = 0 - self.rect.centery/64 # note that logical_pos is an awful homemade
        self.logical_pos.x = 0 - self.rect.centerx/64 # Vector2 class which lacks stuff and is slow
    def render_nametag(self, surf: pygame.Surface):
        s = render_text(self.username.strip(' ') + ' Brian')
        r = s.get_rect(bottom=self.rect.top, centerx=self.rect.centerx)
        surf.blit(s,r)
