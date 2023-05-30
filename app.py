# 必要なライブラリのインポート
import streamlit as st
from main import main_content

# ページごとの表示を切り替えるためのパラメータを取得
params = st.experimental_get_query_params()

# main.pyのmain_contentを表示
if 'page' not in params:
    main_content()