import pygame
import math


class Boid:
    def __init__(self, x_pos, y_pos, speed, rotation, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.color = color
        self.rotation = rotation

        self.x_vel = self.speed * math.cos(self.rotation)
        self.y_vel = self.speed * math.sin(self.rotation)

    def draw(self, surface):

        pygame.draw.polygon(surface,
                            color=self.color,
                            points=((self.x_pos, self.y_pos),
                                    (transform(self.x_pos-10, self.y_pos-6, self.x_pos, self.y_pos, self.rotation)),
                                    (transform(self.x_pos-8, self.y_pos, self.x_pos, self. y_pos, self.rotation)),
                                    (transform(self.x_pos-10, self.y_pos+6, self.x_pos, self.y_pos, self.rotation))))

    def move(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def change_rotation(self, amount):
        self.rotation = (self.rotation + amount) % (2*math.pi)
        self.x_vel = self.speed * math.cos(self.rotation)
        self.y_vel = self.speed * math.sin(self.rotation)

    def change_speed(self, amount):
        self.speed += amount
        self.x_vel = self.speed * math.cos(self.rotation)
        self.y_vel = self.speed * math.sin(self.rotation)

    def distance_to(self, boid):
        return math.sqrt((self.x_pos - boid.x_pos)**2 + (self.y_pos-boid.y_pos)**2)

    def is_friends_with(self, boid, max_distance):
        if self.distance_to(boid) <= max_distance:
            return True
        else:
            return False


def transform(x, y, a, b, angle):
    return a + (x-a)*math.cos(angle) - (y-b)*math.sin(angle), b + (y-b)*math.cos(angle) + (x-a)*math.sin(angle)



