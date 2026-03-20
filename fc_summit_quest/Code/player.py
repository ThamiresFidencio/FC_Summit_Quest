import pygame


class Player:
    def __init__(self, jump_sound):
        self.sprite = pygame.image.load("assets/imagens/knight.png").convert_alpha()

        self.w = 32
        self.h = 32
        self.scale = 3

        self.idle = []
        self.run = []

        for i in range(4):
            self.idle.append(self.get_image(i, 0))

        for i in range(4):
            self.run.append(self.get_image(i, 2))

        self.state = "idle"
        self.frame = 0
        self.speed = 0.15

        self.image = self.idle[0]
        self.rect = pygame.Rect(100, 400, self.w * self.scale, self.h * self.scale)

        self.vel = 0
        self.flip = False

        self.vel_y = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.on_ground = False

        self.jump_sound = jump_sound

    def get_image(self, col, row):
        area = pygame.Rect(col * self.w, row * self.h, self.w, self.h)
        return self.sprite.subsurface(area)

    def current_anim(self):
        return self.run if self.state == "run" else self.idle

    def update(self, keys, platforms):
        self.vel = 0

        if keys[pygame.K_RIGHT]:
            self.vel = 4
            self.state = "run"
            self.flip = False
        elif keys[pygame.K_LEFT]:
            self.vel = -4
            self.state = "run"
            self.flip = True
        else:
            self.state = "idle"

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jump_sound.play()

        self.rect.x += self.vel

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                if self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        self.frame += self.speed
        if self.frame >= len(self.current_anim()):
            self.frame = 0

        frame = self.current_anim()[int(self.frame)]
        frame = pygame.transform.flip(frame, self.flip, False)
        self.image = pygame.transform.scale(
            frame,
            (self.w * self.scale, self.h * self.scale)
        )

    def draw(self, screen):
        # 👇 ajuste visual (cola o pé no chão)
        offset_y = 6
        screen.blit(self.image, (self.rect.x, self.rect.y + offset_y))