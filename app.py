import streamlit as st
from groq import Groq
from PIL import Image

# Tiêu đề ứng dụng
st.title("🤖 Trợ lý AI Cá nhân (Powered by Groq)")

# 1. Ô nhập Groq API Key
api_key = st.text_input("Nhập Groq API Key của bạn:", type="password")

if not api_key:
    st.warning("⚠️ Vui lòng nhập Groq API Key ở ô phía trên để bắt đầu sử dụng.")
else:
    # Khởi tạo client kết nối Groq với API Key người dùng vừa nhập
    client = Groq(api_key=api_key)

    # Khởi tạo lịch sử chat trong bộ nhớ tạm
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị lại các tin nhắn cũ trên giao diện
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ô nhập tin nhắn chat ở dưới cùng
    if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu của bạn..."):
        # Hiển thị tin nhắn của người dùng lên giao diện
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lưu tin nhắn người dùng vào lịch sử
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gửi yêu cầu đến mô hình siêu tốc của Groq
        with st.spinner("Groq đang xử lý tốc độ cao..."):
            try:
                # Gọi API chuẩn của Groq (Sử dụng mô hình Llama 3.3 70B cực mạnh và thông minh)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ]
                )
                
                response_text = completion.choices[0].message.content

                # Hiển thị câu trả lời của AI lên giao diện
                with st.chat_message("assistant"):
                    st.markdown(response_text)
                    
                # Lưu câu trả lời vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Đã xảy ra lỗi từ Groq: {e}")
