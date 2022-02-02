import csv


class Team:
    free_turns = 0
    alive_list = []
    dead_list = []
    active_mon = []
    trainer_name = ""
    all_mons = []
    point_value = 0
    has_rocks = False
    rock_turns = 0
    won_game = False
    lost_game = False

    def get_alive(self):
        return self.alive_list

    def get_dead(self):
        return self.dead_list

    def print_alive(self):
        alive = self.alive_list
        for mon in alive:
            print(mon.get_name())

    def print_dead(self):
        dead = self.dead_list
        for mon in dead:
            print(mon.get_name())

    def get_name(self):
        return self.trainer_name

    def set_dead(self):
        pass

    def get_active(self):
        alive = self.alive_list
        for mon in alive:
            if mon.get_is_active():
                return mon

    def get_active_name(self):
        active_mon = self.get_active()
        return active_mon.get_name()

    def analyze_points(self):
        total_points = 0
        for mon in self.alive_list:
            inFile = open('tierlist_spreadsheet.csv', 'r')
            reader = csv.reader(inFile)
            compare1 = mon.get_name()
            # print(f'we are now searching for : {mon.get_name()}')
            for row in reader:
                for col in row:
                    if col in [compare1]:
                        # print(f'found {compare1}')
                        answer = row.index(compare1) - 19
                        answer = answer * (-1)
                        # print(answer)
                        total_points = total_points + answer

        return total_points

    def set_rocks(self):
        self.has_rocks = True

    def get_rocks(self):
        return self.has_rocks

    def remove_rocks(self):
        self.has_rocks = False

    def add_rock_turn(self):
        self.rock_turns = self.rock_turns + 1
