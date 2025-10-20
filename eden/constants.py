try:
    import pygame.locals as _locals
except ModuleNotFoundError:
    __import__('logging').getLogger(__name__).warning("PyGame not found. Continuing assuming that we are the server and therefore won't need it.")
PORT = 7776
TICK_RATE = 2