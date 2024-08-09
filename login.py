import streamlit as st

if __name__ =='__main__':
    st.header("ĐĂNG NHẬP")
    username = st.text_input("Tên đăng nhập", placeholder="Nhập email")
    password = st.text_input("Mật khẩu", placeholder="Nhập mật khẩu", type = "password")

    if st.button("Đăng nhập"):
        if username == "admin" and password == "123":  # Example credentials
            st.session_state['authenticated'] = True
            st.success("Logged in successfully!")
            st.switch_page(r"pages\app.py")
        else:
            st.error("Invalid username or password")
