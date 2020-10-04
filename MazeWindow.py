#! /usr/bin/env python3
# coding: utf8

import pygame
from pygame.locals import *

from Constantes import *

pygame.init()


class MazeWindow:
    """ Draw what give the maze object, i.e. the kind of items and their positions"""

    def __init__(self, maze, width_picture, height_picture):
        """ Initialize the elements necessary for what will be visible and display it """
        self.width_picture = width_picture
        self.height_picture = height_picture
        self.width_window = self.width_picture * maze.size_x
        self.height_window = self.height_picture * maze.size_y

        self.maze = maze
        self.window = pygame.display.set_mode((self.width_window, self.height_window))

        self.images = {}

    def load_pictures(self, pictures_to_load):
        """ Load pictures into dictionary. Key is kind of elements and content is pygame image """
        for key in pictures_to_load:
            self.images[key] = self.load_picture(pictures_to_load[key][1], pictures_to_load[key][0])

    def load_picture(self, is_alpha, path):
        if is_alpha:  # for transparency
            return pygame.image.load(path).convert_alpha()
        return pygame.image.load(path).convert()

    def fill_with_pictures(self):
        for x in range(0, self.maze.size_x):
            for y in range(0, self.maze.size_y):
                if (x, y) not in self.maze.free_way:
                    key = "W"
                else:
                    key = self.maze.free_way[(x, y)]
                self.blit(key, x, y)

    def blit(self, key, x, y):
        self.window.blit(self.images[key], (x * self.width_picture, y * self.height_picture))

    def add_movable_pictures(self):
        for key in self.maze.movable:
            (x, y) = self.maze.movable[key].position
            self.blit(key, x, y)

    def display(self):
        pygame.display.set_icon(self.images["M"])
        pygame.display.set_caption("Maze Gyver")

        # Don't use flip(), the game must run on different OS, they don't always support hardware acceleration.
        pygame.display.update()

    def survey_events(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        loop = self.move_macgyver((0, -1))
                    if event.key == K_DOWN:
                        loop = self.move_macgyver((0, 1))
                    if event.key == K_LEFT:
                        loop = self.move_macgyver((-1, 0))
                    if event.key == K_RIGHT:
                        loop = self.move_macgyver((1, 0))

        pygame.quit()

    def move_macgyver(self, movement):
        (status, old_position, new_position) = self.maze.move_macgyver(movement)
        if status == DONT_MOVE:  # Try to move in a wall, nothing happens
            return True
        (x, y) = old_position
        key = self.maze.free_way[old_position]
        self.blit(key, x, y)
        (x, y) = new_position
        key = self.maze.free_way[new_position]
        self.blit(key, x, y)
        self.blit("M", x, y)

        pygame.display.update()

        if status == NO_SYRINGE:  # Meet guardian and haven't syringe
            self.kill()
            return False
        if status == FILLED_SYRINGE:  # Meet guardian and have syringe
            self.win()
            return False
        return True  # status == 0:   Movement on free floor

    def kill(self):
        print("kill")
        pass

    def win(self):
        print("win")
        pass
