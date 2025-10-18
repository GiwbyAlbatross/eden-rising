from typing import Optional
import pygame
import socket
import avocado
import pygamescenes
import eden
import time
import sys

pygame.init()

HOST = ('0.0.0.0', eden.PORT)

scr_w = 400
scr_h = 400
username = ('user' + str(hash('hello world')))[:8] # generate username or
if len(sys.argv) > 1: username = (sys.argv[-1]+'       ')[:8]  # use supplied username

def update_status(*args): # for debugging
    print(*args, ' '*24, end='\r', flush=True)
    #time.sleep(0.1)

update_status("Loading")

#scr = pygame.display.set_mode([scr_w, scr_h])

#players = pygame.sprite.Group()
#player_usernames = [username.encode('utf-8')]
#me = avocado.entity.RenderedPlayer(username)
#players.add(me)

#TICK = pygame.event.custom_type()
#pygame.time.set_timer(TICK, 1000//eden.TICK_RATE)

run = 1
clk = pygame.time.Clock()
#username = username.encode('utf-8')

update_status("Joining")

class MainGameplayScene(pygamescenes.scene.AbstractScene):
    me: avocado.entity.RenderedPlayer
    username: bytes # brian trait, as bytes
    players = pygame.sprite.Group()
    player_usernames: list[bytes]
    def __init__(self,
                 scr_size: tuple[int,int]=(1280,720),
                 dpy_flags: int=0, *,
                 open_window: bool=False,
                 screen: Optional[pygame.Surface]=None) -> None:
        self.running = 1
        self.scr_size = scr_size
        if open_window:
            self.scr = pygame.display.set_mode(scr_size, dpy_flags)
            self.scr_is_real = True
        elif screen is not None:
            self.scr = screen
            self.scr_is_real = False
            self.scr_size = self.scr.size
        else:
            self.scr_is_real = False
        self._eventhandlers = {}
        self.clk = pygame.time.Clock()
    def init(self, brian_trait: str) -> None:
        self.player_usernames = [brian_trait.encode('utf-8')]
        self.username = brian_trait.encode('utf-8')
        self.me = eden.player.Brian(brian_trait)
        self.players.add(self.me)
        try:
            with avocado.network.new_sock() as sock:
                sock.connect(HOST)
                sock.send(b'JON')
                sock.send(self.username)
        except ConnectionRefusedError:
            print("\033[1mCONNECTION REFUSED\033[0m", file=sys.stderr)
            print("Server probably isn't up. Quitting")
            update_status("Quitting")
            self.running = False
    def update_frame(self, dt: float=1/60):
        self.me.update_keypresses(pygame.key.get_pressed())
        for player in self.players:
            player.update_pos(dt*1000)
    def render_frame(self):
        self.scr.fill([0,0,0]) # remove when world loading exists
        # TODO: render world
        for player in self.players:
            self.scr.blit(player.surf, player.rect)
            player.render_nametag(self.scr)
        return self.scr
    def cleanup(self) -> int: return 0
    def update_tick(self) -> None:
        try:
            update_status("LSPing")
            with avocado.network.new_sock() as sock:
                sock.connect(HOST)
                sock.send(b'LSP')
                sock.send(self.username) # important part of protocol
                d = self.username
                while d != b'.'*8:
                    #update_status("LSPing:", d)
                    if d not in self.player_usernames:
                        players.add(avocado.entity.RenderedPlayer(d.decode('utf-8')))
                        player_usernames.append(d)
                    d = sock.recv(8)
            update_status("Beaming state to server")
            with avocado.network.new_sock() as sock:
                sock.connect(HOST)
                sock.send(b'SET')
                sock.send(self.username)
                sock.send(self.me.export_location())
            update_status("Fetching state from server")
            for player in self.players:
                if player is self.me: continue # optmisation and so on
                with avocado.network.new_sock() as sock:
                    sock.connect(HOST)
                    sock.send(b'GET')
                    sock.send(player.username)
                    player.update_location(sock.recv(avocado.network.ENTITY_POS_FRMT_LEN))
        except BrokenPipeError:
            print("\033[1mBROKEN PIPE\033[0m, skipping tick...", file=sys.stderr)
        except ConnectionResetError:
            print("\033[1mCONNECTION RESET\033[0m, skipping tick...", file=sys.stderr)
    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            update_status("Quitting")
            self.running = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = 0
            elif event.key == pygame.K_r:
                update_status("Respawning")
                # respawn
                me.kill()
                me = eden.player.Brian(username.decode('utf-8'))
                players.add(me)

class EdenRisingClient(pygamescenes.scene.MultiSceneRunnerGame):
    TICK_RATE = eden.TICK_RATE
    def init(self, *args, **kwargs):
        self.main = MainGameplayScene(screen=self.scr)
        self.main.init(username)
        self.current_scene = self.main
    def get_next_scene(self) -> pygamescenes.scene.AbstractScene:
        return self.main

"""while run:
    dt = clk.tick(60)
    for event in pygame.event.get():
        if event.type == TICK:
            try:
                update_status("LSPing")
                with avocado.network.new_sock() as sock:
                    sock.connect(HOST)
                    sock.send(b'LSP')
                    sock.send(username) # important part of protocol
                    d = username
                    while d != b'.'*8:
                        #update_status("LSPing:", d)
                        if d not in player_usernames:
                            players.add(avocado.entity.RenderedPlayer(d.decode('utf-8')))
                            player_usernames.append(d)
                        d = sock.recv(8)
                update_status("Beaming state to server")
                with avocado.network.new_sock() as sock:
                    sock.connect(HOST)
                    sock.send(b'SET')
                    sock.send(username)
                    sock.send(me.export_location())
                update_status("Fetching state from server")
                for player in players:
                    if player is me: continue # optmisation and so on
                    with avocado.network.new_sock() as sock:
                        sock.connect(HOST)
                        sock.send(b'GET')
                        sock.send(player.username)
                        player.update_location(sock.recv(avocado.network.ENTITY_POS_FRMT_LEN))
            except BrokenPipeError:
                print("\033[1mBROKEN PIPE\033[0m, skipping tick...", file=sys.stderr)
            except ConnectionResetError:
                print("\033[1mCONNECTION RESET\033[0m, skipping tick...", file=sys.stderr)
        elif event.type == pygame.QUIT:
            update_status("Quitting")
            run = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = 0
            elif event.key == pygame.K_r:
                update_status("Respawning")
                # respawn
                me.kill()
                me = avocado.entity.RenderedPlayer(username.decode('utf-8'))
                players.add(me)
    update_status("Rendering")
    scr.fill((0,0,0))
    me.update_keypresses(pygame.key.get_pressed())
    for player in players:
        player.update_pos(dt)
        scr.blit(player.surf, player.rect)
        player.render_nametag(scr)
    pygame.display.flip()

pygame.quit()
"""

if __name__ == '__main__':
    pygamescenes.run_game(EdenRisingClient((1280,720), open_window=True, tick_rate=2000))
