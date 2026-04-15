import pygame
import datetime
import os

pygame.init()
screen = pygame.display.set_mode((1200, 700))
WHITE = (255, 255, 255)

base = r'C:\Users\User\Desktop\tasks\prac9\mickeys_clock\images'

image_surface = pygame.image.load(os.path.join(base, 'clock.png')).convert_alpha()
mickey = pygame.image.load(os.path.join(base, 'mUmrP.png')).convert_alpha()
hand_l = pygame.image.load(os.path.join(base, 'hand_left.png')).convert_alpha() 
hand_r = pygame.image.load(os.path.join(base, 'hand_right.png')).convert_alpha() 

resized_image = pygame.transform.scale(image_surface, (800, 600))
res_mickey = pygame.transform.scale(mickey, (350, 350))
hand_l_base = pygame.transform.scale(hand_l, (200, 200))
hand_r_base = pygame.transform.scale(hand_r, (200, 200))

CLOCK_CENTER = (600, 340)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    now = datetime.datetime.now()
    m = now.minute
    s = now.second

    minutes_angle = -(m * 6 + s * 0.1) 
    seconds_angle = -(s * 6)

    rotated_minutes = pygame.transform.rotate(hand_r_base, minutes_angle)
    rotated_seconds = pygame.transform.rotate(hand_l_base, seconds_angle)

    minutes_rect = rotated_minutes.get_rect(center=CLOCK_CENTER)
    seconds_rect = rotated_seconds.get_rect(center=CLOCK_CENTER)

    screen.fill(WHITE)

    image_rect = resized_image.get_rect(center=CLOCK_CENTER)
    screen.blit(resized_image, image_rect)

    mic_rect = res_mickey.get_rect(center=CLOCK_CENTER)
    screen.blit(res_mickey, mic_rect)

    screen.blit(rotated_minutes, minutes_rect) 
    screen.blit(rotated_seconds, seconds_rect)  

    pygame.display.flip()
    clock.tick(60)

pygame.quit()