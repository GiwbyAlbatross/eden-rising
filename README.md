# Eden Rising

Based on a fictional video game in a stage play I was involved in and decided to make an actual game of.

## File structure

#### pygamescenes
Dependency library `pygamescenes` from `GiwbyAlbatross/PygameScenes`

#### assets
Assets for the game itself. Inside is `img` (images), `audio` (audio), and `misc` (anything else)

#### eden
The main source code of the game.

#### `client.py`
Just the client of the game, no main menu or login or settings prompt, taking command-line arguments.

#### `server`
The server of the game, using Uvicorn ASGI and FastAPI.

## Installation

**Installing basic dependancies** (client):
```
python3 -m ensurepip && python3 -m pip install -r requirements.txt
```

**Installing server dependancies** (the server uses some libraries the average user doesn't need):
```
python3 -m pip install -r server/requirements.txt
```

## Running

To start the full game in the end you would run `python3 main.py` but I haven't implemented a main menu or launcher or anything so thst will fail. `python3 client.py <settings-file> <server-ip>` will suffice for now to start the client. 
Not that the client itself exists ;D

To start the server, use the `uvicorn server.main:api`, provided you have installed the server dependancies (shown above).

## Development

To run the standard checks locally run the following commands:
```
python3 -m pip install devrequirements.txt
./runchecks.sh
```

Those very same standard checks are run on every push, via GitHub Actions.
