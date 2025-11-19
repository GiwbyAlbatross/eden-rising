from typing import Sequence
import pygame


def render_text(text: str, line: int = 0, font_size: int = 16, **kwargs):
    "render text"
    # pos = [10, 8 + font_size*line]
    font = pygame.font.Font(kwargs.get("font_id", None), font_size)
    surf = font.render(text, True, kwargs.get("text_colour", (255, 255, 255)))
    return surf


def create_notfound(size: Sequence = [2, 2]) -> pygame.surface.Surface:
    tiny = pygame.Surface([2, 2])
    tiny.set_at((0, 0), [255, 0, 255])
    tiny.set_at((1, 1), [255, 25, 255])
    tiny.set_at((0, 1), (25, 25, 25))
    tiny.set_at((1, 0), (25, 25, 25))
    return pygame.transform.scale(tiny, size)


imgcache: dict[str, pygame.surface.Surface] = {}


def loadimg(path, *args, **kwargs):
    "load an image to a pygame surface, but it won't reload images that have already been reloaded, instead returning a reference"
    if path not in imgcache:
        imgcache[path] = pygame.image.load(path, *args, **kwargs)
    return imgcache[path]
