" main logic for eden risin, if any ;D "

class LogicalPlayer:
    logical_pos: pygame.Vector2
    username: str
    def init(self, trait: str, pos: tuple[int, int]) -> None:
        self.username = trait
        self.logical_pos = pygame.Vector2(0.0, 0.0)
        self.logical_pos.y = 0 - pos[0]/64
        self.logical_pos.x = 0 - pos[1]/64
    def is_on_ground(self):
        # presently just checks if you're on the floor but it will in future do block-collision
        self.logical_pos.y <= 0.0
    def tick(self) -> None:
        if not self.is_on_ground():
            self.mv.y += self.GRAVITY_ACCEL/20 # 20 ticks where this sorta stuff is processed
            #                                  # networking happens at other times, in threads
