import pygame
import random
from classes import Background, EnemyBullet, Cannon, \
    Bullet, show_end, show_intro, level, screen, game_over, show_defeat
import Groups
import constants

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Monster_rampage")
BackGround = Background("data/fon.png", [0, 0])
cannon = Cannon(10, 15)
FPS = 20
show_intro(level)
schet = 0
while True:
    schet += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
    for monster in Groups.all_monsters:
        if monster.rect.y > constants.height:
            level = '1'
            show_defeat()
    for cannon in Groups.all_people:
        if pygame.sprite.spritecollideany(cannon, Groups.all_monsters) or pygame.sprite.spritecollideany(cannon,
                                                                                                         Groups.enemy_bullets):
            level = '1'
            show_defeat()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        xlevel = show_intro(level)
    Groups.all_people.update()
    if schet % 3 == 0 and keys[pygame.K_SPACE]:
        bullet = Bullet(cannon.get_pos()[0] - 20, cannon.get_pos()[1])
    if schet % (int(level) * 5) == 0:
        for sprite in Groups.all_monsters:
            if sprite.power >= 5:
                enemy_bullet = EnemyBullet(sprite.rect.x + random.randint(0, sprite.image.get_size()[0]),
                                           sprite.rect.y + sprite.image.get_size()[1])
    if not Groups.all_monsters:
        if level == '5':
            level = '1'
            show_end()
        else:
            level = show_intro(str(int(level) + 1))
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
