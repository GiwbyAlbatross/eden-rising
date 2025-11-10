"handling of data files for eden rising, needs CWD to be root of game dir"

from typing import Optional
import logging

try:
    import tomllib as tomli
except ModuleNotFoundError:
    import tomli

logger = logging.getLogger(__name__)

rsrclocfile = "assets/data/resourcelocations.toml"
texturelocations: Optional[dict] = None


def get_texturelocation(loc: str, fallback: str = ""):
    global texturelocations
    if texturelocations is None:
        logger.info(f"ResourceLocations file previously not loaded. Loading {rsrclocfile!r}")
        texturelocations = tomli.load(open(rsrclocfile, 'rb'))
    subkeys = loc.split(".")
    table = texturelocations
    for key in subkeys:
        if key in table:
            table = table[key]
        else:
            logger.error(f"Key {key!r} from {loc!r} could not be found.")
    return table  # weird iterative thing, but it works
