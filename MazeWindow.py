#! /usr/bin/env python3
# coding: utf8

import pygame
from pygame.locals import *

from Constantes import *

pygame.init()


class MazeWindow:
    """ Draw what give the maze object, i.e. the kind of items and their positions"""

    def __init__(self, maze, width_picture, height_picture):
        """ Initialize the elements necessary for what will be visible. """
        self.width_picture = width_picture
        self.height_picture = height_picture
        self.width_window = self.width_picture * maze.size_x
        self.height_window = self.height_picture * maze.size_y

        self.maze = maze
        self.window = pygame.display.set_mode((self.width_window, self.height_window))

        self.images = {}

    def load_pictures(self, pictures_to_load):
        """ Load pictures into dictionary. Key is kind of elements and content is pygame image """
        for kind in pictures_to_load:
            self.images[kind] = self.load_picture(pictures_to_load[kind][1], pictures_to_load[kind][0])

    def load_picture(self, is_alpha, path):
        """ Load one picture """
        if is_alpha:  # for transparency
            return pygame.image.load(path).convert_alpha()
        return pygame.image.load(path).convert()

    def fill_with_pictures(self):
        """ Fill with the pictures of irremovable part (wall, floor, exit, begin)"""
        for position in [(x, y) for x in range(self.maze.size_x) for y in range(self.maze.size_y)]:
            if position not in self.maze.free_way:
                kind = "W"
            else:
                kind = self.maze.free_way[position]
            self.blit(kind, position)

    def blit(self, kind, position):
        """ Blit : copy pixels of image (a surface) onto the window (another surface), at the given position. """
        (x, y) = position
        self.window.blit(self.images[kind], (x * self.width_picture, y * self.height_picture))

    def add_movable_pictures(self):
        """ Draw the pictures of the mobile elements (MacGyver, Guardian, syringe's parts. """
        for kind in self.maze.movable:
            position = self.maze.movable[kind].position
            self.blit(kind, position)

    def display(self):
        """ Display the pygame window """
        pygame.display.set_icon(self.images["M"])
        pygame.display.set_caption("Maze Gyver")

        # Don't use flip(), the game must run on different OS, they don't always support hardware acceleration.
        pygame.display.update()

    def survey_events(self):
        """ Monitors keyboard events. If arrows, start MacGyver's move """
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
        """ Draw MacGyver's movement and possibly follow on victory or defeat"""
        (status, old_position, new_position) = self.maze.move_macgyver(movement)
        if status == DONT_MOVE:  # Try to move in a wall, nothing happens
            return True

        kind = self.maze.free_way[old_position]
        self.blit(kind, old_position)  # Restore the soil at the old MacGyver's position

        kind = self.maze.free_way[new_position]
        self.blit(kind, new_position)  # Restore the soil if position was occupied by piece of syringe
        self.blit("M", new_position)  # Place MacGyver

        pygame.display.update()

        if status == NO_SYRINGE:  # Meet guardian and haven't syringe
            kind = self.maze.free_way[new_position]
            self.blit(kind, new_position)  # Made MacGyver vanish in the air
            self.kill()
            return False
        if status == FILLED_SYRINGE:  # Meet guardian and have syringe
            guardian_position = self.maze.movable["G"].position
            kind = self.maze.free_way[guardian_position]
            self.blit(kind, guardian_position)  # Made Guardian go to rest
            self.win()
            return False
        return True  # status == 0: Movement on free floor

    def kill(self):
        """ In case of defeat. """
        sentence = """Incroyable,\nte faire battre !\nLe monde\nest foutu."""
        self.display_text(sentence)

    def win(self):
        """ In case of victory """
        sentence = """Merci d'avoir joué\nau plus extraordinaire\njeu de l'histoire\ndu monde,\nde l'univers même !"""

        self.display_text(sentence)

    def display_text(self, sentence):
        """ Display a text at the center of the window """
        police = pygame.font.Font("res/SF Slapstick Comic Shaded.ttf", 42)
        text_count = len(sentence.splitlines())
        for x, text in enumerate(sentence.splitlines()):
            text = police.render(text, 1, (50, 50, 50))
            text_height = text.get_height() + 10
            position = text.get_rect()
            position.centerx = self.window.get_rect().centerx
            position.centery = self.window.get_rect().centery + (x * text_height) - ((text_count - 1) * text_height) / 2
            self.window.blit(text, position)
        pygame.display.update()
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
