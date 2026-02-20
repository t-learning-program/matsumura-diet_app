import streamlit as st

def init_session_state():
    """セッションステートの初期化を行う関数"""
    # 食事記録用
    if 'meals' not in st.session_state:
        st.session_state.meals = {
            '朝食': [],
            '昼食': [],
            '夕食': []
        }
    
    # 目標値保存用
    if 'target' not in st.session_state:
        st.session_state.target = {
            'cal': 0,
            'p': 0,
            'f': 0,
            'c': 0
        }