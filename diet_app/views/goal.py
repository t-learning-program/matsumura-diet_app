import streamlit as st
import const

def show():
    """目標設定セクションを表示する関数"""
    st.header(const.SECTION_GOAL)
    
    # 【変更点1】3列にして年齢入力欄を追加
    col1, col2, col3 = st.columns(3)

    with col1:
        height_input = st.text_input(const.LBL_HEIGHT, value="170")
    with col2:
        weight_input = st.text_input(const.LBL_WEIGHT, value="65")
    with col3:
        # 年齢の初期値は30にしておきます
        age_input = st.text_input(const.LBL_AGE, value="30")

    if st.button(const.BTN_CALC):
        # バリデーション処理
        try:
            h = float(height_input)
            w = float(weight_input)
            a = float(age_input) # 【変更点2】年齢の変換

            if h <= 0 or w <= 0 or a <= 0: # 【変更点3】年齢も正の数かチェック
                st.error("全ての項目に正の数を入力してください")
                st.stop()

        except ValueError:
            st.error("全ての項目に半角数字を入力してください")
            st.stop()

        # 計算処理
        # 【変更点4】固定の30ではなく、変数 a (年齢) を使用
        # ハリス・ベネディクト方程式(男性): 66.47 + (13.75 × 体重) + (5.00 × 身長) - (6.75 × 年齢)
        bmr = 66.47 + (13.75 * w) + (5.00 * h) - (6.75 * a)
        
        target_cal = int(bmr * 1.5)
        p_gram = int((target_cal * 0.2) / 4)
        f_gram = int((target_cal * 0.25) / 9)
        c_gram = int((target_cal * 0.55) / 4)

        # 計算結果をセッションステートに保存
        st.session_state.target = {
            'cal': target_cal,
            'p': p_gram,
            'f': f_gram,
            'c': c_gram
        }

        st.success(const.MSG_CALC_SUCCESS.format(target_cal))
        
        m1, m2, m3 = st.columns(3)
        m1.metric("タンパク質 (P)", f"{p_gram} g")
        m2.metric("脂質 (F)", f"{f_gram} g")
        m3.metric("炭水化物 (C)", f"{c_gram} g")
        st.divider()