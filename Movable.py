#! /usr/bin/env python3
# coding: utf8


class Movable:
    """ Create movable item """

    def __init__(self, kind, position):
        """ Principaly to manage position """
        self.kind = kind
        self.position = position
        self.is_collect = False


class Syringe(Movable):
    """ For collectable parts of syringe : Aether, Tube, Needle. """

    count_collect = 0

    def collect(self):
        """ When MacGyver walk on piece of syringe. """
        self.is_collect = True
        self.add_collect()

    @classmethod
    def add_collect(cls):
        """ count_collect does not depend on the instance, but on the class. """
        cls.count_collect = cls.count_collect + 1

    @classmethod
    def is_complete(cls):
        """ Syringe is complete when Aether, Tube and Needle have been collect. """
        if cls.count_collect == 3:
            return True
        return False
