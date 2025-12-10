import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Busje')
clock = pygame.time.Clock()

busje = pygame.image.load("../busje/busjerood.png")
pygame.display.set_icon(busje)
busje = pygame.transform.scale(busje, (140, 90))
pylon = pygame.image.load("pylon.png")
pylon = pygame.transform.scale(pylon, (130, 130))
bg = pygame.image.load("../busje/wegen.png").convert()
bg_width = bg.get_width()
tiles = math.ceil(WIDTH / bg_width) + 1
scroll = 0

LANE_RANGES = [(120, 190), (296, 369), (468, 541)]
bus_h = busje.get_height()
pylon_h = pylon.get_height()

lane_centers = [ (a + b) / 2 for (a, b) in LANE_RANGES ]
Y_positions = []
for c in lane_centers:
    top = int(c - bus_h / 2)
    top = max(0, min(top, HEIGHT - bus_h))
    Y_positions.append(top)

current_lane = 1
Y = Y_positions[current_lane]
X = 100

pylons = []  
spawn_timer = 0.0
score = 0.0
score_font = pygame.font.SysFont("bahnschrift", 40)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and current_lane < len(Y_positions) - 1:
                current_lane += 1
                Y = Y_positions[current_lane]
            elif event.key == pygame.K_UP and current_lane > 0:
                current_lane -= 1
                Y = Y_positions[current_lane]

    scroll -= 10
    if abs(scroll) > bg_width:
        scroll = 0
    for i in range(tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    score += 0.1
    score_text = score_font.render(f"Score: {math.ceil(score)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    spawn_timer -= 1 / 30
    if spawn_timer <= 0:
        lane_idx = random.randrange(len(lane_centers))
        center = lane_centers[lane_idx]
        pylon_top = int(center - pylon_h / 2)
        pylons.append([WIDTH + 50, pylon_top])
        spawn_timer = 1.0

    

    for p in pylons:
        p[0] -= 10
        screen.blit(pylon, (p[0], p[1]))

        HB_W, HB_H = 60, 90
        hb_x = p[0] + (pylon_h - HB_W) // 2 
        hb_x = p[0] + (pylon.get_width() - HB_W)//2
        hb_y = p[1] + (pylon.get_height() - HB_H)//2
        pylon_hitbox = pygame.Rect(hb_x, hb_y, HB_W, HB_H)
        
        bus_rect = busje.get_rect(topleft=(X, Y))
        screen.blit(busje, (X, Y))

        if bus_rect.colliderect(pylon_hitbox):
            print(f"Game Over! Your score was: {math.ceil(score)}")
            running = False

    pylons = [p for p in pylons if p[0] > -pylon.get_width()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

