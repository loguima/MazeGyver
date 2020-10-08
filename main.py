#! /usr/bin/env python3
# coding: utf8

from backside.maze import *
from frontside.window import *

if __name__ == "__main__":
    # Window is driven by Maze
    maze_window = Window(Maze())
    maze_window.load_pictures()
    maze_window.fill_with_pictures()
    maze_window.add_movable_pictures()
    maze_window.display()
    maze_window.survey_events()
