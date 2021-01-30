import pygame
import random
import Groups
from pygame_project import show_defeat, show_intro, show_end, level
from constants import size, height, width, tile_width, tile_height


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__(Groups.all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class EnemyBullet(pygame.sprite.Sprite):
    bullet_image = pygame.image.load("data/enemy_bullet.png")

    def __init__(self, x, y):
        super().__init__(Groups.all_sprites, Groups.enemy_bullets)
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
        self.rect.x = x * tile_width + (tile_width - self.rect.width) // 2
        self.rect.y = y * tile_height + (tile_height - self.rect.height) // 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 10:
            self.y -= 1
            self.rect.y -= tile_height
        if keys[pygame.K_DOWN] and self.rect.y < (height - 100):
            self.y += 1
            self.rect.y += tile_height
        if keys[pygame.K_LEFT] and self.rect.x > 10:
            self.x -= 1
            self.rect.x -= tile_width
        if keys[pygame.K_RIGHT] and self.rect.x < (width - 100):
            self.x += 1
            self.rect.x += tile_width
        if pygame.sprite.spritecollideany(self, Groups.all_monsters) or pygame.sprite.spritecollideany(self,
                                                                                                       Groups.enemy_bullets):
            show_defeat()

    def get_pos(self):
        return self.rect.x, self.rect.y


class Monster(pygame.sprite.Sprite):
    monster_image = pygame.image.load("data/enemy.png")
    boss_image = pygame.image.load("data/boss1.png")
    enemy_image = pygame.image.load("data/bullet_enemy.png")

    def __init__(self, x, y, power):
        super().__init__(Groups.all_sprites, Groups.all_monsters)
        self.x = x
        self.y = y
        self.power = power
        if self.power == 150:
            self.image = Monster.boss_image
            self.rect = Monster.boss_image.get_rect()
        elif self.power >= 5:
            self.image = Monster.enemy_image
            self.rect = Monster.enemy_image.get_rect()
        else:
            self.image = Monster.monster_image
            self.rect = Monster.monster_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, Groups.all_bullets):
            if self.power > 1:
                self.power -= 1
            else:
                self.kill()
        if self.rect.x < 0:
            self.rect = self.rect.move(random.randint(0, int(level)), 1)
        elif self.rect.x > width:
            self.rect = self.rect.move(random.randint(-int(level), 0), 1)
        else:
            self.rect = self.rect.move(random.randint(-int(level), int(level)), 1)
        if self.rect.y >= height:
            show_defeat()


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
