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

    def make_rooms(self, room_max):
        self.grid = [None] * room_max
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * room_max
        self.rooms = [None]
        self.x_max = room_max
        self.y_max = room_max

        room_names = ("name1", "name2", "name3", "foyer")
        room_descriptions = ("desc1", "desc2", "desc3", "it's musty in here.")

        room_count = 0
        # Establish starting room
        entry_room = Room(id = 0, name = "Entry", description = "This is the start", x = 0, y = 0)

        previous_room = entry_room
        id = 0
        x = 1
        y = 1
        x_max = 1
        y_max = 1
        x_min = 0
        y_min = 0
        # Loop will create rooms one at a time in a random available direction
        self.rooms = [entry_room]
        while room_count < room_max:
            id = previous_room.id
            # Set a random direction in an allowed direction
            if x > 0 and y > 0:
                rand_dir = rd.randint(0,3)
            else:
                rand_dir = rd.randint(0,1)

            # change the location
            if rand_dir == 2:
                dir = "n"
                y -= 1
            elif rand_dir == 1:
                dir = "e"
                x += 1
                # if x > x_max:
                #     x_max = x
                #     self.grid.resize(x_max,y_max)
            elif rand_dir == 0:
                dir = "s"
                y += 1
                # if y > y_max:
                #     self.grid.resize(x_max,y_max)
                #     y_max = y
            else:
                dir = "w"
                x -= 1

            # Expand the grid if a new room will be placed outside of it


            room = Room(id = room_count, name = rd.choice(room_names), description = rd.choice(room_descriptions),
                        x = x, y = y)

            # if self.grid[y,x] == 0:
            #     self.grid[y,x] = room.id


            previous_room.connect_rooms(room, dir)
            previous_room = room

            self.rooms.append(room)
            self.grid[y][x] = room.id
            # return room_list
            room_count += 1
        return self.rooms
        return self.grid

n = 10 # Number of rooms goes here
w = World()
w.make_rooms(n)
