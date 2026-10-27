
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="나의 용돈 관리",
    page_icon="💰",
    layout="centered"
)

st.title("💰 나의 용돈 관리")
st.caption("계획적인 소비 습관을 위한 용돈 관리 프로그램")

if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.balance = 0
    st.session_state.income = 0
    st.session_state.expense = 0
    st.session_state.history = []

if not st.session_state.initialized:
    st.subheader("🎉 용돈 설정")
    initial_money = st.number_input(
        "현재 가지고 있는 용돈 (원)",
        min_value=0,
        step=1000,
        value=10000
    )

    if st.button("용돈 설정하기", type="primary"):
        st.session_state.balance = initial_money
        st.session_state.initialized = True
        st.rerun()

else:
    st.subheader("📊 나의 소비 현황")

    c1, c2, c3 = st.columns(3)
    c1.metric("현재 잔액", f"{st.session_state.balance:,}원")
    c2.metric("총수입", f"{st.session_state.income:,}원")
    c3.metric("총지출", f"{st.session_state.expense:,}원")

    st.divider()
    st.subheader("✏️ 수입 및 지출 기록")

    category = st.selectbox(
        "거래 종류",
        ["수입", "지출"]
    )

    amount = st.number_input(
        "금액 (원)",
        min_value=0,
        step=1000,
        value=1000
    )

    memo = st.text_input(
        "내용",
        placeholder="예: 부모님께 받은 용돈, 간식 구매"
    )

    if st.button("기록하기", type="primary"):
        if amount <= 0:
            st.error("0원보다 큰 금액을 입력하세요.")
        elif category == "지출" and amount > st.session_state.balance:
            st.error("잔액이 부족합니다.")
        else:
            if category == "수입":
                st.session_state.balance += amount
                st.session_state.income += amount
            else:
                st.session_state.balance -= amount
                st.session_state.expense += amount

            st.session_state.history.insert(0, {
                "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "종류": category,
                "내용": memo if memo else category,
                "금액": amount
            })

            st.success("기록이 완료되었습니다!")
            st.rerun()

    st.divider()
    st.subheader("📋 거래 내역")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        df["금액"] = df["금액"].map(lambda x: f"{x:,}원")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("아직 기록된 거래 내역이 없습니다.")

    if st.button("처음부터 다시 설정"):
        st.session_state.clear()
        st.rerun()

st.caption("나의 용돈 관리 프로그램 | Python · Streamlit")

