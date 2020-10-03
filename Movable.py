#! /usr/bin/env python3
# coding: utf8


class Movable:

    def __init__(self, kind, position):
        self.kind = kind
        self.position = position

class Collectable(Movable):

    count_collect = 0

    def collect(self):
        self.count_collect = self.count_collect + 1

    @property
    def is_complete(self):
        if self.count_collect == 3:
            return True
        return False

class Character(Movable):

    def change_position(self, position):
        self.position = position
