from langchain_community.llms import Ollama
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import requests
import re

llm = Ollama(model="llama3")
title = st.title("챗봇")

stream = None
tab1, tab2 = st.tabs([ "일반", "날씨" ])
with tab1:
    st.header("입력")
    txt = st.text_input("여기에 내용을 입력하세요", value="", placeholder="질문 내용 입력")
    st.header("답변")
    if txt:
        if "날씨" in txt:
            st.warning("날씨에 대한 챗봇의 응답은 정확하지 않을 수 있습니다.\n정확한 현시각 날씨 정보를 원하신다면 [날씨]탭에서 찾을 수 있습니다.", icon="⚠")
        stream = llm.stream(txt, flush=True)
        st.write_stream(stream)
with tab2:
    st.header("입력")
    txt = st.text_input("여기에 지역 이름을 입력하세요", value="", placeholder="지역 이름만 입력")
    if txt:
        root_url = "https://search.naver.com/search.naver?query="
        url = root_url + txt.replace(" ", "+") + "+날씨"
        res = requests.get(url)
        html = BeautifulSoup(res.text, "html.parser")
        w = html.select_one("._cs_weather")
        if w:
            loc = w.select_one(".title_area>h2.title").text
            temp_raw = w.select_one(".temperature_text>strong").text
            temp = ".".join(list(map((lambda x: re.sub(r"\D*", "", x)), temp_raw.split("."))))
            sky = w.select_one(".summary>.before_slash").text
            st.header(f"{loc}: {temp}° {sky}")

            summary = w.select(".summary_list div")
            if summary:
                for i in summary:
                    term = i.select_one(".term").text
                    desc = i.select_one(".desc").text
                    st.write(f"{term} {desc}")

            datas = w.select("li.item_today")
            if datas:
                mise = datas[0].select_one("span.txt").text
                chomise = datas[1].select_one("span.txt").text
                uv = datas[2].select_one("span.txt").text
                sunset = datas[3].select_one("span.txt").text
                df_datas = pd.DataFrame({
                    "미세먼지": [ mise ],
                    "초미세먼지": [ chomise ],
                    "자외선": [ uv ],
                    "일몰": [ sunset ]
                })
                st.dataframe(df_datas, hide_index=True)
        else:
            st.write("날씨를 지원하지 않는 지역이거나 입력값이 올바르지 않습니다!")