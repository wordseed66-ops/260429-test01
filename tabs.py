import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="centered")

# 샘플 데이터
chart_data = pd.DataFrame({
    "Month": ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
    "Sales": [4300, 4500, 2800, 3600, 3750, 2700, 1800, 2650, 1850, 1300, 4900, 2050]
})

table_data = pd.DataFrame({
    "거래내역": ["INV001", "INV002", "INV003", "INV004", "INV005"],
    "결제": ["수금", "미수금", "수금", "미수금", "수금"],
    "총액": [500, 200, 150, 350, 400],
    "지불방법": ["신용카드", "현금", "체크카드", "신용카드", "무통장입금"]
})

with st.container(border=True):
    
    # 타이틀
    st.title("운영 현황")

    st.write("")  # 간격

    # 내부 카드 3개
    col1, col2, col3 = st.columns(3, gap="large")

    # 카드 1
    with col1:
        with st.container(border=True):
            st.caption("매출 합계")
            st.metric(
                label=" ",
                value="45,231",
                delta="+20.1%"
            )

    # 카드 2
    with col2:
        with st.container(border=True):
            st.caption("회원 가입")
            st.metric(
                label=" ",
                value="+235",
                delta="-1.21%"
            )

    # 카드 3
    with col3:
        with st.container(border=True):
            st.caption("판매 수익")
            st.metric(
                label=" ",
                value="+12,234",
                delta="+19%"
            )


st.write("")
st.header("매출 현황")

# 하단 차트 컨테이너
tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "📈 Line Chart", "📉 Area Chart"])

# --- Bar Chart ---
with tab1:
    with st.container(border=True):
        bar_chart = (
            alt.Chart(chart_data)
            .mark_bar(color="#0051FF", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Month:N", sort=None),
                y="Sales:Q"
            )
            .properties(height=350)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(bar_chart, width='stretch')

# --- Line Chart ---
with tab2:
    with st.container(border=True):
        line_chart = (
            alt.Chart(chart_data)
            .mark_line(color="#0051FF", point=True)
            .encode(
                x=alt.X("Month:N", sort=None),
                y="Sales:Q"
            )
            .properties(height=350)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(line_chart, width='stretch')

# --- Area Chart ---
with tab3:
    with st.container(border=True):
        area_chart = (
            alt.Chart(chart_data)
            .mark_area(color="#0051FF", opacity=0.5)
            .encode(
                x=alt.X("Month:N", sort=None),
                y="Sales:Q"
            )
            .properties(height=350)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(area_chart, width='stretch')

# table_data
# -------------------------
# 상단: 읽기 전용
# -------------------------
st.subheader("📋 거래내역 (Read Only)")

with st.container(border=True):
    st.dataframe(
        table_data,
        width='stretch',
        hide_index=False
    )

st.write("")  # 간격

# -------------------------
# 하단: Editable
# -------------------------
st.subheader("✏️ 거래내역 (Editable)")

with st.container(border=True):
    edited_df = st.data_editor(
        table_data,
        width='stretch',
        hide_index=True,
        num_rows="dynamic",
        column_config={
            # "거래내역": st.column_config.TextColumn(
            #     "거래내역",
            #     disabled=True
            # ),
            "결제": st.column_config.SelectboxColumn(
                "결제",
                options=["수금", "미수금"],
                required=True
            ),
            "총액": st.column_config.NumberColumn(
                "총액",
                min_value=0,
                max_value=1000,
                step=50,
                required=True
            ),
            "지불방법": st.column_config.SelectboxColumn(
                "지불방법",
                options=["신용카드", "현금", "체크카드", "무통장입금"],
                required=True
            )
        }
    )


# -------------------------
# Popup 창 데코레이터
# -------------------------
@st.dialog("의견을 말씀해주세요.")
def vote(item):
    st.write(f"{item} 하는 이유는 무엇입니까?")
    reason = st.text_input("그 이유는...")

    if st.button("제출"):
        st.session_state.vote = {
            "item": item,
            "reason": reason
        }
        st.rerun()


col1, col2 = st.columns(2, gap="large")

# 왼쪽 컬럼: 라디오 버튼
with col1:
    with st.container(border=True):
        st.subheader("지불 방법 선택")

        pay = st.radio(
            "지불 방법을 선택하세요",
            ["신용카드", "현금", "체크카드"],
            captions=[
                "국민/신한/우리",
                "현금영수증",
                "농협/신협",
            ],
        )

        if pay == "신용카드":
            st.success("수수료 면제")
        elif pay == "현금":
            st.info("현금 영수증")
        else:
            st.warning("5% 할인")


# 오른쪽 컬럼: 다이얼로그 버튼
with col2:
    with st.container(border=True):
        st.subheader("찬/반 투표")

        if "vote" not in st.session_state:
            st.write("찬/반 투표에 참여해주세요.")

            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                if st.button("찬성", width='stretch'):
                    vote("찬성")

            with btn_col2:
                if st.button("반대", width='stretch'):
                    vote("반대")

        else:
            st.success(
                f"{st.session_state.vote['item']} 하시는 이유는 "
                f"'{st.session_state.vote['reason']}' 입니다"
            )

            if st.button("다시 투표하기"):
                del st.session_state.vote
                st.rerun()


with st.container(border=True):
    col1, col2 = st.columns([1, 20])

    with col1:
        st.write("⚠️")

    with col2:
        st.markdown("**서두르세요!**")
        st.write("주말 넷플릭스 주도권을 룸메에게 뺏겨서야 되겠습니까?")


videos = {
    "멜로": "https://www.youtube.com/watch?v=0pdqf4P9MB8",
    "미스터리": "https://www.youtube.com/watch?v=YoHD9XEInc0",
    "스릴러": "https://www.youtube.com/watch?v=6hB3S9bIaco",
    "액션": "https://www.youtube.com/watch?v=TcMBFSGVi1c",
}

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = "멜로"

genres = ["멜로", "미스터리", "스릴러", "액션"]
cols = st.columns(4)

for col, genre in zip(cols, genres):
    with col:
        if st.button(
            genre,
            width='stretch',
            key=f"btn_{genre}"
        ):
            st.session_state.selected_genre = genre

st.write("")

selected = st.session_state.selected_genre

st.write(f"현재 선택된 장르: {selected}")
st.video(videos[selected])

titles = ['멜로', '미스터리', '스릴러', '액션']
contents = ['주말엔 무조건 멜로 정주행이지',
            '한번 미스터리에 빠지면 못 헤어나와요', 
            '어제 다 못 본 그장면에서 다시 봐야지', 
            '스트레스를 시원하게 날려버려요!']

for title, content in zip(titles, contents):
    with st.expander(title):
        st.write(content)
