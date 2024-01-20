import pygame
import random
import math

pygame.init()

pop_sound = pygame.mixer.Sound("sounds/pop.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")

icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Whack-a-Mole")
bg = pygame.image.load("images/background.jpg")

clock = pygame.time.Clock()
moles = [pygame.image.load("images/mole1.png"), pygame.image.load("images/mole2.png"), pygame.image.load("images/mole3.png"), pygame.image.load("images/mole4.png")]
hole_image = pygame.image.load("images/hole.png")

run_time = pygame.time.get_ticks()

points = 0
lives = 3

with open("highscore.txt", "r") as file:
    high_score = file.read()

font = pygame.font.SysFont(None, 36)
hit_font = pygame.font.Font("fonts/Roboto-Black.ttf", 144)

miss_bg = False
hit_state = False

circles = []

def generate_rect():
    jeda_1 = 200
    jeda_2 = 200
    for i in range(1, 7):
        if i > 3:
            new_pos = (((screen.get_width() / 2) - 400) + jeda_1, (screen.get_height() / 2) + 200)
            jeda_1 += 200
        else:
            new_pos = (((screen.get_width() / 2) - 400) + jeda_2, screen.get_height() / 2)
            jeda_2 += 200
        circles.append(new_pos)

generate_rect()

def move_mole():
    global rand_pos
    global run_time
    rand_pos = random.choice(circles)
    pop_sound.play()
    run_time = pygame.time.get_ticks()

rand_pos = random.choice(circles)

running = True

while running:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  
            if math.dist(mouse_pos, rand_pos) <= 60:
                hit_state = True
                run_time_hit = pygame.time.get_ticks()
                points += 1
                move_mole()
            else:
                miss_bg = True
                run_time_miss = pygame.time.get_ticks()
                miss_sound.play()
                lives -= 1

    if miss_bg:
        current_time_miss = pygame.time.get_ticks()
        if current_time_miss - run_time_miss <= 250:
            screen.fill((255, 0, 0))
        else:
            screen.blit(bg, (0, 0))
            miss_bg = False

    for i in circles:
        # pygame.draw.circle(screen, "red", i, 5)
        screen.blit(hole_image, (i[0]-60, i[1]+20))

    points_text = font.render("Points: " + str(points), True, (0, 0, 0))
    lives_text = font.render("Lives: " + str(lives), True, (0, 0, 0))

    screen.blit(points_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - run_time
    if elapsed_time >= 1500:
        move_mole()
    
    if elapsed_time <= 300:
        screen.blit(moles[int(elapsed_time // 100)], (rand_pos[0]-60, rand_pos[1]-60))
    else:
        screen.blit(moles[3], (rand_pos[0]-60, rand_pos[1]-60))

    if hit_state:
        current_time_hit = pygame.time.get_ticks()
        if current_time_hit - run_time_hit <= 250:
            hit_text = hit_font.render("+1", True, (0, 255, 0))
            screen.blit(hit_text, (mouse_pos[0] - hit_text.get_width() // 2, mouse_pos[1] - hit_text.get_height() // 2))
        else:
            hit_state = False

    if lives <= 0:
        if points <= int(high_score):
            screen.fill((255, 0, 0))
            screen.blit(points_text, (10, 10))
            screen.blit(lives_text, (10, 50))
            game_over_font = pygame.font.Font("fonts/Impact.ttf", 256)
            game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        elif points > int(high_score):
            high_score = points
            with open("highscore.txt", 'w') as file:
                file.write(str(points))
            screen.blit(bg, (0, 0))
            game_over_font = pygame.font.Font("fonts/Roboto-Black.ttf", 256)
            game_over_text = game_over_font.render("New best!", True, (255, 255, 255))

        pb_text = hit_font.render(str(high_score), True, (255, 255, 255))
        screen.blit(game_over_text, ((screen.get_width() - game_over_text.get_width()) // 2, (screen.get_height() - game_over_text.get_height()) // 2))
        screen.blit(pb_text, ((screen.get_width() - pb_text.get_width()) // 2, (screen.get_height() - pb_text.get_height() + 350) // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()

    pygame.display.flip()
    clock.tick(60)