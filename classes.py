import pygame
import random
import Groups
import sys
from constants import SIZE, HEIGHT, WIDTH, TILE_WIDTH, TILE_HEIGHT


def game_over():
    pygame.quit()
    sys.exit()


level = '1'
music_volume = 0.2

screen = pygame.display.set_mode(SIZE)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__(Groups.all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class EnemyBullet(pygame.sprite.Sprite):
    bullet_image = pygame.image.load("data/enemy_bullet.png")
    boss_bullet = pygame.image.load("data/boss_bullet.png")

    def __init__(self, x, y, level):
        super().__init__(Groups.all_sprites, Groups.enemy_bullets)
        if level == 'B':
            self.image = EnemyBullet.boss_bullet
        else:
            self.image = EnemyBullet.bullet_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x + 50
        self.rect.y = self.y

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, Groups.all_people):
            self.kill()
        self.rect = self.rect.move(0, 5)


class Cannon(pygame.sprite.Sprite):
    cannon_image = pygame.image.load("data/starship.png")

    def __init__(self, x, y):
        super().__init__(Groups.all_sprites, Groups.all_people)
        self.x = x
        self.y = y
        self.image = Cannon.cannon_image
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_WIDTH + (TILE_WIDTH - self.rect.width) // 2
        self.rect.y = y * TILE_HEIGHT + (TILE_HEIGHT - self.rect.height) // 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 10:
            self.y -= 1
            self.rect.y -= TILE_HEIGHT
        if keys[pygame.K_DOWN] and self.rect.y < (HEIGHT - 100):
            self.y += 1
            self.rect.y += TILE_HEIGHT
        if keys[pygame.K_LEFT] and self.rect.x > 10:
            self.x -= 1
            self.rect.x -= TILE_WIDTH
        if keys[pygame.K_RIGHT] and self.rect.x < (WIDTH - 100):
            self.x += 1
            self.rect.x += TILE_WIDTH

    def get_pos(self):
        return self.rect.x, self.rect.y


class Boom(pygame.sprite.Sprite):
    boom_image = pygame.image.load("data/boom.png")

    def __init__(self, x, y):
        super().__init__(Groups.all_sprites, Groups.booms)
        self.image = Boom.boom_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.otschet = 3

    def update(self):
        if self.otschet > 0:
            self.otschet -= 1
        else:
            self.kill()


class Monster(pygame.sprite.Sprite):
    monster_image = pygame.image.load("data/enemy.png")
    boss_image = pygame.image.load("data/boss1.png")
    enemy_image = pygame.image.load("data/bullet_enemy.png")

    def __init__(self, x, y, power):
        super().__init__(Groups.all_sprites, Groups.all_monsters)
        self.power = power
        if self.power == 75:
            self.image = Monster.boss_image
            self.rect = Monster.boss_image.get_rect()
        elif self.power >= 5:
            self.image = Monster.enemy_image
            self.rect = Monster.enemy_image.get_rect()
        else:
            self.image = Monster.monster_image
            self.rect = Monster.monster_image.get_rect()
        self.live = power
        self.rect = self.image.get_rect()
        self.x = x * self.rect.width
        self.y = y * self.rect.height
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, Groups.all_bullets):
            if self.live > 1:
                self.live -= 1
            else:
                self.kill()
                pygame.mixer.Channel(1).set_volume(0.3)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/sound.mp3'))
                boom = Boom(self.rect.x, self.rect.y)
        if self.rect.x < 0:
            self.rect = self.rect.move(random.randint(0, int(level)), 1)
        elif self.rect.x > WIDTH:
            self.rect = self.rect.move(random.randint(-int(level), 0), 1)
        else:
            self.rect = self.rect.move(random.randint(-int(level), int(level)), 1)


class Bullet(pygame.sprite.Sprite):
    bullet_image = pygame.image.load("data/bullet.png")

    def __init__(self, x, y):
        super().__init__(Groups.all_sprites, Groups.all_bullets)
        self.image = Bullet.bullet_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x + 50
        self.rect.y = self.y

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, Groups.all_monsters):
            self.kill()
        else:
            self.rect = self.rect.move(0, -10)
        if self.rect.y <= -1:
            self.kill()


def load_level(filename):
    with open("data/levels/" + filename + ".txt") as file:
        level = list(map(str.strip, file))
        max_len = len(max(level, key=len))
        level = list(map(lambda line: line.ljust(max_len, ' '), level))
        return level


def create_level(filename):
    loaded_level = load_level(filename)
    for y in range(len(loaded_level)):
        for x in range(len(loaded_level[y])):
            if loaded_level[y][x] == "B":
                monster = Monster(0, -1, 75)
            elif int(loaded_level[y][x]) in range(1, 10):
                monster = Monster(x, -y, int(loaded_level[y][x]))


