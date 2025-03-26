import streamlit as st
import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# 간단한 요약 모델 사용 (Streamlit Cloud에서 잘 작동하는 모델)
model_name = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

st.set_page_config(page_title="AI PDF 제목 생성기", page_icon="📄")
st.title("📄 PDF 자동 제목 생성기")
st.markdown("PDF를 업로드하면 AI가 내용을 요약하고 제목을 제안해줍니다.")

uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("PDF 내용 분석 중..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        preview = text[:1500]  # 모델 입력 길이 제한
        inputs = tokenizer.encode("summarize: " + preview, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=50, min_length=10, length_penalty=2.0, num_beams=4, early_stopping=True)
        title = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        st.success("제목 생성 완료!")
        st.markdown(f"**📌 추천 제목:** {title}")
        st.code(title, language="text")

        # 복사 기능은 Streamlit Cloud에서 제한될 수 있음 (pyperclip 제거)
        st.info("제목을 길게 눌러 복사하거나 수동으로 복사해 주세요.")
