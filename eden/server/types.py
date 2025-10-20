from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    type: str
    name: Optional[str] # only present if item has been renamed
    attributes: dict[str, Any]

class EntityState(BaseModel):
    entityID: Optional[str] # must be provided if not provided in URL/URI
    hashedpass: Optional[str] # SHOULD NOT BE SUPPLIED unless logging in/out (unless using guest account, in which case its contents are ignored)
    helditem: Optional[Item] # only supplied if an item is being held

class EntityPos2D(BaseModel):
    entityID: Optional[str] # must be provided if not provided in URL/URI
    x: float
    y: float

class WorldChunk(BaseModel):
    x: int
    y: int
    contents: list[list[int]] # numerical block ID is in use
