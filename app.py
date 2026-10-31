import streamlit as st
from google import genai
from PIL import Image

# Tiêu đề ứng dụng
st.title("🤖 Trợ lý AI Cá nhân của Tài")

# 1. Tạo ô nhập API Key bảo mật
api_key = st.text_input("Nhập Google API Key của bạn:", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập Google API Key ở ô phía trên để bắt đầu sử dụng trợ lý.")
else:
    # Khởi tạo client kết nối Gemini với API Key người dùng vừa nhập
    client = genai.Client(api_key=api_key)

    # Khởi tạo bộ nhớ tạm lưu lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị lại lịch sử các tin nhắn cũ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Tùy chọn tải ảnh lên nếu muốn hỏi về hình ảnh
    uploaded_file = st.file_uploader("Tải ảnh lên (Không bắt buộc):", type=["jpg", "jpeg", "png"])

    # Ô nhập tin nhắn chat ở dưới cùng
    if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu của bạn..."):
        content_to_send = [prompt]
        
        # Hiển thị tin nhắn người dùng lên giao diện
        with st.chat_message("user"):
            st.markdown(prompt)
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Ảnh đính kèm", use_column_width=True)
                content_to_send.append(image)

        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gửi yêu cầu đến mô hình Gemini Flash
        with st.spinner("Trợ lý đang suy nghĩ..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=content_to_send,
                )
                # Hiển thị câu trả lời của AI
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Đã xảy ra lỗi hoặc chạm giới hạn: {e}")
