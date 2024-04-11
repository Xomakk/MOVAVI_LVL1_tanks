import random
import pygame
import settings
from player import Player
import time

pygame.init()

time_start = time.time()
score = 0


def spawn_emeny(groups: list[pygame.sprite.Group], image: str, rotate: float):
    global time_start

    time_now = time.time()
    if time_now - time_start > 2:
        time_start = time_now
        enemy = pygame.sprite.Sprite(*groups)
        enemy.image = pygame.transform.rotate(pygame.image.load(image), rotate)
        enemy.rect = enemy.image.get_rect()
        enemy.rect.left = settings.SCREEN_WIDTH + 100
        enemy.rect.top = random.randint(0, settings.SCREEN_HEIGHT) - enemy.rect.height


def enemy_move(
    enemyes: pygame.sprite.Group,
    bullets: pygame.sprite.Group,
    boom_sound: pygame.mixer.Sound,
):
    global score
    speed = 3

    for enemy in enemyes:
        enemy.rect.x -= speed
        if enemy.rect.right < 0:
            enemy.kill()

        for bullet in bullets:
            if pygame.sprite.collide_mask(enemy, bullet):
                enemy.kill()
                bullet.kill()
                boom_sound.play()
                score += 1


def main():
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # версия с полноэкранным режимом
    screen = pygame.display.set_mode(settings.SCREEN_SIZE)

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemyes = pygame.sprite.Group()

    player = Player(
        groups=[all_sprites],
        image="./images/tank_blue.png",
        fire_sound="./sounds/fire.wav",
        reload=1,
        start_x=100,
        start_y=350,
        rotate=90,
    )

    pygame.mixer.music.load("./sounds/tank_move.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    boom_sound = pygame.mixer.Sound("./sounds/boom.wav")
    game_over_sound = pygame.mixer.Sound("./sounds/game_over.wav")

    bg = pygame.image.load("./images/bg.png")
    bg_x, bg_y = 0, 0

    font_object = pygame.font.Font(None, 24)
    font_object_big = pygame.font.Font(None, 124)

    clock = pygame.time.Clock()
    run = True
    end_game = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(123)
                    player.fire(
                        bullet_groups=[bullets, all_sprites],
                        image="./images/bullet.png",
                        rotate=90,
                        speed_x=20,
                    )

        if not end_game:
            screen.blit(bg, (bg_x, bg_y))
            bg_x -= 1
            if bg.get_rect().width + bg_x < settings.SCREEN_WIDTH:
                bg_x = 0

            player.move_controll()
            end_game = player.check_collide(enemyes)
            spawn_emeny([all_sprites, enemyes], "./images/tank_red.png", -90)
            enemy_move(enemyes, bullets, boom_sound)

            for bullet in bullets:
                bullet.move()

            all_sprites.draw(screen)

            text = font_object.render(f"Score: {score}", True, "white")
            screen.blit(text, (10, 10))
        else:
            pygame.mixer.music.stop()
            game_over_sound.play()

            text = font_object_big.render("GAME OVER", True, "white")
            screen.fill("black")
            screen.blit(text, (300, 400))

        pygame.display.update()


main()

pygame.quit()
