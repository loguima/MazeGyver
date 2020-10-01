#! /usr/bin/env python3
# coding: utf8

from Maze import *

from MazeWindow import *


if __name__ == "__main__":

    maze_window = MazeWindow(Maze())
    maze_window.survey_events()