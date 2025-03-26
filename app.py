import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import pyperclip

# 제목 생성 모델 (HuggingFace 기반 - 무료)
title_gen = pipeline("text2text-generation", model="pszemraj/long-t5-tglobal-base-16384-book-summary")

st.set_page_config(page_title="AI PDF 제목 생성기", page_icon="📄")
st.title("📄 PDF 자동 제목 생성기")
st.markdown("PDF를 업로드하면 AI가 자동으로 내용을 요약하고 제목을 제안해줍니다.")

uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("PDF 내용 분석 중..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        preview = text[:1500]  # 모델 입력 길이 제한
        result = title_gen(f"summarize: {preview}", max_length=50, min_length=10, do_sample=False)
        title = result[0]["generated_text"]

        st.success("제목 생성 완료!")
        st.markdown(f"**📌 추천 제목:** {title}")
        st.code(title, language="text")

        if st.button("📋 제목 복사하기"):
            pyperclip.copy(title)
            st.success("클립보드에 복사되었습니다. 삼성노트에 붙여넣기 하세요!")
