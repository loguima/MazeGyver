#! /usr/bin/env python3
# coding: utf8

import random

from Movable import Movable, Syringe
from Constantes import *


class Maze:
    """ Determine the content of the labyrinth, i.e. the kind of items and their positions """

    def __init__(self):
        """ The maze have two parts : irremovable (wall, floor, ...) and movable (characters, items, ...)? """

        self.free_way = {}  # Contains the free way (no walls) where movable items can evoluate.
        self.create_irremovable_part()
        self.movable = {}  # Contains the references of movable objects (object in the sense of Python).
        self.create_movable_part()
        self.authorized_places = {}  # Contains where next movable item can be place.

    def create_irremovable_part(self):
        """ Transforms the content of the file into the dictionary "free_way". """

        with open("res/maze.txt", "r") as maze_file:
            for y, line in enumerate(maze_file):
                for x, column in enumerate(line.strip()):
                    if column != WALL:
                        self.free_way[(x, y)] = column
                        if column == EXIT:
                            exit_position = (x, y)

        loop = True
        while loop:
            position = self.give_random_position(self.free_way)
            # Begin's position is random, but not at the exit position.
            # Otherwise the Guardian is on Begin and Mac on Start ==> Mac is immediately killed.
            if position != exit_position:
                loop = False
        self.free_way[position] = BEGIN

    def create_movable_part(self):
        """ Give position and create movable items """
        self.authorized_places = self.free_way.copy()  # Where a new movable item can be placed

        for position in self.free_way:
            if self.free_way[position] == EXIT:
                self.create_character(GUARDIAN, position)  # Guardian's position is same as Exit
            elif self.free_way[position] == BEGIN:
                self.create_character(MAC_GYVER, position)  # MacGyver's position is same as Begin

        self.create_syringe(NEEDLE)  # Random position for Needle, Tube, Aether
        self.create_syringe(TUBE)
        self.create_syringe(AETHER)

    def give_random_position(self, authorized_places):
        """ Give random position of free place. """
        free_place = (random.randint(0, len(authorized_places)-1))
        return list(authorized_places)[free_place]  # Position in the converted dictionary in list

    def create_character(self, kind, position):
        """ Create a movable and indicate that the place is not free for deposit other movable """
        self.movable[kind] = Movable(position)
        del self.authorized_places[position]

    def create_syringe(self, kind):
        """ Give position, create a piece of Syringe and indicate that the place is not free """
        position = self.give_random_position(self.authorized_places)
        self.movable[kind] = Syringe(position)
        del self.authorized_places[position]

    def move_macgyver(self, movement):
        """ If free position, move MacGyver, collect if Syringe item, check proximity of guardian """
        macgyver = self.movable[MAC_GYVER]
        old_position = macgyver.position
        new_position = (old_position[0] + movement[0], old_position[1] + movement[1])
        if not (new_position in self.free_way):
            return DONT_MOVE, old_position, old_position  # Wall : no possible movement
        # Can't delete movable when iter, so set a flag and treat after if needed.
        delete_movable = False
        for kind in self.movable:
            if self.movable[kind].position == new_position:
                if isinstance(self.movable[kind], Syringe):  # Piece of syringe
                    self.movable[kind].collect()
                    delete_movable = True
                    break  # Keep the good kind
        if delete_movable:
            del self.movable[kind]  # Delete syringe piece
        macgyver.position = new_position
        status = self.check_guardian_proximity(new_position)
        return status, old_position, new_position

    def check_guardian_proximity(self, new_position):
        """ Check the guardian proximity. If near, check if syringe is complete """
        guardian = self.movable[GUARDIAN]
        for (x, y) in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            position_to_test = (new_position[0] + x, new_position[1] + y)
            if position_to_test == guardian.position:
                if Syringe.is_complete():
                    return FILLED_SYRINGE
                else:
                    return NO_SYRINGE
        return FREE_FLOOR
