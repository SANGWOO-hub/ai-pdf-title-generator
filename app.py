import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="AI PDF 제목 생성기", page_icon="📄")
st.title("📄 PDF 자동 제목 생성기")
st.markdown("PDF를 업로드하면 AI가 내용을 요약하고 제목을 제안해줍니다.")

# 사용자에게 OpenAI API 키 입력 받기
openai_api_key = st.text_input("🔑 OpenAI API 키 입력", type="password")

uploaded_file = st.file_uploader("📄 PDF 파일 업로드", type=["pdf"])

if openai_api_key and uploaded_file is not None:
    with st.spinner("PDF 내용 분석 중..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        preview = text[:1500]  # 너무 길면 모델 입력 초과

        try:
            openai.api_key = openai_api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 문서 내용을 요약하고, 적절한 제목을 붙이는 AI 비서입니다."},
                    {"role": "user", "content": f"다음 PDF 내용을 보고, 간결하고 적절한 제목을 하나만 만들어줘:\n\n{preview}"}
                ]
            )
            title = response.choices[0].message.content.strip()

            st.success("제목 생성 완료!")
            st.markdown(f"**📌 추천 제목:** {title}")
            st.code(title, language="text")
            st.info("제목을 길게 눌러 복사하거나 수동으로 복사해 주세요.")
        except Exception as e:
            st.error(f"❌ 오류 발생: {str(e)}")

elif uploaded_file and not openai_api_key:
    st.warning("🔑 OpenAI API 키를 먼저 입력해 주세요.")
