#! /usr/bin/env python3
# coding: utf8

import random


class Maze:

    def __init__(self, size_x, size_y):
        """ The maze is in deux parts : irremovable (wall, floor, ...) and movable (characters, items, ...)
            The free_way dict contains the irremovable part where movable part can evoluate.
            The movable dict contains what can move """
        self.size_x = size_x
        self.size_y = size_y
        self.free_way = {}
        self.create_irremovable_part()
        self.movable = {}
        self.create_movable_part()
        self.authorized_places = {}

    def create_irremovable_part(self):
        """ Transforms the content of the file into a dictionary, which contains: a position as key and a type of
            elements. Positions do not apply to walls, it's the free way """
        with open("res/maze.txt", "r") as maze_file:
            y = 0
            for line in maze_file:
                x = 0
                for column in line:
                    if column != "W":
                        self.free_way[(x, y)] = column
                    x = x + 1
                y = y + 1

        # Begin's position is random
        position = self.give_random_position(self.free_way)
        self.free_way[position] = "B"


    def create_movable_part(self):
        """ Give position and create movable items """

        # Where a new movable item can be placed
        self.authorized_places = self.free_way.copy()

        loop = True
        for position in self.free_way:
            # Guardian's position is same as Exit
            if self.free_way[position] == "E":
                self.movable["G"] = position
            # MacGyver's position is same as Begin
            elif self.free_way[position] == "B":
                self.movable["M"] = position
            elif self.free_way[position] == "E":
                del self.authorized_places[position]
            elif self.free_way[position] == "B":
                del self.authorized_places[position]

        # Random position for Needle, Tube, Aether
        self.place_to_collect("N")
        self.place_to_collect("T")
        self.place_to_collect("A")

    def give_random_position(self, authorized_places):
        x = random.randint(0, self.size_x - 1)
        y = random.randint(0, self.size_y - 1)
        if (x, y) not in authorized_places:
            return self.give_random_position(authorized_places)
        return (x, y)

    def place_to_collect(self, kind):
        position = self.give_random_position(self.authorized_places)
        self.movable[kind] = position
        del self.authorized_places[position]