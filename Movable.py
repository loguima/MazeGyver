#! /usr/bin/env python3
# coding: utf8


class Movable:
    """ To create movable item """

    def __init__(self, kind, position):
        self.kind = kind
        self.position = position
        self.is_collect = False


class Syringe(Movable):
    """ For collectable parts of syringe : Aether, Tube, Needle """

    count_collect = 0

    def collect(self):
        self.is_collect = True
        self.add_collect()

    @classmethod
    def add_collect(cls):
        cls.count_collect = cls.count_collect + 1

    @property
    def is_complete(self):
        if self.count_collect == 3:
            return True
        return False


class Character(Movable):
    """ For character : MacGyver and Guardian (not realy usefull, just for fun) """
    pass
