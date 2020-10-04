#! /usr/bin/env python3
# coding: utf8

import random

from Movable import Character, Syringe
from Constantes import *


class Maze:
    """ Determine the content of the labyrinth, i.e. the kind of items and their positions """

    def __init__(self, size_x, size_y):
        """ The maze have two parts : irremovable (wall, floor, ...) and movable (characters, items, ...)
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
                for column in line.strip():
                    if column != "W" and column != "\n":
                        self.free_way[(x, y)] = column
                        if column == "E":
                            exit_position = (x, y)
                    x = x + 1
                y = y + 1

        # Begin's position is random, but not at exit's position
        loop = True
        while loop:
            position = self.give_random_position(self.free_way)
            if position != exit_position:
                loop = False
        self.free_way[position] = "B"

    def create_movable_part(self):
        """ Give position and create movable items """

        # Where a new movable item can be placed
        self.authorized_places = self.free_way.copy()

        for position in self.free_way:
            # Guardian's position is same as Exit
            if self.free_way[position] == "E":
                self.create_character("G", position)
            # MacGyver's position is same as Begin
            elif self.free_way[position] == "B":
                self.create_character("M", position)

        # Random position for Needle, Tube, Aether
        self.create_Syringe("N")
        self.create_Syringe("T")
        self.create_Syringe("A")

    def give_random_position(self, authorized_places):
        """ Give random position if free place 
        :rtype: object
        :param authorized_places: 
        :return: 
        """
        position = (random.randint(0, self.size_x - 1), random.randint(0, self.size_y - 1))
        if position not in authorized_places:
            return self.give_random_position(authorized_places)
        return position

    def create_character(self, kind, position):
        """ To create a movable and to indicate that the place is not free for deposit other movable """
        self.movable[kind] = Character(kind, position)
        del self.authorized_places[position]

    def create_Syringe(self, kind):
        """ Give position, create a piece of Syringe and indicate that the place is not free """
        position = self.give_random_position(self.authorized_places)
        self.movable[kind] = Syringe(kind, position)
        del self.authorized_places[position]

    def move_macgyver(self, movement):
        """ If free position, move MacGyver, collect if Syringe item, check proximity of guardian """
        macgyver = self.movable["M"]
        old_position = macgyver.position
        new_position = (old_position[0] + movement[0], old_position[1] + movement[1])
        if not (new_position in self.free_way):
            return DONT_MOVE, old_position, old_position  # Wall : no possible movement
        for key in self.movable:
            if self.movable[key].position == new_position:
                if isinstance(self.movable[key], Syringe):
                    if not self.movable[key].is_collect:
                        self.movable[key].collect()
        macgyver.position = new_position
        status = self.check_guardian_proximity(new_position)
        return status, old_position, new_position

    def check_guardian_proximity(self, new_position):
        guardian = self.movable["G"]
        for (x, y) in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            position_to_test = (new_position[0] + x, new_position[1] + y)
            if position_to_test == guardian.position:
                if Syringe.is_complete:
                    return FILLED_SYRINGE
                else:
                    return NO_SYRINGE
        return FREE_FLOOR
