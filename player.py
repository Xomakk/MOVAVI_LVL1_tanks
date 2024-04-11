import time
import pygame
import settings


class Player:
    def __init__(
        self,
        groups: tuple[pygame.sprite.Group],
        image: str,
        fire_sound: str,
        reload: int,
        start_x: 10,
        start_y: 10,
        rotate: float = 0,
    ) -> pygame.sprite.Sprite:
        self.sprite = pygame.sprite.Sprite(*groups)
        self.sprite.image = pygame.transform.rotate(pygame.image.load(image), rotate)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = start_x
        self.sprite.rect.y = start_y

        self.fire_sound = pygame.mixer.Sound(fire_sound)
        self.rotate = rotate
        self.reload = reload
        self.spawn_time = time.time()

    def check_collide(self, srpite_group):
        for sprite in srpite_group:
            if pygame.sprite.collide_mask(self.sprite, sprite):
                return True
        return False

    def move_controll(self):
        keys = pygame.key.get_pressed()

        val_y = 0
        if keys[pygame.K_w] and self.sprite.rect.top > 0:
            val_y = -settings.PLAYER_MOVE_SPEED
        if keys[pygame.K_s] and self.sprite.rect.bottom < settings.SCREEN_HEIGHT:
            val_y = settings.PLAYER_MOVE_SPEED

        self.sprite.rect.y += val_y

    def fire(
        self,
        bullet_groups: list,
        image: str,
        rotate: float,
        speed_x: float = 0,
        speed_y: float = 0,
    ):
        time_now = time.time()
        if time_now - self.spawn_time > self.reload:
            Bullet(
                bullet_groups,
                image,
                rotate,
                self.sprite.rect.centerx,
                self.sprite.rect.centery,
                speed_x,
                speed_y,
            )
            self.fire_sound.play()
            self.spawn_time = time_now


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list,
        image: str,
        rotate: float,
        start_x: float,
        start_y: float,
        speed_x: float = 0,
        speed_y: float = 0,
    ):
        super().__init__(groups)
        self.image = pygame.transform.rotate(pygame.image.load(image), rotate)
        self.rect = self.image.get_rect()
        self.rect.centerx = start_x
        self.rect.centery = start_y

        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right > settings.SCREEN_WIDTH:
            self.kill()
