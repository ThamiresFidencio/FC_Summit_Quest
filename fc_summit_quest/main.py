import pygame
import sys
from Code.enemy import Enemy
from Code.player import Player
from Code.platform import Platform

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FC Summit Quest")
clock = pygame.time.Clock()

GOLD = (212, 175, 55)
GOLD_LIGHT = (235, 205, 96)
WHITE = (245, 245, 245)

GROUND_GREEN = (88, 140, 74)
PLATFORM_GREEN = (74, 112, 63)

title_font = pygame.font.SysFont("arial", 60, bold=True)
button_font = pygame.font.SysFont("arial", 30, bold=True)
text_font = pygame.font.SysFont("arial", 16)
hud_font = pygame.font.SysFont("arial", 26, bold=True)
win_font = pygame.font.SysFont("arial", 32, bold=True)

button_rect = pygame.Rect(WIDTH // 2 - 150, 300, 300, 70)

bg = pygame.image.load("assets/imagens/montain.jpg").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
overlay.fill((10, 15, 25, 55))

flag = pygame.image.load("assets/imagens/bandeira.png").convert_alpha()
flag = pygame.transform.scale(flag, (70, 90))

# sons
jump_sound = pygame.mixer.Sound("assets/imagens/jump.wav")
hurt_sound = pygame.mixer.Sound("assets/imagens/hurt.wav")
win_sound = pygame.mixer.Sound("assets/imagens/power_up.wav")

pygame.mixer.music.load("assets/imagens/time_for_adventure.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

player = Player(jump_sound)

platforms = [
    Platform(0, 500, 800, 100, GROUND_GREEN),
    Platform(120, 420, 140, 20, PLATFORM_GREEN),
    Platform(350, 340, 140, 20, PLATFORM_GREEN),
    Platform(580, 260, 140, 20, PLATFORM_GREEN),
    Platform(300, 180, 140, 20, PLATFORM_GREEN),
    Platform(90, 80, 140, 20, PLATFORM_GREEN),
    Platform(380, -20, 140, 20, PLATFORM_GREEN),
    Platform(600, -120, 140, 20, PLATFORM_GREEN),
    Platform(250, -220, 140, 20, PLATFORM_GREEN),
    Platform(80, -320, 140, 20, PLATFORM_GREEN),
    Platform(340, -420, 140, 20, PLATFORM_GREEN),
    Platform(590, -520, 140, 20, PLATFORM_GREEN),
]

goal_platform = Platform(320, -640, 160, 20, GOLD)

enemy1 = Enemy(610, 220, 580, 720)
enemy3 = Enemy(100, -340, 80, 220)

enemies = [enemy1, enemy3]

camera_offset = 0
max_height = 0
game_started = False
game_won = False
running = True
hit_cooldown = 0

while running:
    dt = clock.tick(60)
    if hit_cooldown > 0:
        hit_cooldown -= dt

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    previous_won = game_won

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_started:
        screen.blit(bg, (0, 0))
        screen.blit(overlay, (0, 0))

        title = title_font.render("FC Summit Quest", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GOLD_LIGHT, button_rect, border_radius=14)
            if mouse_click[0]:
                game_started = True
        else:
            pygame.draw.rect(screen, GOLD, button_rect, border_radius=14)

        pygame.draw.rect(screen, (40, 30, 20), button_rect, 2, border_radius=14)

        button_text = button_font.render("INICIAR", True, (30, 20, 10))
        screen.blit(
            button_text,
            (
                button_rect.centerx - button_text.get_width() // 2,
                button_rect.centery - button_text.get_height() // 2
            )
        )

        # faixa fina
        controls_bg = pygame.Surface((WIDTH, 20), pygame.SRCALPHA)
        controls_bg.fill((10, 15, 25, 100))
        screen.blit(controls_bg, (0, HEIGHT - 20))

        controls = text_font.render(
            "SETAS: MOVER | ESPAÇO: PULAR | ESC: SAIR",
            True,
            WHITE
        )
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 18))

    else:
        player.update(keys, platforms + [goal_platform])

        # câmera sobe
        if player.rect.y < 250:
            diff = 250 - player.rect.y
            player.rect.y = 250
            camera_offset += diff

            for p in platforms:
                p.rect.y += diff

            goal_platform.rect.y += diff

            for enemy in enemies:
                enemy.rect.y += diff

        # câmera desce
        elif player.rect.y > 350 and camera_offset > 0:
            diff = player.rect.y - 350
            player.rect.y = 350
            camera_offset -= diff

            for p in platforms:
                p.rect.y -= diff

            goal_platform.rect.y -= diff

            for enemy in enemies:
                enemy.rect.y -= diff

        altitude = max(0, camera_offset)
        if altitude > max_height:
            max_height = altitude

        # ✅ VITÓRIA CORRIGIDA
        if (
            player.vel_y >= 0 and
            player.rect.bottom >= goal_platform.rect.top and
            player.rect.bottom <= goal_platform.rect.top + 10 and
            player.rect.centerx > goal_platform.rect.left + 10 and
            player.rect.centerx < goal_platform.rect.right - 10
        ):
            game_won = True
            if not previous_won:
                win_sound.play()

        for enemy in enemies:
            enemy.update()

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect) and hit_cooldown <= 0:
                hurt_sound.play()
                player.rect.x = 350
                player.rect.y = 420
                player.vel_y = 0
                hit_cooldown = 800
                break

        screen.blit(bg, (0, 0))
        screen.blit(overlay, (0, 0))

        for p in platforms:
            p.draw(screen)

        goal_platform.draw(screen)

        flag_x = goal_platform.rect.centerx - flag.get_width() // 2
        flag_y = goal_platform.rect.top - flag.get_height() + 5
        screen.blit(flag, (flag_x, flag_y))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        hud = hud_font.render(f"{max_height} m", True, WHITE)
        screen.blit(hud, (20, 20))

        if game_won:
            text = win_font.render("Cume alcançado!", True, GOLD)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    pygame.display.update()

pygame.quit()
sys.exit()