import pygame


class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        sheet = pygame.image.load("assets/imagens/slime_green.png").convert_alpha()

        frame_w = 24
        frame_h = 18

        area = pygame.Rect(1 * frame_w, 3 * frame_h, frame_w, frame_h)
        sprite = sheet.subsurface(area)

        self.image = pygame.transform.scale(sprite, (40, 30))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.left_limit = left_limit
        self.right_limit = right_limit

        self.speed = 1
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.left <= self.left_limit or self.rect.right >= self.right_limit:
            self.direction *= -1

    def draw(self, screen):
        # 👇 ajuste visual (não flutuar)
        offset_y = 4
        screen.blit(self.image, (self.rect.x, self.rect.y + offset_y))