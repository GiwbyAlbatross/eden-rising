try:
    import pygame.locals as _locals
except ModuleNotFoundError:
    __import__("logging").getLogger(__name__).warning(
        "PyGame not found. Continuing assuming that we are the server and therefore won't need it."
    )
else:
    TRANSPARENT = _locals.SRCALPHA
    MV_LEFT  = _locals.K_z
    MV_RIGHT = _locals.K_c
    MV_JUMP  = _locals.K_x
PORT = 7776
TICK_RATE = 2
