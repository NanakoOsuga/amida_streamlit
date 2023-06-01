# 必要なライブラリのインポート
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np


# キャッシュ(再計算をスキップ)
@st.cache_data()
def create_and_cache_amida(list, bar_horizontal, font_color, line_w, h, w):
    return create_amida(list, bar_horizontal, font_color, line_w, h, w)


# あみだくじを作る関数
def create_amida(list, bar_horizontal, font_color, line_w, h, w):

    global election
    global width_w
    global width_h
    global font
    global base_img

    # 情報入力
    bar_vertical=len(list)
    width_h=int((h-400)/bar_horizontal)
    width_w=int(w/bar_vertical)

    # ベース画像の作成
    base_img=Image.new("L",(w+width_w,h+width_h))

    # PillowからNumPyへの変換
    base_img=np.array(base_img)

    # あみだの線を描写する
    for i in range(bar_vertical):
        base_img[width_h+100:-width_h-100,(i+1)*width_w-line_w:(i+1)*width_w+line_w]=200
    for i in range(bar_horizontal):
        pos=np.random.randint(1,bar_vertical)
        base_img[width_h+200+int((i+1)*width_h-line_w):width_h+200+int((i+1)*width_h+line_w),pos*width_w:(pos+1)*width_w]=200

    # NumPyからPillowへの変換
    base_img=Image.fromarray(base_img)

    # 候補者リストを描写する
    font = ImageFont.truetype("./NotoSansJP-Black.ttf", 50)
    for i in range(bar_vertical):
        ImageDraw.Draw(base_img).text(((i+1)*width_w-12*len(list[i]), 50), list[i], font = font , fill = font_color)
    
    election=np.random.randint(0,bar_vertical)
    
    ImageDraw.Draw(base_img).text(((election+1)*width_w-25, h-100), '★', font = font , fill = font_color)

    return base_img


# 画面を表示する関数
def main_content():

    # streamlitアプリケーションの構築
    st.title("あみだくじ作成アプリ")
    st.sidebar.header("設定")

    # ユーザー入力
    list = st.sidebar.text_input("リスト", "AA,BB,CC,DD,EE,FF,GG,HH").split(",")
    bar_horizontal = st.sidebar.slider("横棒の数", 5, 50, 25)
    line_w = st.sidebar.slider("あみだくじの線の太さ", 1, 10, 5)
    h = st.sidebar.slider("画像の高さ", 300, 3000, 1200)
    w = st.sidebar.slider("画像の幅", 300, 3000, 1200)

    font_color = 255

    # picturesのリストを初期化
    pictures = []

    # あみだくじの画像を作成
    amida_img = create_and_cache_amida(list, bar_horizontal, font_color, line_w, h, w)

    # picturesにあみだくじの画像を追加
    pictures.append(amida_img)

    # あみだくじを表示
    st.image(pictures[-1])

    # Numpy配列をコピー
    amida_img = np.array(base_img)

    # ★を移動させる関数
    def show_pic(amida_img,hpos,wpos,n):
        img=Image.fromarray(amida_img)
        ImageDraw.Draw(img).text((wpos-25, hpos-25), '★', font = font , fill = font_color)
        pictures.append(img.convert('P'))

    # ★マークの移動
    wpos=int((election+1)*width_w)
    spos=30
    n=0

    # 上左右に移動
    for i in range(h-width_h-100+25,width_h+100,-line_w*2):
        hpos=i
        # 上に進む
        if amida_img[i, wpos-spos]<100 and amida_img[i, wpos+spos]<100: 
            show_pic(amida_img,hpos,wpos,n)
            n+=1 
        # 左に進む
        elif amida_img[i, wpos-spos]>100:
            j=0
            while amida_img[i, wpos-j]>100:
                j+=1
                if j%(line_w*2)==0:
                    show_pic(amida_img,hpos,wpos-j,n)
                    n+=1
            i+=10
            wpos=wpos-j+line_w
        # 右に進む
        else:
            j=0
            while amida_img[i, wpos+j]>100:
                j+=1
                if j%(line_w*2)==0:
                    show_pic(amida_img,hpos,wpos+j,n)
                    n+=1
            wpos=wpos+j-line_w

    # 「当たりを表示」ボタンが押されたら、動画を表示
    if st.button('当たりを表示'):
        # gifをディスクに一時的に保存
        pictures[0].save('anime.gif', save_all=True, append_images=pictures[1:], optimize=False, duration=20, loop=0)
 
        # 保存したgifを表示
        st.image('anime.gif', use_column_width=True)