import streamlit as st
import base64
import google.generativeai as genai
import pptx
from pptx.util import Inches, Pt
import os
import time
import google.api_core.exceptions
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Lấy API Key từ .env
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY không được tìm thấy trong file .env!")
    st.stop()

# Cấu hình Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Định dạng font
TITLE_FONT_SIZE = Pt(30)
SLIDE_FONT_SIZE = Pt(16)

# Hàm gọi API với retry
def call_gemini_api(prompt, retries=5, delay=10):
    """Gọi Gemini API với cơ chế thử lại nếu gặp lỗi quota"""
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except google.api_core.exceptions.ResourceExhausted:
            if attempt < retries - 1:
                st.warning(f"⚠️ API bị giới hạn, chờ {delay}s rồi thử lại ({attempt+1}/{retries})...")
                time.sleep(delay)
            else:
                st.error("🚨 Quá tải API! Hãy thử lại sau hoặc kiểm tra Google Cloud Console.")
                return "Không thể tạo nội dung do giới hạn API."

# Tạo tiêu đề slide
def generate_slide_titles(topic):
    prompt = f"Tạo tiêu đề slide cho chủ đề '{topic}'."
    time.sleep(1)  # Giảm tải API
    return call_gemini_api(prompt)

# Tạo nội dung từng slide
def generate_slide_content(slide_title):
    prompt = f"Tạo nội dung chi tiết cho tiêu đề: '{slide_title}'."
    time.sleep(1)
    return call_gemini_api(prompt)

# Tạo PowerPoint
def create_presentation(topic, slide_titles, slide_contents):
    prs = pptx.Presentation()
    slide_layout = prs.slide_layouts[1]

    # Slide tiêu đề chính
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = topic

    # Các slide nội dung
    for slide_title, slide_content in zip(slide_titles, slide_contents):
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = slide_title
        slide.shapes.placeholders[1].text = slide_content

        # Tùy chỉnh font chữ
        slide.shapes.title.text_frame.paragraphs[0].font.size = TITLE_FONT_SIZE
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_frame = shape.text_frame
                for paragraph in text_frame.paragraphs:
                    paragraph.font.size = SLIDE_FONT_SIZE

    ppt_path = "generated_ppt/presentation.pptx"
    prs.save(ppt_path)
    return ppt_path

# Tạo link tải file PPT
def get_ppt_download_link(ppt_path):
    with open(ppt_path, "rb") as file:
        ppt_contents = file.read()

    b64_ppt = base64.b64encode(ppt_contents).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64_ppt}" download="presentation.pptx">📥 Tải PowerPoint</a>'

# Giao diện Streamlit
def main():
    st.title("🎤 Tạo PowerPoint tự động bằng AI")

    topic = st.text_input("📌 Nhập chủ đề bài thuyết trình:")
    generate_button = st.button("✨ Tạo PowerPoint")

    if generate_button and topic:
        st.info("⏳ Đang tạo bài thuyết trình... Vui lòng chờ.")

        # Gọi API tạo tiêu đề slide
        slide_titles_text = generate_slide_titles(topic)
        slide_titles = [title.strip() for title in slide_titles_text.split("\n") if title.strip()]
        
        if not slide_titles:
            st.error("❌ Không tạo được tiêu đề slide! Hãy thử lại với chủ đề khác.")
            return
        
        # Gọi API tạo nội dung từng slide
        slide_contents = [generate_slide_content(title) for title in slide_titles]

        # Tạo file PowerPoint
        ppt_path = create_presentation(topic, slide_titles, slide_contents)

        st.success("✅ Bài thuyết trình đã tạo thành công!")
        st.markdown(get_ppt_download_link(ppt_path), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
