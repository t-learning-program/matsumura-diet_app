import streamlit as st
import const

# フォルダ名.ファイル名 という形で読み込む
from utils import session
from views import goal
from views import record

# ページ設定
st.set_page_config(page_title="食生活管理アプリ", layout="wide")

st.title(const.APP_TITLE)

# 1. 初期化処理
session.init_session_state()

# 2. 目標設定セクション
goal.show()

# 3. 食事記録セクション
record.show()