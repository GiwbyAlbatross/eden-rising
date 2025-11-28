"main logic for eden rising, if any ;D"

from typing import Optional
import math
import random
import logging
from asyncio import Lock as AsyncLock
from eden import IS_SERVER, CHUNK_WIDTH, CHUNK_HEIGHT
from eden.server.types import Item, EntityPos2D, EntityState

logger = logging.getLogger(__name__)


class Vector2:
    x: float
    y: float

    def __init__(self, x: float, y: Optional[float] = None):
        if y is None:
            self.x, self.y = x, x
        else:
            self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"<Vector2 (giwby-implementation) x: {self.x:.3f}, y: {self.y:.3f}>"


class LogicalPlayer:
    GRAVITY_ACCEL = 98.0
    logical_pos: Vector2
    username: str
    helditem: Optional[Item] = None
    inventory: list[Item]
    lock: AsyncLock
    chunkId: int
    chunk: list[list[int]]
    mv: "Vector2 | pygame.Vector2"

    def init(self, trait: str, pos: tuple[int, int], chunkId: int = 0) -> None:
        self.username = trait
        self.logical_pos = Vector2(0.0)
        self.mv = Vector2(0.0)
        self.logical_pos.y = 0 - pos[0] / 64
        self.logical_pos.x = pos[1] / 64
        self.chunkId = chunkId
        self.chunk = [[0 for _ in range(CHUNK_WIDTH)] for _ in range(CHUNK_HEIGHT)]
        self.inventory = []
        self.lock = AsyncLock()

    def get_block_standing_on(self) -> int:
        x = math.floor(self.logical_pos.x)
        y = math.floor(self.logical_pos.y)
        if y <= 0:
            return -1  # -1 is a solid block that shouldn't be rendered or whatever
        try:
            return self.chunk[y][x]
        except IndexError:
            return 0  # outside the world is air

    def get_block_standing_in(self) -> int:
        x = math.floor(self.logical_pos.x)
        y = math.floor(self.logical_pos.y + 1)
        if y <= 0:
            return -1  # -1 is a solid block that shouldn't be rendered or whatever
        try:
            return self.chunk[y][x]
        except IndexError:
            return 0  # outside the world is air

    def is_on_ground(self, yoffset: float = 0.0, xoffset: float = 0.0) -> bool:
        ### unused function? ###
        y = self.logical_pos.y + yoffset
        x = self.logical_pos.x + xoffset
        blktype = self.get_block_standing_on()
        return blktype != 0

    # def tick(self) -> None:
    #    if not self.is_on_ground():
    #        self.mv.y += (
    #            self.GRAVITY_ACCEL / 20
    #        )  # 20 ticks where this sorta stuff is processed
    #        #  # networking happens at other times, in threads

    def get_state(self) -> EntityState:
        # more state attributes will be added later but for now forget it
        es = EntityState(
            entityId=self.username, helditem=self.helditem, chunkId=self.chunkId
        )
        return es

    def set_state(self, state: EntityState) -> None:
        if self.username != state.entityID:
            logger.warning(
                f"EntityState passed to LogicalPlayer.set_state has incorrect username ({self.username} != {state.entityID})"
            )
        self.helditem = state.helditem
        self.chunkId = state.chunkId

    def getinv(self) -> list[Item]:
        return self.inventory

    def setinv(self, inv: list[Item]) -> bool:
        if len(inv) > 8:
            # more than 8 inventory items (not including hand or carried block)
            if IS_SERVER:
                logger.error(
                    f"Too many inventory items passed to LogicalPlayer.setinv: {len(inv)} > 8 : not updating inventory"
                )
                return False
            else:
                logger.warning(
                    f"Too many inventory items passed to LogicalPlayer.setinv: {len(inv)} > 8 : still updating inventory, assuming server is modded"
                )
        self.inventory = inv

    def getpos(self) -> EntityPos2D:
        return EntityPos2D(
            entityID=self.username,
            x=self.logical_pos.x,
            y=self.logical_pos.y,
            chunkId=self.chunkId,
        )

    def setpos(self, pos: EntityPos2D) -> None:
        if pos.entityID is not None:
            if self.username != pos.entityID:
                logger.warning(
                    f"EntityState passed to LogicalPlayer.setpos has incorrect username ({self.username} != {state.entityID})"
                )
        self.chunkId = pos.chunkId
        self.logical_pos.x, self.logical_pos.y = pos.x, pos.y


def generate_chunk() -> list[list[int]]:
    return [
        [max(0, random.randint(-3, 4)) for _ in range(CHUNK_WIDTH)]
        for _ in range(CHUNK_HEIGHT)
    ]
