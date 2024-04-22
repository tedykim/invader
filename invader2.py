""" invader.py - Copyright 2016 Kenichiro Tanaka  """
import sys
from random import randint
import pygame
from pygame.locals import Rect, QUIT, KEYDOWN, \
    K_LEFT, K_RIGHT, K_SPACE

pygame.init()
pygame.key.set_repeat(5, 5) # pygame.key.set_repeat(delay, interval) mil sec
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

class Drawable:
    """ 전체 화면 오브젝트 슈퍼 클래스 : 全ての 描画 オブジェクト の スー パー クラス(Subete no byōga obujekuto no sūpākurasu) """
    def __init__(self, rect, offset0, offset1): # self: 파이썬에서 클래스의 메서드는 첫 번째 매개변수로 항상 자신을 참조하는 self 매개변수를 가져야 합니다. 이를 통해 클래스의 속성과 메서드에 접근할 수 있습니다.
        strip = pygame.image.load("strip.png")
        self.images = (pygame.Surface((24, 24), pygame.SRCALPHA),
                       pygame.Surface((24, 24), pygame.SRCALPHA))
        self.rect = rect
        self.count = 0
        self.images[0].blit(strip, (0, 0),
                            Rect(offset0, 0, 24, 24))
        self.images[1].blit(strip, (0, 0),
                            Rect(offset1, 0, 24, 24))

    def move(self, diff_x, diff_y):
        """ 객체이동: オブジェクトを移動(Obujekuto o idō) """
        self.count += 1
        self.rect.move_ip(diff_x, diff_y)

    def draw(self):
        """ 객체 그리기..이미지를 불러온다..: オ ブ ジェ ク ト を 描画 (Obujekuto o byōga)"""
        image = self.images[0] if self.count % 2 == 0 \
                else self.images[1]
        SURFACE.blit(image, self.rect.topleft)

class Ship(Drawable):
    """ 자기기계 오브젝트: 自機 オブジェクト(Jibata obujekuto Obujekuto) """
    def __init__(self):
        super().__init__(Rect(300, 550, 24, 24), 192, 192)

class Beam(Drawable):
    """ 빔 오브젝트:ビーム オブジェクト(Bīmu obujekuto) """
    def __init__(self):
        super().__init__(Rect(300, 0, 24, 24), 0, 24)

class Bomb(Drawable):
    """ 폭탄 오브젝트:爆弾オブジェクト(Bakudan obujekuto) """
    def __init__(self):
        super().__init__(Rect(300, -50, 24, 24), 48, 72)
        self.time = randint(5, 220)

class Alien(Drawable):
    """ 외계인 오브젝트:エイリアンオブジェクト(E i Ri An obujekuto) """
    def __init__(self, rect, offset, score):
        super().__init__(rect, offset, offset+24)
        self.score = score

def main():
    """ 메인루틴:メインルーチン(Meinrūchin) """
    sysfont = pygame.font.SysFont(None, 72)
    scorefont = pygame.font.SysFont(None, 36)
    message_clear = sysfont.render("!!CLEARED!!",
                                   True, (0, 255, 225))
    message_over = sysfont.render("GAME OVER!!",
                                  True, (0, 255, 225))
    message_rect = message_clear.get_rect()
    message_rect.center = (300, 300)
    game_over = False
    moving_left = True
    moving_down = False
    move_interval = 20
    counter = 0
    score = 0
    aliens = []
    bombs = []
    ship = Ship()
    beam = Beam()

    # 외계인 배열 초기화:エイリアンの 並 び を 初期化(Eirian no nara bi o sho ki ka)
    for ypos in range(4):
        offset = 96 if ypos < 2 else 144
        for xpos in range(10):
            rect = Rect(100+xpos*50, ypos*50 + 50, 24, 24)
            alien = Alien(rect, offset, (4-ypos)*10)
            aliens.append(alien)

    # 폭탄 설정:爆弾 を 設定(Baku dan o sette)
    for _ in range(4):
        bombs.append(Bomb())

    while True:
        ship_move_x = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    ship_move_x = -5
                elif event.key == K_RIGHT:
                    ship_move_x = +5
                elif event.key == K_SPACE and beam.rect.bottom < 0:
                    beam.rect.center = ship.rect.center

        if not game_over:
            counter += 1
            # 自機を移動
            ship.move(ship_move_x, 0)

            # 빔이동:ビームを移動(Bīmu o idō)
            beam.move(0, -15)

            # 외계인 이동:エイリアンを移動(Eirian o idō)
            area = aliens[0].rect.copy()
            for alien in aliens:
                area.union_ip(alien.rect)

            if counter % move_interval == 0:
                move_x = -5 if moving_left else 5
                move_y = 0

                if (area.left < 10 or area.right > 590) and \
                    not moving_down:
                    moving_left = not moving_left
                    move_x, move_y = 0, 24
                    move_interval = max(1, move_interval - 2)
                    moving_down = True
                else:
                    moving_down = False

                for alien in aliens:
                    alien.move(move_x, move_y)

            if area.bottom > 550:
                game_over = True

            # 폭탄 이동:爆弾を移動(Bakudan o idō)
            for bomb in bombs:
                if bomb.time < counter and bomb.rect.top < 0:
                    enemy = aliens[randint(0, len(aliens) - 1)]
                    bomb.rect.center = enemy.rect.center

                if bomb.rect.top > 0:
                    bomb.move(0, 10)

                if bomb.rect.top > 600:
                    bomb.time += randint(50, 250)
                    bomb.rect.top = -50

                if bomb.rect.colliderect(ship.rect):
                    game_over = True

            # 빔이 에이리안 충돌 : ビームがエイリアンと衝突?(Bīmu ga eirian to shōtotsu)
            tmp = []
            for alien in aliens:
                if alien.rect.collidepoint(beam.rect.center):
                    beam.rect.top = -50
                    score += alien.score
                else:
                    tmp.append(alien)
            aliens = tmp
            if len(aliens) == 0:
                game_over = True

        # 그리기 : 描画(Byōga)
        SURFACE.fill((0, 0, 0))
        for alien in aliens:
            alien.draw()
        ship.draw()
        beam.draw()
        for bomb in bombs:
            bomb.draw()

        score_str = str(score).zfill(5)
        score_image = scorefont.render(score_str,
                                       True, (0, 255, 0))
        SURFACE.blit(score_image, (500, 10))

        if game_over:
            if len(aliens) == 0:
                SURFACE.blit(message_clear, message_rect.topleft)
            else:
                SURFACE.blit(message_over, message_rect.topleft)

        pygame.display.update()
        FPSCLOCK.tick(20)

if __name__ == '__main__':
    main()
