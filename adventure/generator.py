#import numpy as np
import random as rd
import sys
from time import process_time
from adventure.flavor_lists import *
from django.contrib.auth.models import User
from adventure.models import Player, Room

tic = process_time()

def room_check(grids, x, y, x_max, y_max):
    if x == 0 or y == 0 or x == x_max or y == y_max:
        new_dirs = []
    else:
        new_dirs = ["n", "e", "s", "w"]
        if grids[y-1][x] != 0:
            new_dirs.remove("n")
        if grids[y+1][x] != 0:
            new_dirs.remove("s")
        if grids[y][x-1] != 0:
            new_dirs.remove("w")
        if grids[y][x+1] != 0:
            new_dirs.remove("e")
    return new_dirs

def name_gen():
    global houses
    global extra_adjectives
    b = rd.randint(1,3)
    if b == 1 or b == 2:
        if houses != []:
            m = rd.choice(houses)
            houses.remove(m)
            b_name = f"{m} Smurf's house"

        elif extra_adjectives != []:
            m = rd.choice(extra_adjectives)
            extra_adjectives.remove(m)
            m = m.capitalize()
            b_name = f"{m} Smurf's house"
        else:
            b_name = "An empty house"
    if b == 3:
        b_name = f"Smurf {rd.choice(buildings)}"
    return b_name

def desc_gen():
    b_desc = f"{rd.choice(desc_start)} {rd.choice(desc_adj)}. {rd.choice(desc_mid)} {rd.choice(desc_noun)} {rd.choice(desc_end)}."
    return b_desc

class World():
    def __init__(self):
        self.grid = None
        self.rooms = None
        self.x_max = 0
        self.y_max = 0

    def make_rooms(self, room_max):
        self.grid = [0]
        self.rooms = []
        self.x_max = room_max
        self.y_max = room_max

        room_names = ("name1", "name2", "name3", "foyer")
        room_descriptions = ("desc1", "desc2", "desc3", "it's musty in here.")

        room_count = 1
        # Establish starting room
        entry_room = Room(id = 1, title = "Entry", description = "This is the start", x = 0, y = 0)

        previous_room = entry_room
        x = 0
        y = 0
        x_max = 1
        y_max = 1
        base_dir = ["n", "e", "s", "w"]
        self.rooms = [entry_room]

        main_room_count = room_max // 5
        # While loop to make a 'backbone' list of rooms with unique id's
        while room_count < main_room_count:
            # Set a random direction
            dir = rd.choice(("s", "e"))
            if dir == "e":
                x += 1
                if x > x_max:
                    x_max = x
            if dir == "s":
                y += 1
                if y > y_max:
                    y_max = y

            room = Room(id = room_count + 1, title = "Smurf Main Street",
                        description = "Smurfsville's main road. It's paved with blue cobblestones and is well maintained by Maintenance Smurf. Smurf dirt roads branch off of it.",
                        x = x, y = y)

            previous_room.connect_rooms(room, dir)
            previous_room = room

            self.rooms.append(room)

            # increase room_count and start over
            room_count += 1

        # After building a backbone, store room indexes in their positions in a
        # grid, for use in checking for overwrite conflicts and making a visual

        self.grid = [0] * (y_max+1)
        for i in range(len(self.grid)):
            self.grid[i] = [0] * (x_max+1)
        for room in self.rooms:
            self.grid[room.y][room.x] = room.id

        # Main cooridor is completed, and a grid is populated with room indecies
        # and empty spaces

        # Make a new while loop to make rooms branching off of existing rooms
        allowed_dir = []
        start_id = rd.randint(1,room_count-1)
        previous_room = self.rooms[start_id]
        x = previous_room.x
        y = previous_room.y
        allowed_dir = room_check(self.grid, x, y, x_max, y_max)

        while room_count >= main_room_count and room_count < room_max:
            allowed_dir = room_check(self.grid, x, y, x_max, y_max)
            if allowed_dir != []:
                dir = rd.choice(allowed_dir)
                if dir == "n":
                    y -= 1
                if dir == "s":
                    y += 1
                if dir == "e":
                    x += 1
                if dir == "w":
                    x -= 1
                dead_end_check = room_check(self.grid, x, y, x_max, y_max)
                if dead_end_check != []:
                    room = Room(id = room_count+1, title = "Smurf dirt road",
                            description = "a dirt path branching off of the main smurf street.",
                            x = x, y = y)
                else:
                    room = Room(id = room_count+1, title = name_gen(),
                            description = desc_gen(),
                            x = x, y = y)
                previous_room.connect_rooms(room, dir)
                self.rooms.append(room)
                self.grid[y][x] = room.id
                previous_room = room
                room_count += 1

            else:
                start_id = rd.randint(1,room_count-5)
                previous_room = self.rooms[start_id]
                x = previous_room.x
                y = previous_room.y

        #grid = np.array(self.grid)
        #np.set_printoptions(threshold=sys.maxsize)
        #print(grid)
        #print("There are", len(self.rooms), "rooms.")
        self.room_dictionaries = []
        r_dict = {}
        for room in self.rooms:
            r_dict = {'id': room.id, 'title': room.title, 'description': room.description,
                    'x': room.x, 'y': room.y}
            self.room_dictionaries.append(dict(r_dict))
        #print(rd.choice(self.room_dictionaries))
        return self.room_dictionaries
        return self.rooms
        return self.grid

n = 120 # Number of rooms goes here
w = World()
w.make_rooms(n)
toc = process_time()
print("World built in", toc - tic, "seconds.")
