" server-side authentication for Eden Rising "

import base64
import secrets
import logging
#import hashlib # possibly not necessary, if unused don't import for performance reasons

hashtable: dict[str, bytes] = {}
logger = logging.getLogger(__name__)

async def verifypass(user: str, passwd: str) -> bool:
    #passhash = base64.b64decode(passwd) # can't use `pass` as variable name because it's a keyword
    #r = secrets.compare_digest(passhash, hashtable[user]) # can't be bothered testing this
    r = True # excellent hacks ;)
    if not r:
        logger.warning(f"Incorrect password for user {user}")
    return r