def show_defeat():
    Groups.all_people.empty()
    defeat_image = pygame.image.load("data/defeat.jpg")
    defeat_screen = pygame.transform.scale(defeat_image, (WIDTH, HEIGHT))
    screen.blit(defeat_screen, (0, 0))
    font = pygame.font.Font("data/font.ttf", 50)
    defeat_text = font.render("You lose :(", True, (0, 0, 255))
    screen.blit(defeat_text, (200, 100))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_intro(level)
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            show_intro(level)


def show_end():
    Groups.all_people.empty()
    end_screen = pygame.image.load("data/end.jpg")
    end_screen = pygame.transform.scale(end_screen, (WIDTH, HEIGHT))
    screen.blit(end_screen, (0, 0))
    font = pygame.font.Font("data/font.ttf", 50)
    end_text = font.render("Thanks for playing", True, (0, 0, 255))
    screen.blit(end_text, (200, 100))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_intro(level)
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            show_intro(level)


def show_intro(level):
    global music_volume
    Groups.enemy_bullets.empty()
    Groups.all_people.empty()
    cannon = Cannon(10, 15)
    Groups.all_bullets.empty()
    Groups.all_monsters.empty()
    intro_screen = pygame.image.load("data/game_fon.jpg")
    intro_screen = pygame.transform.scale(intro_screen, (WIDTH, HEIGHT))
    screen.blit(intro_screen, (0, 0))
    font = pygame.font.Font("data/font.ttf", 50)
    level_font = pygame.font.Font("data/font.ttf", 30)
    if level == '1':
        Groups.all_monsters.empty()
        Groups.all_bullets.empty()
        Groups.enemy_bullets.empty()
        new_text = font.render("New game", True, (0, 0, 255))
        exit_text = font.render("Exit", True, (0, 0, 255))
        music_text = font.render("Music", True, (0, 0, 255))
        plus = font.render("+", True, (0, 0, 255))
        minus = font.render("-", True, (0, 0, 255))
        screen.blit(new_text, (50, 100))
        screen.blit(exit_text, (50, 200))
        screen.blit(music_text, (380, 700))
        screen.blit(plus, (390, 730))
        screen.blit(minus, (425, 730))
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.x = 50
        exit_text_rect.y = 200
        new_text_rect = new_text.get_rect()
        new_text_rect.x = 50
        new_text_rect.y = 100
        plus_rect = plus.get_rect()
        plus_rect.x = 390
        plus_rect.y = 730
        minus_rect = minus.get_rect()
        minus_rect.x = 425
        minus_rect.y = 730
        create_level(level)
    else:
        game_text = font.render("Continue", True, (0, 0, 255))
        level_text = level_font.render(f'Level: {level}', True, (0, 0, 255))
        screen.blit(level_text, (95, 135))
        screen.blit(game_text, (50, 100))
        new_text = font.render("New game", True, (0, 0, 255))
        exit_text = font.render("Exit", True, (0, 0, 255))
        music_text = font.render("Music", True, (0, 0, 255))
        plus = font.render("+", True, (0, 0, 255))
        minus = font.render("-", True, (0, 0, 255))
        screen.blit(new_text, (50, 200))
        screen.blit(exit_text, (50, 300))
        screen.blit(music_text, (380, 700))
        screen.blit(plus, (390, 730))
        screen.blit(minus, (425, 730))
        game_text_rect = game_text.get_rect()
        game_text_rect.x = 50
        game_text_rect.y = 100
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.x = 50
        exit_text_rect.y = 300
        new_text_rect = new_text.get_rect()
        new_text_rect.x = 50
        new_text_rect.y = 200
        plus_rect = plus.get_rect()
        plus_rect.x = 390
        plus_rect.y = 730
        minus_rect = minus.get_rect()
        minus_rect.x = 425
        minus_rect.y = 730
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_text_rect.collidepoint(event.pos):
                    game_over()
                elif plus_rect.collidepoint(event.pos):
                    music_volume += 0.1
                    pygame.mixer.Channel(0).set_volume(music_volume)
                elif minus_rect.collidepoint(event.pos):
                    music_volume -= 0.1
                    pygame.mixer.Channel(0).set_volume(music_volume)
                elif new_text_rect.collidepoint(event.pos):
                    Groups.all_monsters.empty()
                    Groups.all_bullets.empty()
                    Groups.enemy_bullets.empty()
                    create_level(level)
                    return '1'
                elif level != '1' and game_text_rect.collidepoint(event.pos):
                    create_level(level)
                    return level
