# Eden Rising

Based on a fictional video game in a stage play I was involved in and decided to make an actual game of.

## File structure

#### pygamescenes
Dependency library `pygamescenes` from `GiwbyAlbatross/PygameScenes`

#### assets
Assets for the game itself. Inside is `textures` (textures), `audio` (audio), `data` (data files or any other data strcture i dont want to hard-code) and `misc` (anything else)

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
python3 -m pip install -r devrequirements.txt
./runchecks.sh
```

Those very same standard checks are run on every push, via GitHub Actions.

Code is formatted using the `black` formatting style. I use `ruff` however, for it is *much* faster. To format the code (which might not be done for every commit) run the following:
```
python3 -m pip install -r devrequirements.txt
ruff format
```

## Mechanics

### Character Rank

Players can be leved up by Queen Flows (sort of leader in the game, wheather or not they are a real player on the other end is debated in the play until the end where it is clear) or administrators (username: `Avesta` *you will probably never get it unless you saw the play.*)

#### Ranks
```
0. Brian # can interact with the world, each other and the market, etc
1. Mark or Val # reference to the original play, can do all the brian things, plus 'secret market' access and private missions
2. Playable Character with custom name # same as Mark/Val, but the admins/Flows trusts that they won't make a stupid entity name
3. King # can start wars and govern a faction, has the ability to provide kits of basic items to players in your faction, can't interact with world
```

### Controls

```
Z: move left on screen
X: jump
C: move right on screen
shift: go under the block you are standing on
```