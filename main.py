
def play():
    import pygame
    import sys
    import random
    import time
    pygame.init()

    # цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # переменные и первые команды
    W = 800
    H = 600
    clock = pygame.time.Clock()
    fps = 15

    pygame.mouse.set_visible(True)

    mainscreen = pygame.display.set_mode((W, H))
    menuimage = pygame.image.load('menu.png')

    pygame.mixer.music.load('музыка.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.8)

    # меню, цикл (пока чего-то не нажмешь меню будет висеть)
    menu = True
    while menu:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            # нажатие кнопок PLAY и EXIT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sp1 = event.pos

                if 73 < sp1[0] < 410 and 306 < sp1[1] < 415:
                    menu = False
                    time.sleep(1)

                    pygame.mixer.music.set_volume(0.3)
                    pygame.mouse.set_visible(False)

                elif 455 < sp1[0] < 745 and 447 < sp1[1] < 545:
                    sys.exit()

        mainscreen.blit(menuimage, (0, 0))
        pygame.draw.rect(mainscreen, RED, (0,0, W, H), 10)
        pygame.display.flip()


    # спрайт игрока и группа
    player_group = pygame.sprite.Group()
    class Player(pygame.sprite.Sprite):
        # условия создания
        def __init__(self, filename, plx, ply, position, p):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.rect = self.image.get_rect(center=(plx, ply))
            self.position = position
            self.p = p

        # передвижение
        def update(self, speed):
            if self.p==1:
                self.speedy = 0
                self.speedx = 0

            tank_up = self.image

            keys = pygame.key.get_pressed()

            if pygame.sprite.spritecollide(player, zombie_group, True):
                x = random.randrange(110, 700, 54)
                y = random.randrange(120, 500, 47)
                zombie = Block('zombie.png', x, y)
                while (pygame.sprite.spritecollide(zombie, block_kirpich_group, False) or pygame.sprite.spritecollide(
                        zombie, block_water_group, False)):
                    x = random.randrange(110, 700, 54)
                    y = random.randrange(120, 500, 47)
                    zombie = Block('zombie.png', x, y)
                zombie_group.add(zombie)


            if keys[pygame.K_UP] or self.p==1:
                self.image = tank_up
                self.p=0
                # вверх
                if self.position == 0:
                    self.speedy = -speed
                # направо
                if self.position == 1:
                    self.speedx = speed
                # налево
                if self.position == 3:
                    self.speedx = -speed
                # вниз
                if self.position == 2:
                    self.speedy = speed

            # если трава или вода то скорость замедляем
            if pygame.sprite.spritecollide(player, block_water_group, False) or pygame.sprite.spritecollide(player, block_grass_group, False):
                if self.position == 0:
                    self.speedy = -speed//3
                if self.position == 1:
                    self.speedx = speed//3
                if self.position == 3:
                    self.speedx = -speed//3
                if self.position == 2:
                    self.speedy = speed//3
                # если в воде и сталкиваешься с кирпичом
                elif pygame.sprite.spritecollide(player, block_kirpich_group, False):
                    if self.position == 0:
                        self.rect.y += 8
                    if self.position == 1:
                        self.rect.x -= 8
                    if self.position == 3:
                        self.rect.x += 8
                    if self.position == 2:
                        self.rect.y -= 8
                    self.speedx = 0
                    self.speedy = 0

            # если кирпичи то скорость в ноль и отступаем назад
            elif pygame.sprite.spritecollide(player, block_kirpich_group, False):
                if self.position == 0:
                    self.rect.y += 8
                if self.position == 1:
                    self.rect.x -= 8
                if self.position == 3:
                    self.rect.x += 8
                if self.position == 2:
                    self.rect.y -= 8
                self.speedx = 0
                self.speedy = 0

            # иначе значит чистое поле и скорость возвращаем к первоначальной
            else:
                if self.position == 0:
                    self.speedy = -speed
                if self.position == 1:
                    self.speedx = speed
                if self.position == 3:
                    self.speedx = -speed
                if self.position == 2:
                    self.speedy = speed

            self.rect.y += self.speedy
            self.rect.x += self.speedx

        # движение влево
        def moveLeft(self):
            self.p=1
            tank_left = pygame.transform.rotate(self.image, 90)
            self.image = tank_left

            # разворот
            if self.position == 0:
                self.rect.y += 4
            if self.position == 1:
                self.rect.x -= 4
            if self.position == 3:
                self.rect.x += 4
            if self.position == 2:
                self.rect.y -= 4

            self.position -= 1
            self.position = self.position - (self.position // 4) * 4

        # движение вправо
        def moveRight(self):
            self.p=1
            tank_right = pygame.transform.rotate(self.image, -90)
            self.image = tank_right

            # разворот
            if self.position == 0:
                self.rect.y += 4
            if self.position == 1:
                self.rect.x -= 4
            if self.position == 3:
                self.rect.x += 4
            if self.position == 2:
                self.rect.y -= 4
            self.position += 1
            self.position = self.position - (self.position // 4) * 4

        # выстрел
        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.position)
            bullet_group.add(bullet)
            pygame.mixer.music.load('выстрел.mp3')
            pygame.mixer.music.play()
            #pygame.mixer.music.load('музыка.mp3')
            #pygame.mixer.music.play(0, i/1000, 0)
            #print(i)
            #i = pygame.time.get_ticks()
            #pygame.mixer.music.set_volume(0.3)

    # создание спрайта игрока и его помещение в группу
    player = Player('tank.png', W//2, H-150, 0, 1)
    player_group.add(player)

    # пуля
    bullet_group = pygame.sprite.Group()
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((15, 15))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(center=(x, y))
            self.position = position

        # полет пули
        def update(self, speed):
            if self.position == 0:
                self.rect.y -= speed
            if self.position == 1:
                self.rect.x += speed
            if self.position == 2:
                self.rect.y += speed
            if self.position == 3:
                self.rect.x -= speed
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.position)

            # попадание в кирпич
            if pygame.sprite.spritecollide(bullet, block_kirpich_group, False):
                self.kill()
            # попадание в траву
            if pygame.sprite.spritecollide(bullet, block_grass_group, True):
                pass
            # попадание в зомби
            if pygame.sprite.spritecollide(bullet, zombie_group, True):
                x = random.randrange(110, 700, 54)
                y = random.randrange(120, 500, 47)
                zombie = Block('zombie.png', x, y)
                while (pygame.sprite.spritecollide(zombie, block_kirpich_group, False) or pygame.sprite.spritecollide(zombie, block_water_group, False)):
                    x = random.randrange(110, 700, 54)
                    y = random.randrange(120, 500, 47)
                    zombie = Block('zombie.png', x, y)
                zombie_group.add(zombie)
                self.kill()


    # коробка из кирпичей
    # кирпичи по-середине
    block_kirpich_group = pygame.sprite.Group()
    class Block(pygame.sprite.Sprite):
        def __init__(self, filename, blx):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect(center=(blx, H//2))
    for x in range (250, 550, 53):
        block = Block('kirpich.png', x)
        block_kirpich_group.add(block)
    # кирпичи сверху
    class Block(pygame.sprite.Sprite):
        def __init__(self, filename, blx):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect(topleft=(blx, 1))
    for x in range (0, W, 53):
        block = Block('kirpich.png', x)
        block_kirpich_group.add(block)
    # курпичи снизу
    class Block(pygame.sprite.Sprite):
        def __init__(self, filename, blx):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect(bottomleft=(blx, H))
    for x in range (0, W, 53):
        block = Block('kirpich.png', x)
        block_kirpich_group.add(block)
    # кирпичи слева
    class Block(pygame.sprite.Sprite):
        def __init__(self, filename, bly):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect(topleft=(0, bly))
    for y in range (47, H-64, 46):
        block = Block('kirpich.png', y)
        block_kirpich_group.add(block)
    # кирпичи справа
    class Block(pygame.sprite.Sprite):
        def __init__(self, filename, bly):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect(topright=(W, bly))
    for y in range (47, H-64, 46):
        block = Block('kirpich.png', y)
        block_kirpich_group.add(block)


    block_water_group = pygame.sprite.Group()
    block_grass_group = pygame.sprite.Group()
    zombie_group = pygame.sprite.Group()
    class Block(pygame.sprite.Sprite):
        def __init__(self, filename, blx, bly):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect(topleft=(blx, bly))
    # первый спавн зомби
    x = random.randrange(110, 700, 54)
    y = random.randrange(120, 500, 47)
    zombie = Block('zombie.png', x, y)
    while (pygame.sprite.spritecollide(zombie, block_kirpich_group, False) or pygame.sprite.spritecollide(zombie, block_water_group, False)):
        x = random.randrange(110, 700, 54)
        y = random.randrange(120, 500, 47)
        zombie = Block('zombie.png', x, y)
    zombie_group.add(zombie)

    # спрва
    for x in range (570, 625, 54):
        block = Block('grass.png', x, 391)
        block_grass_group.add(block)
    block = Block('grass.png', x-54, 390+47)
    block_grass_group.add(block)

    # трава слева
    for y in range (120, 350, 47):
        block = Block('grass.png', 110, y)
        block_grass_group.add(block)

    # вода сверху
    for x in range (500, 700, 54):
        block = Block('water.png', x, 180)
        block_water_group.add(block)

    # вода по-середине
    for x in range (250, 400, 53):
        block = Block('water.png', x-27, H//2+23)
        block_water_group.add(block)
    block = Block('water.png', 200-30, H//2-3)
    block_water_group.add(block)

    # кирпичи снизу
    for x in range(100, 160, 53):
        block = Block('kirpich.png', x, 390+47)
        block_kirpich_group.add(block)

    # кирпичи и трава сверху
    for x in range(450, 600, 53):
        block = Block('kirpich.png', x , 100)
        block_kirpich_group.add(block)
    block = Block('grass.png', 450-53, 100-47)
    block_grass_group.add(block)


    # лягушка
    frog_group = pygame.sprite.Group()
    class Frog(pygame.sprite.Sprite):
        def __init__(self, frx, fry):
            pygame.sprite.Sprite.__init__(self)
            self.frogsprites = []
            self.frogsprites.append(pygame.image.load('frog/attack_1.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_2.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_3.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_4.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_5.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_6.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_7.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_8.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_9.png'))
            self.frogsprites.append(pygame.image.load('frog/attack_10.png'))
            self.current_sprite = 0
            self.image = self.frogsprites[self.current_sprite]
            self.rect = self.image.get_rect(bottomleft=(frx, fry))

        # движение лягушки
        def update(self, speed):
            self.current_sprite += speed
            if self.current_sprite >= len(self.frogsprites):
                self.current_sprite = 0
            self.image = self.frogsprites[int(self.current_sprite)]

    # создание спрайта лягушки и помещение его в группу
    frog = Frog(40, 40)
    frog_group.add(frog)

    # кнопки и главный цикл
    F = R = O = G = False
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # нажатие (комбинация) для активации лягушки
                if event.key == pygame.K_f:
                    F = True
                elif event.key == pygame.K_r:
                    R = True
                elif event.key == pygame.K_o:
                    O = True
                elif event.key == pygame.K_g:
                    G = True
                # выстрел
                elif event.key == pygame.K_SPACE:
                    player.shoot()
                # поворот танка
                elif event.key == pygame.K_LEFT:
                    player.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    player.moveRight()
                # возврат в меню
                elif event.key == pygame.K_ESCAPE:
                    play()

        if F and R and O and G == True:
            frog_group.update(1)

        # апдейты и зарисовки
        player_group.update(3)
        bullet_group.update(50)
        clock.tick(fps)
        mainscreen.fill(BLACK)

        block_water_group.draw(mainscreen)

        zombie_group.draw(mainscreen)
        player_group.draw(mainscreen)

        block_kirpich_group.draw(mainscreen)
        block_grass_group.draw(mainscreen)

        bullet_group.draw(mainscreen)

        frog_group.draw(mainscreen)

        pygame.display.flip()
play()
exit()
