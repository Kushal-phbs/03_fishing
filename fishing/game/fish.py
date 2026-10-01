"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. The starter has one fish type; Task 2 adds more.
"""

import pygame


class Fish:
    def __init__(
        self, x, y, speed, width=36, height=18, point_value=10, color=(80, 180, 220)
    ):
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x - self.width / 2 >= screen_width:
            self.x = -self.width / 2
        elif self.speed < 0 and self.x + self.width / 2 <= 0:
            self.x = screen_width + self.width / 2

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )
