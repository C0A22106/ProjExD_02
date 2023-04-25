import random
import sys

import pygame as pg

delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, 1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (1, 0),
        }


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し,真理値タプルを返す関数
    引数１：画面surfaceのRect
    引数２：こうかとん、または、爆弾SurfaceのRect
    戻り値：横方向、縦方向のはみ出し判定結果（画面内：True/画面外:False）
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_bk_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    gli_chi = pg.image.load("ex02/fig/yakitori.jpeg")
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    mv_dir = (-1, 0)    # 始めのこうかとんの向き
    
    x = random.randint(0, 1600)
    y = random.randint(0, 900)
    bb_rct.center = (x, y)
    kk_rct.center = (900, 400)
    vx = 1
    vy = 1
    tmr = 0

    kk_dir = {
         (-1, 0): kk_img,
         (-1, 1): pg.transform.rotate(kk_img, 45),
         (0, 1): pg.transform.rotate(kk_bk_img, 270),
         (1, 1): pg.transform.rotate(kk_bk_img, 45),
         (1, 0): kk_bk_img,
         (1, -1): pg.transform.rotate(kk_bk_img, 315),
         (0, -1): pg.transform.rotate(kk_bk_img, 90),
         (-1, -1): pg.transform.rotate(kk_img, 45),
         }  # こうかとんの傾きとキーを対応させた辞書

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1

        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
                #mv_dir = (mv_dir[0] + mv[0], mv_dir[1] + mv[1]) #  進行方向をmv_dirに代入
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
                    mv_dir = (-mv[0], -mv[1]) #  進行方向をmv_dirに代入

        screen.blit(bg_img, [0, 0])
        screen.blit(bb_img, bb_rct)
        screen.blit(kk_dir[mv_dir], kk_rct) #kk_dirに応じた向きのこうかとんを出力
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:    # 横がはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):
            screen.blit(bg_img, [0, 0])
            screen.blit(gli_chi, kk_rct)
            pg.display.update()
            pg.time.delay(50000)
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()