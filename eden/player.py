import pygame
from avocado.entity import RenderedPlayer
from avocado.util import render_text

BRIAN_SIZE = (64,128)
scr_w = 1280
scr_h = 720

class Brian(RenderedPlayer):
    logical_pos: pygame.Vector2 = pygame.Vector2(0.0, 0.0)
    def __init__(self, trait: str='Boring', pos: tuple[int,int] = (0,scr_h-16)):
        super().__init__(trait, pos)
        self.rect = pygame.FRect(pos, BRIAN_SIZE)
        self.surf = pygame.Surface(self.rect.size)
    def update_pos(self, dt: float=1000/60):
        mv = self.mv * (dt / 1000)
        self.rect.move_ip(mv)
        self.logical_pos.y = 0 - self.rect.centery/64
        self.logical_pos.x = 0 - self.rect.centerx/64
    def render_nametag(self, surf: pygame.Surface):
        s = render_text(self.username.decode('utf-8').strip(' ') + ' Brian')
        r = s.get_rect(bottom=self.rect.top, centerx=self.rect.centerx)
        surf.blit(s,r)
