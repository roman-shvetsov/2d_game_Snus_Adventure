import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
pygame.init()

W = 600
H = 400

sc = pygame.display.set_mode((W, H))

pygame.display.set_caption("Snus adventure")
background_image_endgame = pygame.image.load('images/back_end_game2.PNG')
background_image_start_game = pygame.image.load('images/start_game2.PNG')
background_image_win = pygame.image.load('images/win.PNG')
background_image_game = pygame.image.load('images/wallpaper.png')

heart_image = pygame.image.load('images/heart.png')
snus_image = pygame.image.load('images/snus.png')
galandec_image_left = pygame.image.load('images/galandec_left.png')
galandec_image_right = pygame.image.load('images/galandec_right.png')
dust_image_left = pygame.image.load('images/dust_left.png')
dust_image_right = pygame.image.load('images/dust_right.png')

pygame.mixer.music.load('music/game.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

take_snus_sound = pygame.mixer.Sound("music/take_snus2.wav")
begin_sound = pygame.mixer.Sound("music/begin.wav")
game_end_sound = pygame.mixer.Sound("music/game_end.wav")
snus_lost_sound = pygame.mixer.Sound("music/snus lost.wav")
speed_sound = pygame.mixer.Sound("music/speed.wav")
game_sound = pygame.mixer.Sound("music/game.wav")
game_win_sound = pygame.mixer.Sound("music/win (online-audio-converter.com).wav")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

clock = pygame.time.Clock()
FPS = 60

galandec = pygame.Surface((40, 110))
snus = pygame.Surface((50, 50))
snus_2lvl = pygame.Surface((50, 50))
snus_3lvl = pygame.Surface((50, 50))

ground = H - 70
rect_galandec = galandec.get_rect(centerx=W // 2)
rect_galandec.bottom = ground

rect_snus = snus.get_rect(centerx=random.randint(0, 570))
rect_snus2lvl = snus.get_rect(centerx=rect_galandec.left)
rect_snus3lvl = snus.get_rect()

snus_list = [rect_snus, rect_snus2lvl, rect_snus3lvl]  # Список снюсов, для проверки столкновения

speed = 6  # Скорость движения игрока
score = 0  # Количество пойманных шайб
lost_snus = 0  # Количество не пойманных шайб
life = 3
vector = "left"

game_end = False
game_start = False
game_win = False
lvl2 = False
lvl3 = False
run = False

footprints = []  # Нужно для снюса 3 уровня

f1 = pygame.font.Font(None, 36)
f2 = pygame.font.Font(None, 32)
causes_of_death = [" рака дёсен", " рака щёк", " поражения органов ЖКТ", " пещевого отравления", " язвы желудка"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Окно до начала игры--------------------------------------------
    if not game_start and not game_win:
        last_snus = random.randrange(50, 60)  # Снюс после которого игрок умирает
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_start = True
        sc.blit(background_image_start_game, (0, 0))
        pygame.display.update()

    # Начало игрового процесса----------------------------------------
    elif not game_end and game_start and not game_win:
        # Движение игрока
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and keys[pygame.K_SPACE]:
            rect_galandec.left -= 2 * speed
            run = True
            vector = "left"
            footprints.append(rect_galandec.left)
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and keys[pygame.K_SPACE]:
            rect_galandec.right += 2 * speed
            run = True
            vector = "right"
            footprints.append(rect_galandec.right)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            rect_galandec.left -= speed
            run = False
            vector = "left"
            footprints.append(rect_galandec.left)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            rect_galandec.right += speed
            run = False
            vector = "right"
            footprints.append(rect_galandec.right)

        # Не даём игроку выйти за границу
        if rect_galandec.left < 0:
            rect_galandec.left += 2*speed
        elif rect_galandec.right > 600:
            rect_galandec.right -= 2*speed

        # Проверяем взял ли игрок снюс
        for i in snus_list:
            if pygame.Rect.colliderect(rect_galandec, i):
                take_snus_sound.play(0)             # Звук поимки снюса
                score += 1
                i.bottom = 0
                i.left = random.randint(0, 580)
                text_score = f1.render(f'Снюс: {score}', True, (180, 0, 0))
                if score % 10 == 0:
                    life += 1

        # Описание движения первого снюса
        if rect_snus.bottom < ground:
            rect_snus.bottom += 2

        else:
            snus_lost_sound.play(0)
            lost_snus += 1
            rect_snus.bottom = 0
            rect_snus.left = random.randint(0, 580)
        # Активация 3 уровня
        if 25 <= score <= last_snus:
            lvl3 = True
            if rect_snus3lvl.bottom < ground:
                rect_snus3lvl.bottom += 4
                rect_snus3lvl.left = footprints[-3]
            else:
                snus_lost_sound.play(0)
                lost_snus += 1
                rect_snus3lvl.bottom = 0
        # Активация 2 уровня
        if 5 <= score <= last_snus:
            lvl2 = True
            if rect_snus2lvl.bottom < ground:
                rect_snus2lvl.bottom += 3
            else:
                snus_lost_sound.play(0)
                lost_snus += 1
                rect_snus2lvl.bottom = 0
                rect_snus2lvl.left = rect_snus.left

        # Выигрыш игры или проигрыш
        if lost_snus >= life:
            game_win = True
            last_snus = random.randrange(50, 60)  # Снюс после которого игрок умирает
            rect_snus2lvl.bottom = 0
            rect_snus3lvl.bottom = 0
            rect_snus.bottom = 0
            game_win_sound.play(0)  # мелодия победы
            footprints.clear()
        elif score > last_snus:
            random_death = random.choice(causes_of_death)
            last_snus = random.randrange(50, 60)  # Снюс после которого игрок умирает
            rect_snus2lvl.bottom = 0
            rect_snus3lvl.bottom = 0
            rect_snus.bottom = 0
            game_end_sound.play(0)          # мелодия проигрыша
            footprints.clear()
            game_end = True

        # ОСНОВНАЯ ОТРИСОВКА------------------
        sc.blit(background_image_game, (0, 0))
        sc.blit(snus_image, rect_snus)
        if lvl2:
            sc.blit(snus_image, rect_snus2lvl)
        if lvl3:
            sc.blit(snus_image, rect_snus3lvl)
        if vector == "left":
            sc.blit(galandec_image_left, rect_galandec)
            if run:
                speed_sound.play(0)             # Звук ускорения
                sc.blit(dust_image_left, (rect_galandec.left + 20, rect_galandec.bottom - 70))
        elif vector == "right":
            sc.blit(galandec_image_right, rect_galandec)
            if run:
                speed_sound.play(0)             # Звук ускорения
                sc.blit(dust_image_right, (rect_galandec.left - 90, rect_galandec.bottom - 70))

        # Отрисовка оставшихся жизней
        hearts = life - lost_snus
        hearts_x = 20
        for i in range(hearts):
            sc.blit(heart_image, (hearts_x, 10))
            hearts_x += 35

        # Счёт игрока
        if score > 0:
            sc.blit(text_score, (480, 20))
        pygame.display.update()

    # Если проиграл----------------------------------------------------------------------
    elif game_end:
        text_end1 = f2.render(f'Из-за {random_death}', True, (255, 255, 255))
        text_end = f1.render(f'Набрано снюса: {score}', True, (255, 255, 255))
        rect_end1 = text_end1.get_rect(centerx=W//2)
        rect_end = text_end.get_rect(centerx=W//2)
        rect_end1.bottom = 310
        rect_end.bottom = 340
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            lost_snus = 0
            life = 3
            game_end = False
            lvl2 = False
            lvl3 = False

        # Отрисовка
        sc.blit(background_image_endgame, (0, 0))
        sc.blit(text_end1, rect_end1)
        sc.blit(text_end, rect_end)
        pygame.display.update()

    # Если выиграл----------------------------------------------------------------------
    else:
        text_end = f1.render(f'Влад победил зависимость на {score} шайбе снюса', True, (40, 255, 10))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            score = 0
            lost_snus = 0
            life = 3
            game_win = False
            lvl2 = False
            lvl3 = False
        # Отрисовка
        sc.blit(background_image_win, (0, 0))
        sc.blit(text_end, (10, 370))
        pygame.display.update()

    clock.tick(FPS)
