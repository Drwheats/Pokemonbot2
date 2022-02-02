class Pokemon:
    def __init__(self):
        self.name = ''
        self.hit_points = 100
        self.used_rocks = False
        self.has_live_rocks = False
        self.mons_statused = 0
        self.is_active = False
        self.owner = ''
        self.typing = []
        self.nickname = ''
        self.moves = []
        self.has_nickname = False
        self.total_rock_turns = 0
        self.is_mega = False

    def set_mega(self):
        self.is_mega = True
        print(self.is_mega)

    def get_mega(self):
        return self.is_mega

    def get_nickname(self):
        return self.nickname

    def set_nickname(self, x):
        self.has_nickname = True
        unparsed_nick = x
        name = self.get_name()
        name = unparsed_nick.replace(f'({name})', '')
        name = name.strip()
        self.nickname = name

    def get_typing(self):
        return self.typing

    def set_typing(self, x):
        self.typing = x

    def get_name(self):
        return self.name

    def set_name(self, x):
        self.name = x

    def set_owner(self, x):
        self.owner = x

    def get_owner(self):
        return self.owner

    def get_is_active(self):
        if self.is_active:
            return True

    def set_is_active(self):
        self.is_active = True
        print(f'{self.get_name()} is now ACTIVE.')
    def set_is_inactive(self):
        self.is_active = False
        print(f'{self.get_name()}.')

    def set_live_rocks(self):
        self.has_live_rocks = True

    def add_move(self, x):
        self.moves.append(x)

    def get_moves(self):
        return self.moves

    def most_used_move(self):
        print(f"{self.name}'s most used move is % s" % (max(set(self.moves), key=self.moves.count)))
