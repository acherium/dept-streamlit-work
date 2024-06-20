import streamlit as st
import pandas as pd
import math

file_path = r"./cafe.xlsx"
df = pd.read_excel(file_path)

df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
sal_tot = df["price"].sum()

title = st.title("카페 매출 대시보드")
tab1, tab2, tab3, tab4 = st.tabs([ "대시보드", "연간 매출", "월간 매출", "월간 제품 매출" ])
with tab1:
    st.header(f"전체 기간 매출 총액: {sal_tot:,}원")
    col1, col2 = st.columns(2)
    with col1:
        df_byyear = df.groupby("year")["price"].sum().reset_index()
        st.subheader(f"연간 매출 데이터")
        st.bar_chart(df_byyear.set_index("year"))
    with col2:
        df_bymonth = df.groupby("month")["price"].sum().reset_index()
        st.subheader(f"월간 매출 데이터")
        st.bar_chart(df_bymonth.set_index("month"))
    st.subheader("주문 내역")
    t1_tgl_sort = st.toggle("최근순 정렬", value=True, key="t1_tgl_sort")
    if t1_tgl_sort:
        st.dataframe(df.sort_values("order_date", ascending=False), use_container_width=True)
    else:
        st.dataframe(df.sort_values("order_date"), use_container_width=True)
with tab2:
    df_filtered = df.groupby("year")["price"].sum().reset_index()
    st.header(f"연간 매출 데이터")
    st.bar_chart(df_filtered.set_index("year"))
    st.dataframe(df_filtered.set_index("year"), use_container_width=True)
    tip = st.expander("도표 항목 설명")
    tip.write("- year: 연도\n" +
              "- price: 당해 매출총액\n")
with tab3:
    t3_sel_type = st.selectbox("기간", [ "전체 연도 총합", "연도별" ])
    if t3_sel_type == "전체 연도 총합":
        df_filtered = df.groupby("month")["price"].sum().reset_index()
        st.header(f"월간 매출 데이터")
        st.bar_chart(df_filtered.set_index("month"))
        st.dataframe(df_filtered.set_index("month"), use_container_width=True)
    elif t3_sel_type == "연도별":
        t4_sel_year = st.selectbox("연도 선택", map((lambda x: int(x)), filter((lambda x: not math.isnan(x)), sorted(df["year"].unique()))), key="0")
        df_filtered = df[df["year"] == t4_sel_year]
        sal_yearly = df_filtered.groupby("month")["price"].sum().reset_index()
        st.header(f"{t4_sel_year}년 월별 매출 데이터")
        st.bar_chart(sal_yearly.set_index("month"))
        st.subheader(f"{t4_sel_year}년 주문 내역")
        t3b_tgl_sort = st.toggle("최근순 정렬", value=True, key="t3b_tgl_sort")
        if t3b_tgl_sort:
            st.dataframe(df_filtered.sort_values("order_date", ascending=False), use_container_width=True)
        else:
            st.dataframe(df_filtered.sort_values("order_date"), use_container_width=True)
    tip = st.expander("도표 항목 설명")
    tip.write("- order_id: 주문 번호\n" +
              "- order_date: 주문일자\n" +
              "- category: 제품 카테고리\n" +
              "- item: 주문한 제품\n" +
              "- price: 제품 가격\n" +
              "- year: 주문일자(연도)\n" +
              "- month: 주문일자(월)\n")
with tab4:
    t5_sel_year = st.selectbox("연도 선택", map((lambda x: int(x)), filter((lambda x: not math.isnan(x)), sorted(df["year"].unique()))), key="1")
    sel_prod = st.selectbox("제품 선택", sorted(df["item"].unique()))
    df_filtered = df[(df["year"] == t5_sel_year) & (df["item"] == sel_prod)]
    sal_monthly = df_filtered.groupby("month")["price"].sum().reset_index()
    st.header(f"{t5_sel_year}년 월별 [{sel_prod}] 매출 데이터")
    st.bar_chart(sal_monthly.set_index("month"))
    st.subheader(f"[{sel_prod}]의 {t5_sel_year}년 주문 내역")
    t2_tgl_sort = st.toggle("최근순 정렬", value=True, key="t2_tgl_sort")
    if t2_tgl_sort:
        st.dataframe(df_filtered.sort_values("order_date", ascending=False), use_container_width=True)
    else:
        st.dataframe(df_filtered.sort_values("order_date"), use_container_width=True)
    tip = st.expander("도표 항목 설명")
    tip.write("- order_id: 주문 번호\n" +
              "- order_date: 주문일자\n" +
              "- category: 제품 카테고리\n" +
              "- item: 주문한 제품\n" +
              "- price: 제품 가격\n" +
              "- year: 주문일자(연도)\n" +
              "- month: 주문일자(월)\n")
