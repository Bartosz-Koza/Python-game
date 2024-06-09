import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE WARS")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0, 1)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

SHIP_WIDTH, SHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
UPGRADE_WIDTH, UPGRADE_HEIGHT = 30, 30
PLAYER1_SHIP_IMAGE = pygame.image.load("./assets/Player1_ship.png")
PLAYER1_SHIP = pygame.transform.rotate(pygame.transform.scale(PLAYER1_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 180)
PLAYER2_SHIP_IMAGE = pygame.image.load("./assets/Player1_ship.png")
PLAYER2_SHIP = pygame.transform.rotate(pygame.transform.scale(PLAYER2_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 180)
ASTEROID_IMAGE = pygame.image.load("./assets/asteroid.png")
ASTEROID = pygame.transform.scale(ASTEROID_IMAGE, (ASTEROID_WIDTH, ASTEROID_HEIGHT))
UPGRADE_IMAGE = pygame.image.load("./assets/upgrade.png")
BACKGROUND_IMAGE =  pygame.transform.scale(pygame.image.load("./assets/menu_bg.jpg"), (WIDTH, HEIGHT))
UPGRADE = pygame.transform.scale(UPGRADE_IMAGE, (UPGRADE_WIDTH, UPGRADE_HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load("./assets/background.jpg"), (WIDTH, HEIGHT))

FIRE_SOUND = pygame.mixer.Sound("./assets/fire.mp3")
HIT_SOUND = pygame.mixer.Sound("./assets/hit.mp3")
UPGRADE_SOUND = pygame.mixer.Sound("./assets/upgrade.mp3")

FPS = 60

PLAYER_VEL = 5
PROJECTILE_VEL = 7
ASTEROID_VEL = 3
MAX_HEALTH = 3

FONT = pygame.font.SysFont('sans', 40)
MENU_FONT = pygame.font.SysFont('sans', 100)

class Ship:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.health = MAX_HEALTH
        self.projectiles = []
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for projectile in self.projectiles:
            projectile.draw(window)
        self.draw_health(window)

    def draw_health(self, window):
        health_text = FONT.render(f"Zdrowie: {self.health}", 1, WHITE)
        if self.image == PLAYER1_SHIP:
            window.blit(health_text, (10, 10))
        else:
            window.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))

    def move_projectiles(self, vel, objs):
        for projectile in self.projectiles:
            projectile.move(vel)
            if projectile.off_screen():
                self.projectiles.remove(projectile)
            else:
                for obj in objs:
                    if projectile.collide(obj):
                        objs.remove(obj)
                        self.projectiles.remove(projectile)
                        obj.health -= 1
                        HIT_SOUND.play()

    def shoot(self, key):
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            projectile = Projectile(self.x + SHIP_WIDTH // 2 - 5, self.y, RED if key == pygame.K_SPACE else GREEN)
            self.projectiles.append(projectile)
            FIRE_SOUND.play()

class Projectile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 10
        self.height = 20

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return not (0 <= self.y <= HEIGHT)

    def collide(self, obj):
        return collide(self, obj)

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = ASTEROID
        self.width = ASTEROID_WIDTH
        self.height = ASTEROID_HEIGHT

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return self.y > HEIGHT

    def collide(self, obj):
        return collide(self, obj)

class Upgrade:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = UPGRADE
        self.width = UPGRADE_WIDTH
        self.height = UPGRADE_HEIGHT

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return self.y > HEIGHT

    def collide(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    return obj1.x < obj2.x + obj2.width and obj1.x + obj1.width > obj2.x and obj1.y < obj2.y + obj2.height and obj1.y + obj1.height > obj2.y

def draw_window(player1, player2, asteroids, upgrades):
    WIN.blit(BACKGROUND, (0, 0))
    player1.draw(WIN)
    player2.draw(WIN)
    for asteroid in asteroids:
        asteroid.draw(WIN)
    for upgrade in upgrades:
        upgrade.draw(WIN)
    pygame.display.update()

def handle_movement(keys, player1, player2, in_menu):
    if keys[pygame.K_a] and player1.x - PLAYER_VEL > 0:  
        player1.x -= PLAYER_VEL
    if keys[pygame.K_d] and player1.x + PLAYER_VEL + SHIP_WIDTH < WIDTH:  
        player1.x += PLAYER_VEL
    if keys[pygame.K_w] and player1.y - PLAYER_VEL > 0:  
        player1.y -= PLAYER_VEL
    if keys[pygame.K_s] and player1.y + PLAYER_VEL + SHIP_HEIGHT < HEIGHT:  
        player1.y += PLAYER_VEL

    if keys[pygame.K_LEFT] and player2.x - PLAYER_VEL > 0:  
        player2.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player2.x + PLAYER_VEL + SHIP_WIDTH < WIDTH:  
        player2.x += PLAYER_VEL
    if keys[pygame.K_UP] and player2.y - PLAYER_VEL > 0:
        player2.y -= PLAYER_VEL
    if keys[pygame.K_DOWN] and player2.y + PLAYER_VEL + SHIP_HEIGHT < HEIGHT:
        player2.y += PLAYER_VEL

    if keys[pygame.K_ESCAPE]:
        return True
    return False

class Button:
    def __init__(self, x, y, width, height, text, text_color, color, hover_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.clicked = False

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        else:
            gradient = pygame.Surface((self.rect.width, self.rect.height))
            pygame.draw.rect(gradient, self.color, (0, 0, self.rect.width, self.rect.height))
            window.blit(gradient, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_menu(start_button, instructions_button, quit_button):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    draw_text_centered("SPACE WARS", MENU_FONT, WHITE, -200)
    start_button.draw(WIN)
    instructions_button.draw(WIN)
    quit_button.draw(WIN)
    pygame.display.update()

def draw_instructions(back_button):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    draw_text_centered("Instrukcje", MENU_FONT, WHITE, -200)
    instructions = [
        "Gracz 1:",
        "Poruszanie: W/A/S/D",
        "Strzelanie: Spacja",
        "",
        "Gracz 2:",
        "Poruszanie: Strzałki",
        "Strzelanie: Enter",
        "",
        "Zasady:",
        "Unikaj asteroidów i zbieraj ulepszenia dla korzyści.",
        "Pierwszy, kto straci wszystkie punkty zdrowia, przegrywa grę."
    ]
    for i, line in enumerate(instructions):
        draw_text_centered(line, FONT, WHITE, -100 + i * 40)
    back_button.draw(WIN)
    pygame.display.update()

def draw_text_centered(text, font, color, y_offset):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    WIN.blit(text_surface, text_rect)

def draw_win_screen(winner):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    draw_text_centered(f"{winner} Wygrywa!", MENU_FONT, WHITE, -50)
    draw_text_centered("Naciśnij ESC, aby wrócić do menu głównego", FONT, WHITE, 50)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    def reset_game():
        return Ship(100, HEIGHT // 2, PLAYER1_SHIP), Ship(WIDTH - 100 - SHIP_WIDTH, HEIGHT // 2, PLAYER2_SHIP), [], []

    player1, player2, asteroids, upgrades = reset_game()

    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Start Gry", WHITE, DARK_GREEN, GREEN, FONT)
    instructions_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Instrukcje", WHITE, DARK_GREEN, GREEN, FONT)
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, "Wyjście", WHITE, DARK_GREEN, GREEN, FONT)
    back_button = Button(WIDTH // 2 - 100, HEIGHT - 70, 200, 50, "Wstecz", WHITE, DARK_GREEN, GREEN, FONT)

    asteroid_spawn_time = random.randint(1000, 3000)
    pygame.time.set_timer(pygame.USEREVENT, asteroid_spawn_time)

    upgrade_spawn_time = random.randint(5000, 10000)
    pygame.time.set_timer(pygame.USEREVENT + 1, upgrade_spawn_time)

    in_menu = True
    in_instructions = False
    in_win_screen = False
    winner = ""

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if in_menu:
                if start_button.is_clicked(event):
                    in_menu = False
                elif instructions_button.is_clicked(event):
                    in_menu = False
                    in_instructions = True
                elif quit_button.is_clicked(event):
                    run = False
                    pygame.quit()
                    return
            elif in_instructions:
                if back_button.is_clicked(event):
                    in_instructions = False
                    in_menu = True
            elif in_win_screen:
                if keys[pygame.K_ESCAPE]: 
                    player1, player2, asteroids, upgrades = reset_game()
                    in_win_screen = False
                    in_menu = True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player1.shoot(event.key)
                    if event.key == pygame.K_RETURN:
                        player2.shoot(event.key)
                if event.type == pygame.USEREVENT:
                    x = random.randint(0, WIDTH - ASTEROID_WIDTH)
                    asteroid = Asteroid(x, 0)
                    asteroids.append(asteroid)
                    asteroid_spawn_time = random.randint(1000, 3000)
                    pygame.time.set_timer(pygame.USEREVENT, asteroid_spawn_time)
                if event.type == pygame.USEREVENT + 1:
                    x = random.randint(0, WIDTH - UPGRADE_WIDTH)
                    upgrade = Upgrade(x, 0)
                    upgrades.append(upgrade)
                    upgrade_spawn_time = random.randint(5000, 10000)
                    pygame.time.set_timer(pygame.USEREVENT + 1, upgrade_spawn_time)

        if in_menu:
            draw_menu(start_button, instructions_button, quit_button)
        elif in_instructions:
            draw_instructions(back_button)
        elif in_win_screen:
            draw_win_screen(winner)
        else:
            if handle_movement(keys, player1, player2, in_menu):
                in_win_screen = False
                in_menu = True

            player1.move_projectiles(-PROJECTILE_VEL, [player2])
            player2.move_projectiles(-PROJECTILE_VEL, [player1])

            for asteroid in asteroids[:]:
                asteroid.move(ASTEROID_VEL)
                if asteroid.off_screen():
                    asteroids.remove(asteroid)
                elif asteroid.collide(player1):
                    player1.health -= 1
                    HIT_SOUND.play()
                    asteroids.remove(asteroid)
                elif asteroid.collide(player2):
                    player2.health -= 1
                    HIT_SOUND.play()
                    asteroids.remove(asteroid)

            for upgrade in upgrades[:]:
                upgrade.move(ASTEROID_VEL)
                if upgrade.off_screen():
                    upgrades.remove(upgrade)
                elif upgrade.collide(player1):
                    player1.health = min(player1.health + 1, MAX_HEALTH)
                    UPGRADE_SOUND.play()
                    upgrades.remove(upgrade)
                elif upgrade.collide(player2):
                    player2.health = min(player2.health + 1, MAX_HEALTH)
                    UPGRADE_SOUND.play()
                    upgrades.remove(upgrade)

            if player1.health <= 0:
                winner = "Gracz 2"
                in_win_screen = True

            if player2.health <= 0:
                winner = "Gracz 1"
                in_win_screen = True

            draw_window(player1, player2, asteroids, upgrades)

if __name__ == "__main__":
    main()
