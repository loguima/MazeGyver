#! /usr/bin/env python3
# coding: utf8

import pygame

pygame.init()


class MazeWindow:

    def __init__(self, maze, size_x_picture, size_y_picture):
        """ Initialize the elements necessary for what will be visible and display it """
        self.size_x_picture = size_x_picture
        self.size_y_picture = size_y_picture
        self.size_x_window = self.size_x_picture * maze.size_x
        self.size_y_window = self.size_y_picture * maze.size_y

        self.maze = maze
        self.window = pygame.display.set_mode((self.size_x_window, self.size_y_window))
        pygame.display.set_caption("Maze Gyver")
        background = pygame.Surface(self.window.get_size())
        background.fill((0, 200, 255))
        self.window.blit(background, (0, 0))

        self.images = {}

    def load_pictures(self, pictures_to_load):
        """ Load pictures into dictionary. Key is kind of elements and content is pygame image """
        for key in pictures_to_load:
            self.images[key] =self.load_picture(pictures_to_load[key][1], pictures_to_load[key][0])

    def load_picture(self, is_alpha, path):
        if is_alpha:  # for png transparency
            return pygame.image.load(path).convert_alpha()
        return pygame.image.load(path).convert()

    def fill_with_pictures(self):
        for x in range(0, self.maze.size_x):
            for y in range(0, self.maze.size_y):
                if (x, y) not in self.maze.free_way:
                    key = "W"
                else:
                     key = self.maze.free_way[(x, y)]
                self.window.blit(self.images[key], (x * self.size_x_picture, y * self.size_y_picture))

    def add_movable_pictures(self):
        for key in self.maze.movable:
            pass

    def survey_events(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

    def display(self):
        pygame.display.update()
