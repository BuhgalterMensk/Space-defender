import time

import pygame
import sys
from bullet import Bullet
from ufo import Ufo

def events(screen, gun, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type ==pygame.KEYDOWN:
            # key to right
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                gun.mright = True
            #key to left
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                gun.mleft = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet (screen, gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            #stop moving right
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                gun.mright = False
            #stop moving left
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                gun.mleft = False

def update (bg_color, screen, stats, sc, gun, ufos, bullets):
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    ufos.draw(screen)
    pygame.display.flip()

def update_bullets (bullets, screen, stats, sc, ufos):

    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    if collisions:
        for ufos in collisions.values():
           stats.score+=10*len(ufos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_lives()
    if len(ufos) == 0:
        bullets.empty()
        create_army(screen, ufos)

def gun_kill(stats, screen, sc, gun, ufos, bullets):

    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_lives()
        ufos.empty()
        bullets.empty()
        create_army(screen, ufos)
        gun.create_gun()
        time.sleep(2)
    else:
        stats.run_games = False
        sys.exit()

def update_ufos(stats, screen, sc, gun, ufos, bullets):

    ufos.update()
    if pygame.sprite.spritecollideany(gun, ufos):
        gun_kill(stats, screen, sc, gun, ufos, bullets)
    ufos_check(stats, screen, sc, gun, ufos, bullets)

def ufos_check(stats, screen, sc, gun, ufos, bullets):

    screen_rect=screen.get_rect()
    for ufo in ufos.sprites():
        if ufo.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen,sc, gun, ufos, bullets)
            break

def create_army(screen, ufos):

    ufo = Ufo(screen)
    ufo_width = ufo.rect.width
    number_ufos_x=int((700-2*ufo_width)/ufo_width)
    ufo_height = ufo.rect.height
    number_ufo_y = int((800-100-2*ufo_height)/ufo_height)

    for row_num in range (number_ufo_y):
        for ufo_num in range(number_ufos_x):
            ufo = Ufo(screen)
            ufo.x = ufo_width*(ufo_num+1)
            ufo.y= ufo_height*(row_num+1)
            ufo.rect.x = ufo.x
            ufo.rect.y = ufo.y
            ufos.add(ufo)

def check_high_score(stats, sc):

    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('Record.txt','w') as f:
            f.write(str(stats.high_score))