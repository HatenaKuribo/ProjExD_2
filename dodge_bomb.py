import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向のチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向のチェック
        tate = False
    return yoko,tate


def gameover(scr: pg.Surface) -> None:
    """
    引数:screenのsurface
    戻り値:無し
    画面変更後5秒待つ
    """
    # 黒背景のsurface設定
    black_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_img, (0,0,0),(0,0,WIDTH,HEIGHT))
    black_img.set_alpha(200)
    # 文字の設定
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver",True,(255,255,255))
    black_img.blit(txt, [450,325])
    # こうかとんの画像設定
    kk_img = pg.image.load("fig/8.png")
    black_img.blit(kk_img, [400,325])
    black_img.blit(kk_img,[750,325])
    # 画面変更
    scr.blit(black_img,[0,0])
    pg.display.update()
    # 5秒待つ
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数:なし
    戻り値:爆弾surfaceのタプル、加速度のタプル
    """
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1,11)]
    return tuple(bb_imgs),tuple(bb_accs)



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    # bb_img = pg.Surface((20,20))
    # pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_imgs,bb_accs = init_bb_imgs()  # 大きさの違う爆弾と加速度のタプルを得る
    bb_img = bb_imgs[0]  # 爆弾の初期状態
    bb_rect = bb_img.get_rect()
    bb_rect.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx = +5  # 爆弾の横速度
    vy = +5  # 爆弾の縦速度
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rect):  # こうかとんと爆弾が衝突
            print("ゲームオーバー")
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量
    
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):  # 画面外なら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])  # 移動を無かったことにする
        screen.blit(kk_img, kk_rct)

        # 大きさの違う爆弾を得る
        bb_img = bb_imgs[min(tmr//500, 9)]
        yoko,tate = check_bound(bb_rect)
        if not yoko:  # 横画面外なら
            vx *= -1  # 反射
        if not tate:  # 縦画面外なら
            vy *= -1  # 反射
        # 加速度を得る
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        # widthとheight属性の更新
        bb_rect.width = bb_img.get_rect().width
        bb_rect.height = bb_img.get_rect().height
        screen.blit(bb_img,bb_rect)
        bb_rect.move_ip(avx,avy)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
