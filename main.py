import pygame
import sys
import randomп
from classes import Background, EnemyBullet, Cannon, Monster, Bullet
from constants import size, height, width
import Groups

level = '1'


def game_over():
    pygame.quit()
    sys.exit()


def show_end():
    global level
    level = '1'
    end_screen = pygame.image.load("data/end.jpg")
    end_screen = pygame.transform.scale(end_screen, (width, height))
    screen.blit(end_screen, (0, 0))
    font = pygame.font.Font("data/font.ttf", 50)
    end_text = font.render("Спасибо за игру", True, (0, 0, 255))
    screen.blit(end_text, (200, 100))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_intro()
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            show_intro()


def show_defeat():
    global level
    level = '1'
    defeat_image = pygame.image.load("data/defeat.jpg")
    defeat_screen = pygame.transform.scale(defeat_image, (width, height))
    screen.blit(defeat_screen, (0, 0))
    font = pygame.font.Font("data/font.ttf", 50)
    defeat_text = font.render("Вы проиграли :(", True, (0, 0, 255))
    screen.blit(defeat_text, (200, 100))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_intro()
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            show_intro()


def show_intro():
    global level
    Groups.all_bullets.empty()
    intro_screen = pygame.image.load("data/game_fon.jpg")
    intro_screen = pygame.transform.scale(intro_screen, (width, height))
    screen.blit(intro_screen, (0, 0))
    font = pygame.font.Font("data/font.ttf", 50)
    level_font = pygame.font.Font("data/font.ttf", 30)
    if level == '1':
        Groups.all_monsters.empty()
        Groups.all_bullets.empty()
        Groups.enemy_bullets.empty()
        new_text = font.render("Новая игра", True, (0, 0, 255))
        exit_text = font.render("Выход", True, (0, 0, 255))
        screen.blit(new_text, (50, 100))
        screen.blit(exit_text, (50, 200))
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.x = 50
        exit_text_rect.y = 200
        new_text_rect = new_text.get_rect()
        new_text_rect.x = 50
        new_text_rect.y = 100
        create_level(level)
    else:
        game_text = font.render("Продолжить", True, (0, 0, 255))
        level_text = level_font.render(f'Уровень: {level}', True, (0, 0, 255))
        screen.blit(level_text, (115, 135))
        screen.blit(game_text, (50, 100))
        new_text = font.render("Новая игра", True, (0, 0, 255))
        exit_text = font.render("Выход", True, (0, 0, 255))
        screen.blit(new_text, (50, 200))
        screen.blit(exit_text, (50, 300))
        game_text_rect = game_text.get_rect()
        game_text_rect.x = 50
        game_text_rect.y = 100
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.x = 50
        exit_text_rect.y = 300
        new_text_rect = new_text.get_rect()
        new_text_rect.x = 50
        new_text_rect.y = 200
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_text_rect.collidepoint(event.pos):
                    game_over()
                elif new_text_rect.collidepoint(event.pos):
                    level = '1'
                    Groups.all_monsters.empty()
                    Groups.all_bullets.empty()
                    Groups.enemy_bullets.empty()
                    create_level(level)
                    return
                elif level != '1' and game_text_rect.collidepoint(event.pos):
                    create_level(level)
                    return


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
            if int(loaded_level[y][x]) in range(0, 10):
                monster = Monster(x * Monster.rect.width, -y * Monster.rect.height, int(loaded_level[y][x]))
            elif loaded_level[y][x] == "B":
                monster = Monster(0, -300, 150)


pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Monster_rampage")
BackGround = Background("data/fon.png", [0, 0])
cannon = Cannon(10, 15)
FPS = 20
show_intro()
schet = 0
while True:
    schet += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        show_intro()
    Groups.all_people.update()
    if schet % 3 == 0 and keys[pygame.K_SPACE]:
        bullet = Bullet(cannon.get_pos()[0] - 20, cannon.get_pos()[1])
    if level == '5':
        if schet % int(level) * 5 == 0:
            for sprite in Groups.all_monsters:
                enemy_bullet = EnemyBullet(sprite.rect.x + random.randint(0, sprite.image.get_size()[0]),
                                           sprite.rect.y + sprite.image.get_size()[1])
    if not Groups.all_monsters:
        if level == '5':
            show_end()
        else:
            level = str(int(level) + 1)
            show_intro()
    Groups.all_bullets.update()
    Groups.all_monsters.update()
    Groups.enemy_bullets.update()
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    Groups.enemy_bullets.draw(screen)
    Groups.all_people.draw(screen)
    Groups.all_bullets.draw(screen)
    Groups.all_monsters.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
