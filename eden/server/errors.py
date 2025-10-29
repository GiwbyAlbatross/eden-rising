from typing import Optional
import logging

logger = logging.getLogger(__name__)
authlogger = logging.getLogger(__name__ + ".auth")

_missinginfo = {
    "response": "ERROR",
    "type": "notfound:info",
    "msg": "There is information missing from your request.",
}
_playernotfound = {
    "response": "ERROR",
    "type": "notfound:player",
    "msg": "The player you are attempting to access properties of could not be found",
}
_wrongpassword = {
    "response": "ERROR",
    "type": "permission:wrongpass",
    "msg": "Incorrect password",
}
_sketchyip = {
    "response": "ERROR",
    "type": "permission:sketchyip",
    "msg": "You are not able to log on as this player as another IP address has already logged on with your username.",
}
_unimplemented = {
    "response": "ERROR",
    "type": "unimplemented:*",
    "msg": "Whatever you tried to access is simply not implemented.",
}


def missinginfo(client_host, user: str) -> dict:
    logger.info(
        f"User at {client_host} produced a malformed request with missing information."
    )
    return _missinginfo


def notfound(client_host: str, user: str) -> dict:
    logger.info(
        f"User at {client_host} attempted to access properties of nonexistant user {user}"
    )
    return _playernotfound


def wrongpass(client_host: str, user: str) -> dict:
    logger.warning(f"User at {client_host} attempted unauthorised access to {user}")
    authlogger.info(
        f"User at {client_host} attempted to log in as {user} with incorrect password."
    )
    return _wrongpassword


def sketchyip(client_host: str, user: str) -> dict:
    logger.warning(f"User at {client_host} attempted unauthorised access to {user}")
    authlogger.info(
        f"User at {client_host} attempted to set properties of {user} from a different IP to {user}'s logon IP"
    )
    return _sketchyip


def unimplemented(featname: Optional[str] = None) -> dict:
    r = _unimplemented.copy()
    if featname is None:
        logger.info("Someone tried to access an unimplemented feature")
    else:
        r["msg"] = f"The feature {featname!r} is not implemtented yet."
        logger.info(f"Someone tried to access unimplemented feature {featname!r}")
    return r
