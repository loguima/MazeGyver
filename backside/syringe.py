#! /usr/bin/env python3
# coding: utf8

from backside.movable import Movable
from common.constantes import *


class Syringe(Movable):
    """ For collectable parts of syringe : Aether, Tube, Needle. """
    _count_collect = 0

    def __init__(self, position):
        """ Manage collect """
        super().__init__(position)
        self.is_collect = False

    def collect(self):
        """ When MacGyver walk on piece of syringe. """
        self.is_collect = True
        self._add_collect()

    @classmethod
    def _add_collect(cls):
        """ count_collect does not depend on the instance, but on the class. """
        cls._count_collect = cls._count_collect + 1

    @classmethod
    def is_complete(cls):
        """ Syringe is complete when Aether, Tube and Needle have been collect. """
        if cls._count_collect == NUMBER_TO_COLLECT:
            return True
        return False
