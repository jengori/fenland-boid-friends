import math
import pygame
import random
from boid import Boid

# Game title and window dimensions
WINDOW_TITLE = "BOIDS"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 593

# Shades of black for boids
BOID_SHADES = [(52, 52, 52), (27, 18, 18), (0, 0, 0), (40, 40, 43), (48, 25, 52)]

# Background image
BG_IMAGE = pygame.image.load("fens.jpg")

# Game setup - These variables can be changed for different game results
UPDATES_PER_SECOND = 70
NUM_STARTING_BOIDS = 100
FRIEND_ZONE = 30
PERSONAL_SPACE = 10
FRIEND_LINES_ENABLED = False
SPEED_ALIGNMENT = 0.05
DIRECTION_ALIGNMENT = 0.05
WIGGLE = 0.1
MIN_SPEED = 1
MAX_SPEED = 5

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BOIDS")

continue_game = True
clock = pygame.time.Clock()

# create starting array of boids
boids = []
for _ in range(NUM_STARTING_BOIDS):
    boid = Boid(random.randint(0, 1000), random.randint(400, 593), random.randint(MIN_SPEED, MAX_SPEED), random.random()*2*math.pi, random.choice(BOID_SHADES))
    boids.append(boid)

while continue_game:

    for event in pygame.event.get():
        # if player quits, end game
        if event.type == pygame.QUIT:
            continue_game = False

        # if mouse is clicked, add a new boid in the location clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_boid_pos = pygame.mouse.get_pos()
            new_boid = Boid(new_boid_pos[0], new_boid_pos[1], random.randint(MIN_SPEED, MAX_SPEED), random.random()*2*math.pi, random.choice(BOID_SHADES))
            boids.append(new_boid)

        # if a key is pressed, scatter the boids
        if event.type == pygame.KEYDOWN:
            print("a key is pressed")
            for boid in boids:
                boid.change_rotation(random.random()*random.choice([-1, 1])* math.pi)
                boid.change_speed(1)

    # draw background image
    window.blit(BG_IMAGE, (0, 0))
    # for each boid
    for i in range(len(boids)):

        # set friend variables to 0
        num_friends = 0
        sum_speed_of_friends = 0
        sum_rotation_of_friends = 0

        sum_friends_x_pos = 0
        sum_friends_y_pos = 0

        # draw all boids
        boids[i].draw(window)
        # move all boids
        boids[i].move()

        for j in range(len(boids)):
            # if another boid is a friend of this boid
            if boids[i].is_friends_with(boids[j], FRIEND_ZONE) and i != j:
                # update friend variables
                num_friends += 1
                sum_rotation_of_friends += boids[j].rotation
                sum_speed_of_friends += boids[j].speed
                sum_friends_x_pos += boids[j].x_pos
                sum_friends_y_pos += boids[j].y_pos
                # change color of friend to color of this boid
                boids[j].color = boids[i].color

                # adjust position for separation (boid tries to stay SEPARATION pixels away from other boids)
                if boids[i].is_friends_with(boids[j], PERSONAL_SPACE):
                    if abs(boids[i].x_pos - boids[j].x_pos) < PERSONAL_SPACE:
                        if boids[i].x_pos < boids[j].x_pos:
                            boids[i].x_pos -= 1
                        else:
                            boids[i].x_pos += 1

                    if abs(boids[i].y_pos - boids[j].y_pos) < PERSONAL_SPACE:
                        if boids[i].y_pos < boids[j].y_pos:
                            boids[i].y_pos -= 1
                        else:
                            boids[i].y_pos += 1
                # draw lines between friends if friend lines enabled
                if FRIEND_LINES_ENABLED:
                    pygame.draw.line(window, color="White", start_pos=(boids[i].x_pos, boids[i].y_pos), end_pos=(boids[j].x_pos, boids[j].y_pos))
        # if this boid has any friends:
        if num_friends > 0:
            # find average rotation, speed and position of friends
            avg_rotation_of_friends = sum_rotation_of_friends / num_friends
            avg_speed_of_friends = sum_rotation_of_friends / num_friends
            avg_x_pos_of_friends = sum_friends_x_pos / num_friends
            avg_y_pos_of_friends = sum_friends_y_pos / num_friends

            # adjust speed to align with friends
            speed_diff = abs(avg_speed_of_friends - boids[i].speed)

            if boids[i].speed < avg_speed_of_friends:
                if speed_diff < SPEED_ALIGNMENT:
                    boids[i].speed = avg_speed_of_friends
                else:
                    boids[i].speed += SPEED_ALIGNMENT

            elif boids[i].speed > avg_speed_of_friends:
                if speed_diff < SPEED_ALIGNMENT:
                    boids[i].speed = avg_speed_of_friends
                else:
                    boids[i].speed -= SPEED_ALIGNMENT

            # adjust rotation to align with friends
            rotation_diff = abs(avg_rotation_of_friends - boids[i].rotation)

            if boids[i].rotation < avg_rotation_of_friends and rotation_diff <= math.pi:
                if rotation_diff < DIRECTION_ALIGNMENT:
                    boids[i].change_rotation(rotation_diff)
                else:
                    boids[i].change_rotation(DIRECTION_ALIGNMENT)

            elif boids[i].rotation < avg_rotation_of_friends and rotation_diff > math.pi:
                if math.pi - rotation_diff < DIRECTION_ALIGNMENT:
                    boids[i].change_rotation(rotation_diff - math.pi)
                else:
                    boids[i].change_rotation(-DIRECTION_ALIGNMENT)

            elif boids[i].rotation > avg_rotation_of_friends and rotation_diff <= math.pi:
                if rotation_diff < DIRECTION_ALIGNMENT:
                    boids[i].change_rotation(-rotation_diff)
                else:
                    boids[i].change_rotation(-DIRECTION_ALIGNMENT)

            elif boids[i].rotation > avg_rotation_of_friends and rotation_diff > math.pi:
                if math.pi - rotation_diff < DIRECTION_ALIGNMENT:
                    boids[i].change_rotation(math.pi - rotation_diff)
                else:
                    boids[i].change_rotation(DIRECTION_ALIGNMENT)

            # enforce speed limits
            if boids[i].speed < MIN_SPEED:
                boids[i].change_speed(MIN_SPEED - boids[i].speed)

            if boids[i].speed > MAX_SPEED:
                boids[i].change_speed(-(boids[i].speed-MAX_SPEED))

        # wrap around
        if boids[i].x_pos > WINDOW_WIDTH:
            boids[i].x_pos = 0

        if boids[i].x_pos < 0:
            boids[i].x_pos = WINDOW_WIDTH

        # avoid top and bottom
        if boids[i].y_pos <= 75:
            if math.pi * (3/2) < boids[i].rotation < math.pi * 2:
                boids[i].change_rotation(0.05)
            elif math.pi < boids[i].rotation <= math.pi * (3/2):
                boids[i].change_rotation(-0.05)

        if boids[i].y_pos >= WINDOW_HEIGHT - 250:
            if 0 < boids[i].rotation < math.pi/2:
                boids[i].change_rotation(-0.05)
            elif math.pi/2 < boids[i].rotation <= math.pi:
                boids[i].change_rotation(0.05)

        # apply wiggle factor
        boids[i].change_rotation(random.random()*random.choice([-WIGGLE, WIGGLE]))

    pygame.display.flip()

    clock.tick(UPDATES_PER_SECOND)

pygame.quit()
