#! /usr/bin/env python3
# coding: utf8


class Maze:

    def __init__(self):
        """ Transforms the content of the file into a dictionary, which contains: a position as key and a type of
            elements (mobile or not). Positions do not apply to walls, it's the free way """
        with open("res/maze.txt", "r") as file:
            self.free_way = {}
            k = 0
            for line in file:
                j = 0
                for column in line:
                    if column != "W":
                        self.free_way[(j, k)] = column
                    j = j +1
                k = k+1
