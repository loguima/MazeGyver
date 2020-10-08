#! /usr/bin/env python3
# coding: utf8

import pygame
from pygame.locals import *

from Constantes import *

pygame.init()


class MazeWindow:
    """ Draw what give the maze object, i.e. the kind of items and their positions"""

    def __init__(self, maze):
        """ Initialize the elements necessary for what will be visible. """
        self.maze = maze

        self.window_width = PIC_WIDTH * MAZE_WIDTH
        self.window_height = PIC_HEIGHT * MAZE_HEIGHT
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.images = {}

    def load_pictures(self):
        """ Load pictures into dictionary. Key is kind of elements and content is pygame image """
        # key = kind of items / path / True if transparency image
        pictures_to_load = {
            AETHER: ("img/Aether.png", True), BEGIN: ("img/Begin.png", True), EXIT: ("img/Exit.png", True),
            FLOOR: ("img/Floor.png", False), GUARDIAN: ("img/Guardian.png", True),
            MAC_GYVER: ("img/MacGyver.png", True),
            NEEDLE: ("img/Needle.png", True), TUBE: ("img/Tube.png", True), WALL: ("img/Wall.png", False)
        }
        for kind in pictures_to_load:
            self.images[kind] = self.load_picture(pictures_to_load[kind][1], pictures_to_load[kind][0])

    def load_picture(self, is_alpha, path):
        """ Load one picture """
        if is_alpha:  # for transparency
            return pygame.image.load(path).convert_alpha()
        return pygame.image.load(path).convert()

    def fill_with_pictures(self):
        """ Fill with the pictures of irremovable part (wall, floor, exit, begin)"""
        for position in [(x, y) for x in range(MAZE_WIDTH) for y in range(MAZE_HEIGHT)]:
            if position not in self.maze.free_way:
                kind = WALL
            else:
                kind = self.maze.free_way[position]
            self.blit(kind, position)

    def blit(self, kind, position):
        """ Blit : copy pixels of image (a surface) onto the window (another surface), at the given position. """
        (x, y) = position
        self.window.blit(self.images[kind], (x * PIC_WIDTH, y * PIC_HEIGHT))

    def add_movable_pictures(self):
        """ Draw the pictures of the mobile elements (MacGyver, Guardian, syringe's parts. """
        for kind in self.maze.movable:
            position = self.maze.movable[kind].position
            self.blit(kind, position)

    def display(self):
        """ Display the pygame window """
        pygame.display.set_icon(self.images[MAC_GYVER])
        pygame.display.set_caption("Maze Gyver")

        # Don't use flip(), the game must run on different OS, they don't always support hardware acceleration.
        pygame.display.update()

    def survey_events(self):
        """ Monitors keyboard events. If arrows, start MacGyver's move """
        # Use the arrows to move
        movement = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == KEYDOWN:
                    if event.key in movement:
                        loop = self.move_macgyver(movement[event.key])

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
        self.blit(MAC_GYVER, new_position)  # Place MacGyver

        pygame.display.update()

        if status == NO_SYRINGE:  # Meet guardian and haven't syringe
            kind = self.maze.free_way[new_position]
            self.blit(kind, new_position)  # Made MacGyver vanish in the air
            self.kill()
            return False
        if status == FILLED_SYRINGE:  # Meet guardian and have syringe
            guardian_position = self.maze.movable[GUARDIAN].position
            kind = self.maze.free_way[guardian_position]
            self.blit(kind, guardian_position)  # Made Guardian go to rest
            self.win()
            return False
        return True  # status == FREE_FLOOR

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
        while loop:  # The displayed text must have time to be seen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
