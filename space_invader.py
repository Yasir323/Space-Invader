"""
1. Create the screen
2. Set the title
3. Set the background
4. Set the icon
5. Load the spaceship
6. Adding bullet and shooting it
7. Restricting the spaceship movement
8. Bring in the enemies
9. Make the bullet hit the enemies
10. Add sounds
11. Display score
12. Game over condition
"""
import pygame
import random
import math
import time

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
score = 0

# Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title
pygame.display.set_caption("Space Invader")

# Load the icon image
icon_img = pygame.image.load("rocket-ship.png")
# Set the icon
pygame.display.set_icon(icon_img)

# Load the background
background_img = pygame.image.load("background.png")

# Load the spaceship image
player_img = pygame.image.load("spaceship.png")
player_x = (SCREEN_WIDTH - player_img.get_width()) / 2
player_y = (SCREEN_HEIGHT - player_img.get_height() - 20)
x_limit = SCREEN_WIDTH - player_img.get_width()

# Load the bullet image
bullet_img = pygame.image.load("bullet.png")
bullet_x = (SCREEN_WIDTH - bullet_img.get_width()) / 2
bullet_y = (SCREEN_HEIGHT - bullet_img.get_height() - 35)
bullet_state = "ready"

# Add sounds
bullet_sound = pygame.mixer.Sound("laser.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Load enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6
enemy_speedx = 5
enemy_speedy = 20
for i in range(num_enemies):
    enemy_img.append(pygame.image.load("ufo(2).png"))
    enemy_x.append(random.randint(0, x_limit))
    enemy_y.append(random.randint(0, 150))
    enemy_x_change.append(enemy_speedx)
    enemy_y_change.append(enemy_speedy)


def player():
    screen.blit(player_img, (player_x, player_y))


def bullet():
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (bullet_x, bullet_y))


def enemies(i):
    screen.blit(enemy_img[i], (enemy_x[i], enemy_y[i]))


def show_score():
    font = pygame.font.SysFont("Courier", 32)
    text = font.render(f"Score: {score}", True, (90, 176, 14))
    screen.blit(text, (10, 10))


def game_over():
    font = pygame.font.SysFont("Courier", 64)
    text = font.render("GAME OVER", True, (90, 176, 14))
    screen.blit(text, ((SCREEN_WIDTH - 300) / 2, (SCREEN_HEIGHT - 50) / 2))


bullet_y_change = 2
player_x_change = 0
running = True
while running:
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound.play()
                    bullet_x = player_x + 16      
                    bullet()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    # Moving the player
    player_x = player_x + player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= x_limit:
        player_x = x_limit

    # Enemy movement
    for i in range(num_enemies):
        # Game over condition
        if math.dist([player_x, player_y], [enemy_x[i], enemy_y[i]]) < 50:
            game_over()
            show_score()
            pygame.display.update()
            time.sleep(2)
            running = False
            break
            
        enemy_x[i] += enemy_x_change[i]
        
        if enemy_x[i] >= x_limit:
            enemy_x_change[i] = -enemy_speedx
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] <= 0:
            enemy_x_change[i] = enemy_speedx
            enemy_y[i] += enemy_y_change[i]
        enemies(i)
        distance = math.dist([bullet_x, bullet_y], [enemy_x[i], enemy_y[i]])
        if distance < 30:
            explosion_sound.play()
            bullet_y = (SCREEN_HEIGHT - bullet_img.get_height() - 35)
            bullet_state = "ready"
            enemy_x[i] = random.randint(0, x_limit)
            enemy_y[i] = random.randint(0, 150)
            score += 100
    
    # Bullet movement
    if bullet_state == "fire":
        bullet_y = bullet_y - bullet_y_change
        bullet()
    if bullet_y <= 0:
        bullet_y = (SCREEN_HEIGHT - bullet_img.get_height() - 35)
        bullet_state = "ready"
    player()
    show_score()
    pygame.display.update()
pygame.quit()
