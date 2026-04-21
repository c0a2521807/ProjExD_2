import os
import sys
import random
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def game_over(screen: pg.Surface) -> None:#　ゲームオーバーの表示
    ge_img = pg.Surface((WIDTH, HEIGHT))#　透明度のある黒いSurfaceを作成
    pg.draw.rect(ge_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    ge_img.set_alpha(150)
    screen.blit(ge_img, (0, 0))

    font = pg.font.Font(None, 100)#　フォントオブジェクトを作成
    text1 = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    kk_img = pg.image.load("fig/8.png")#　こうかとんの悲しい画像を読み込む
    kk_rect1 = kk_img.get_rect(center=(WIDTH // 2 - 250, HEIGHT // 2))
    kk_rect2 = kk_img.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2))

    screen.blit(text1, text_rect)
    screen.blit(kk_img, kk_rect1)
    screen.blit(kk_img, kk_rect2)

    pg.display.update()
    time.sleep(5)  

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:

    bb_imgs = []
    bb_accs = [a for a in range(1, 11)] # 加速度リスト 1〜10
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0)) # 黒を透明化
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def check_bound(rct: pg.Rect) -> tuple[bool, bool]: 
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # --- 爆弾リストの初期化 ---
    bb_imgs, bb_accs = init_bb_imgs()
    tmr = 0
    
    # 初期の爆弾設定
    vx, vy = +5, +5 
    bb_img = bb_imgs[0]
    bb_rec = bb_img.get_rect()
    bb_rec.centerx = random.randint(0, WIDTH)
    bb_rec.centery = random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rec):
            game_over(screen)
            return  
        
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:  
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        screen.blit(kk_img, kk_rct)
        
        # --- 爆弾の更新 (時間経過 tmr に応じる) ---
        idx = min(tmr // 500, 9) # 500フレームごとに段階アップ
        bb_img = bb_imgs[idx]
        # サイズが変わったのでRectのサイズを更新（中心は維持）
        curr_center = bb_rec.center
        bb_rec = bb_img.get_rect()
        bb_rec.center = curr_center
        
        # 加速度を適用した速度で移動
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        
        bb_rec.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rec)
        if not yoko: vx *= -1
        if not tate: vy *= -1

        screen.blit(bb_img, bb_rec)
        pg.display.update()
        tmr += 1 # タイマーを加算
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()