#! /usr/bin/env python3
# coding: utf8

import pygame

pygame.init()


class MazeWindow:

    def __init__(self, maze):
        """ Initializes the elements necessary for what will be visible on the screen and display it """

        self.maze = maze
        self.window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Maze Gyver")
        background = pygame.Surface(self.window.get_size())
        background.fill((0, 200, 255))
        self.window.blit(background, (0, 0))
        self.load_pictures()
        self.fill_with_pictures()
        pygame.display.update()

    def load_pictures(self):
        """ Load pictures into dictionary. Key is kind of elements and content is pygame image """
        self.img1 =pygame.image.load("res/img/Wall.png").convert_alpha()

    def fill_with_pictures(self):
        for j in range(0, 14):
            for k in range(0, 14):
                if (j, k) not in self.maze.free_way:
                    self.window.blit(self.img1, (j*40, k*40))

    def survey_events(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
