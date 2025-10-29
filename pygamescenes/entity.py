from __future__ import annotations
import pygame
import abc


class AbstractEntity(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    surf: pygame.Surface
    rect: pygame.rect.Rect | pygame.rect.FRect
    mv: pygame.math.Vector2  # pixels per second, retains speed despite FPS

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @abc.abstractmethod
    def tick(self) -> None:
        "tick this entity, do complex logic etc"
        pass

    # def init(self, *args, **kwargs) -> None: is not defined so multi-inherited classes can still use it

    @abc.abstractmethod
    def update(self, dt: float = 1 / 60) -> None:
        "update this entity's position and other per-frame stuff, `dt` is in seconds"
        self.rect.move_ip(self.mv * dt)

    def render(self, surf: pygame.Surface) -> pygame.Rect:
        "render this entity onto `surf` and return pixels changed"
        return surf.blit(self.surf, self.rect)

class VisualEffect(pygame.sprite.Sprite):
    def __repr__(self) -> str:
        clsName = self.__class__.__name__
        groups = len(self.groups())
        return f"<{clsName} VisualEffect (in {groups} groups)>"

    def is_on_screen(self) -> bool:
        rect = self.rect
        if rect.bottom < 0:
            return False
        if rect.top > scr_h:
            return False
        if rect.right < 0:
            return False
        if rect.left > scr_w:
            return False
        return True

    def kill(self, reason: str = ""):
        super().kill()

    def update_logic(self):
        pass

    def update_pos(self):
        pass

    def render(self, surf, show_hitboxes: bool = False):
        pass
