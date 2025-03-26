import streamlit as st
import PyPDF2
from openai import OpenAI
from io import BytesIO

# OpenAI API 키 입력 (본인의 키로 바꿔주세요)
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="삼성노트 AI제목생성기", layout="centered")
st.title("📄 삼성노트 AI제목생성기")
st.write("PDF 파일을 업로드하면 AI가 내용을 분석해 자동으로 제목을 지어드립니다.")

uploaded_file = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages[:3]:  # 앞 3페이지만 읽기
        text += page.extract_text()
    return text

def generate_title(text):
    prompt = f"다음 문서 내용을 바탕으로 간결하고 직관적인 제목을 지어줘:\n\n{text}\n\n제목:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=30
    )
    title = response.choices[0].message.content.strip().replace(":", "").replace("?", "")
    return title

if uploaded_file:
    with st.spinner("제목을 생성 중입니다..."):
        text = extract_text_from_pdf(uploaded_file)
        title = generate_title(text)

        # 새 이름으로 저장
        uploaded_file.seek(0)  # 파일 처음으로 이동
        new_pdf = BytesIO(uploaded_file.read())
        st.success(f"📌 추천 제목: **{title}**")
        st.download_button(
            label="📥 제목이 적용된 PDF 다운로드",
            data=new_pdf,
            file_name=f"{title}.pdf",
            mime="application/pdf"
        )
