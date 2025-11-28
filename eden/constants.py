#fmt: off
try:
    import pygame.locals as _locals
    import pygame as _pyg
except ModuleNotFoundError:
    __import__("logging").getLogger(__name__).warning(
        "PyGame not found. Continuing assuming that we are the server and therefore won't need it."
    )
else:
    TRANSPARENT = _locals.SRCALPHA
    MV_LEFT = _locals.K_z
    MV_RIGHT = _locals.K_c
    MV_JUMP = _locals.K_x
    FALL_THROUGH = _locals.KMOD_SHIFT
    START_PAN_EVENT = _pyg.event.custom_type()

PORT = 7776
TICK_RATE = 2
CHUNK_WIDTH = 20 # was 16 before CHUNK_WIDTH refactor, is still 16 for testing pan should be 20
CHUNK_HEIGHT = 11
