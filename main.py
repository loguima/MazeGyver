#! /usr/bin/env python3
# coding: utf8

from Maze import *
from MazeWindow import *

if __name__ == "__main__":
    maze_window = MazeWindow(MazeDriver(15, 15), 40, 40)
    # key = kind of items / path / True if transparency image
    pictures_to_load = {"A": ("img/Aether.png", True), "B": ("img/Begin.png", True), "E": ("img/Exit.png", True),
                        "G": ("img/Guardian.png", True),"M": ("img/MacGyver.png", True),"N": ("img/Needle.png", True),
                        "T": ("img/Tube.png", True), "W": ("img/Wall.png", False), ".": ("img/Floor.png", True)}
    maze_window.load_pictures(pictures_to_load)
    maze_window.fill_with_pictures()
    maze_window.add_movable_pictures()
    maze_window.display()
    maze_window.survey_events()
