# Eden Rising

Based on a fictional video game in a stage play I was involved in and decided to make an actual game of.

## File structure

#### avocado
Dependency library `avocado` from `GiwbyAlbatross/multiplayer-avocado`

#### pygamescenes
Dependency library `pygamescenes` from `GiwbyAlbatross/PygameScenes`

#### assets
Assets for the game itself. Inside is `img` (images), `audio` (audio), and `misc` (anything else)

#### eden
The main source code of the game.

#### `client.py`
Just the client of the game, no main menu or login or settings prompt, taking command-line arguments.

#### `server.py`
The server, of the game. Pretty chill and doesn't care if you have a hacked client ;)

## Installation

Installing basic dependancies:
```
python3 -m ensurepip && python3 -m pip install -r requirements.txt
```

## Running

To start the full game in the end you would run `python3 main.py` but I haven't implemented a main menu or launcher or anything so thst will fail. `python3 client.py <settings-file> <server-ip>` will suffice for now to start the client. `python3 server.py [world-file] 0.0.0.0` will start the server serving on all interfaces.

## Development

To run the standard checks locally run the following commands:
```
python3 -m pip install devrequirements.txt
./runchecks.sh
```