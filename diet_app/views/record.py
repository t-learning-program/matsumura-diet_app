import streamlit as st
import const

def show():
    "食事記録セクションを表示する関数"
    
    # タイトルの横にボタンを置くレイアウト
    col_header, col_btn = st.columns([3, 2])
    with col_header:
        st.header(const.SECTION_RECORD)
    with col_btn:
        # 下に余白を入れて位置調整
        st.write("") 
        calc_btn = st.button(const.BTN_CALC_RESULT, type="primary")

    # タブ表示
    tab1, tab2, tab3 = st.tabs(["☀️ 朝食", "🌤 昼食", "🌙 夕食"])
    with tab1: render_meal_tab("朝食")
    with tab2: render_meal_tab("昼食")
    with tab3: render_meal_tab("夕食")

    # --- 計算ボタンが押されたときの処理 ---
    if calc_btn:
        calculate_and_show_result()

def render_meal_tab(meal_type):
    st.subheader(f"{meal_type}の記録")
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        name = st.text_input(const.LBL_FOOD_NAME, key=f"name_{meal_type}")
    with c2:
        # プレースホルダーで数字入力を促す
        amount = st.text_input("量(g) ※数字のみ", key=f"amount_{meal_type}")
    with c3:
        st.write("") 
        st.write("")
        add_btn = st.button(const.BTN_ADD, key=f"btn_{meal_type}")

    if add_btn and name:
        st.session_state.meals[meal_type].append({"name": name, "amount": amount})
        st.rerun()

    if st.session_state.meals[meal_type]:
        st.markdown(const.MSG_RECORD_LIST)
        for i, item in enumerate(st.session_state.meals[meal_type]):
            row1, row2 = st.columns([4, 1])
            row1.text(f"・{item['name']} ({item['amount']}g)") # gを表示
            if row2.button(const.BTN_DELETE, key=f"del_{meal_type}_{i}"):
                st.session_state.meals[meal_type].pop(i)
                st.rerun()
    else:
        st.info(const.MSG_NO_RECORD)

def calculate_and_show_result():
    """1日の合計を計算して表示するロジック"""
    st.divider()
    st.markdown(const.MSG_RESULT_TITLE)

    # 目標値が計算されているかチェック
    targets = st.session_state.target
    if targets['cal'] == 0:
        st.warning("先に「1. 目標設定」で目標を計算してください！")
        return

    total = {'cal': 0, 'p': 0, 'f': 0, 'c': 0}
    unknown_foods = [] # 辞書になかった食材リスト

    # 全ての食事（朝・昼・夕）をループして計算
    for meal_type in ['朝食', '昼食', '夕食']:
        for item in st.session_state.meals[meal_type]:
            food_name = item['name']
            
            # 辞書にあるかチェック
            if food_name in const.FOOD_DATABASE:
                try:
                    # 量を数値に変換（入力が数字であることを期待）
                    grams = float(item['amount'])
                    # 100gあたりのデータなので調整
                    ratio = grams / 100.0
                    
                    data = const.FOOD_DATABASE[food_name]
                    total['cal'] += data['kcal'] * ratio
                    total['p'] += data['p'] * ratio
                    total['f'] += data['f'] * ratio
                    total['c'] += data['c'] * ratio
                except ValueError:
                    # 量が数字じゃなかった場合などは無視
                    pass
            else:
                unknown_foods.append(food_name)

    # 結果表示エリア（4列）
    cols = st.columns(4)
    labels = ["カロリー", "タンパク質(P)", "脂質(F)", "炭水化物(C)"]
    keys = ['cal', 'p', 'f', 'c']
    units = ["kcal", "g", "g", "g"]

    is_all_clear = True # 全クリアフラグ

    for i, col in enumerate(cols):
        key = keys[i]
        val = int(total[key])     # 実績
        tgt = int(targets[key])   # 目標
        
        # 目標との差分
        diff = val - tgt
        
        # メトリクス表示 (delta_color="inverse" で、プラスだと赤字になる)
        col.metric(
            label=labels[i],
            value=f"{val} {units[i]}",
            delta=f"{diff} (目標: {tgt})",
            delta_color="inverse" 
        )

        # オーバー判定のメッセージ作成
        if val > tgt:
            is_all_clear = False
            st.error(const.MSG_OVER.format(labels[i], f"{diff}{units[i]}"))

    # 全クリアの場合
    if is_all_clear:
        st.success(const.MSG_CLEAR)

    # 辞書になかった食材があれば通知
    if unknown_foods:
        # 重複を除去して表示
        unique_unknowns = list(set(unknown_foods))
        st.caption(const.MSG_UNKNOWN_FOOD.format(", ".join(unique_unknowns)))