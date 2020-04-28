import random as rd
import pandas as pd
import numpy as np

class Bin():
    def __init__(self, items = None):
        if not items:
            self.items = []
        else:
            self.items = items

class Player(Bin):
    def __init__(self, name, c_room, items=None):
        super().__init__(items)
        self.name = name
        self.c_room = c_room

    def __str__(self):
        p = "Thou art in"+str(self.c_room) + "\n" + "In thy bag ye have:\n" + "\n".join([str(i) for i in self.items])
        return p

class Room():

    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.x = x
        self.y = y
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None

    def __str__(self):
        r = self.name + self.description
        # + "\n".join([str(i)] for i in self.items)
        return r

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")



class World():
    def __init__(self):
        self.grid = None
        self.rooms = None
        self.x_max = 0
        self.y_max = 0

    # def check_space(self, room, )

    def make_rooms(self, room_max):
        self.grid = [0]
        self.rooms = []
        self.x_max = room_max
        self.y_max = room_max

        room_names = ("name1", "name2", "name3", "foyer")
        room_descriptions = ("desc1", "desc2", "desc3", "it's musty in here.")

        room_count = 2
        # Establish starting room
        entry_room = Room(id = 1, name = "Entry", description = "This is the start", x = 0, y = 0)

        previous_room = entry_room
        x = 0
        y = 0
        x_max = 1
        y_max = 1
        allowed_dir = ("n", "e", "s", "w")
        self.rooms = [entry_room]

        # While loop to make a list of rooms with unique id's
        while room_count < room_max + 2:
            # Set a random direction in an allowed direction
            # if x > 0 and y > 0:
            #     dir = rd.choice(allowed_dir)
            # else:
            #     dir = rd.choice(("s", "e"))

            dir = rd.choice(("s", "e"))
            # Limiting the direction options to south and east so that it works
            # while I fix the overwriting problem

            # change the location, and change the allowed directions to prohibit
            # overwriting by backtrack
            if dir == "n":
                y -= 1
                allowed_dir = ("n", "e", "w")
            elif dir == "e":
                x += 1
                allowed_dir = ("n", "s", "e")
                if x > x_max:
                    x_max = x
            elif dir == "s":
                y += 1
                allowed_dir = ("e", "s", "w")
                if y > y_max:
                    y_max = y
            else:
                x -= 1
                allowed_dir = ("n", "s", "w")


            room = Room(id = room_count, name = rd.choice(room_names), description = rd.choice(room_descriptions),
                        x = x, y = y)

            previous_room.connect_rooms(room, dir)
            previous_room = room

            self.rooms.append(room)

            # return room_list
            room_count += 1

        self.grid = [0] * (y_max+1)
        for i in range(len(self.grid)):
            self.grid[i] = [0] * (x_max+1)
        for room in self.rooms:
            self.grid[room.y][room.x] = room.id

        for i in self.grid:
            print(i)
        return self.rooms
        return self.grid
'''
This method still allows for new rooms to overwrite old ones if north and west
are allowed.
When making a new room, choices are limited to just south and east, which will
make a long snakey set of rooms from top left to bottom right.
'''
n = 50 # Number of rooms goes here
w = World()
w.make_rooms(n)
