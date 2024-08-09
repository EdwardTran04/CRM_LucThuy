import streamlit as st
import requests

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.error("You are not logged in.")
    st.stop()

# Phần "Thông tin người lập đơn"
st.header("Thông tin người lập đơn")

# Dropdown để chọn tên đăng nhập
login_name = st.selectbox("Chọn tên đăng nhập", ["User1", "User2", "User3"])
if not login_name:
    st.warning("Vui lòng chọn tên đăng nhập")

# Phần "Thông tin khách hàng"
st.header("Thông tin khách hàng")

# Lựa chọn khách hàng
customer_option = st.radio("Lựa chọn khách hàng", ["Thêm mới", "Chọn từ danh sách"])

# Nếu thêm mới, yêu cầu nhập thông tin
if customer_option == "Thêm mới":
    customer_name = st.text_input("Tên khách hàng", placeholder="Nhập tên khách hàng...")
    customer_phone = st.text_input("Số điện thoại", placeholder="Nhập số điện thoại (VD: 081622)")
    customer_source = st.selectbox("Nguồn khách hàng", ["FB Mới", "Zalo", "Google", "Khác"])
    customer_note = st.text_area("Ghi chú", placeholder="Nhập ghi chú nếu có (ghi chú về khách hàng)")
    
    # Thông báo thêm mới
    if st.button("Lưu đơn hàng"):
        st.info("Thông tin khách hàng sẽ được thêm mới khi bạn lưu đơn hàng!")
else:
    # Nếu chọn từ danh sách, hiển thị danh sách
    customer_list = st.selectbox("Chọn khách hàng từ danh sách", ["Khách hàng A", "Khách hàng B", "Khách hàng C"])


# Phần "Thông tin đơn hàng"
st.header("Thông tin đơn hàng")

# Hình thức đơn hàng, Hình thức thanh toán, Tình trạng cọc
order_type = st.selectbox("Hình thức đơn hàng", ["Vật tư", "Dịch vụ", "Khác"])
payment_method = st.selectbox("Hình thức thanh toán", ["Thanh toán trước", "Thanh toán sau", "Trả góp"])
deposit_status = st.selectbox("Tình trạng cọc", ["Chưa cọc", "Đã cọc", "Cọc một phần"])

# Nút thêm sản phẩm
if st.button("Thêm sản phẩm"):
    st.warning("Chức năng thêm sản phẩm chưa hoàn thiện, do có sản phẩm tính theo m2 *1,03 chỗ này cần phải thảo luận lại!!!")

# Thông báo đơn hàng trống
st.warning("Đơn hàng trống. Vui lòng thêm sản phẩm.")

# Xóa toàn bộ sản phẩm
if st.button("Xóa toàn bộ sản phẩm"):
    st.info("Nhưng yên tâm, khi dữ liệu lưu ở table 4. Quản lý hợp đồng chi tiết sẽ chuẩn không lệch số nhé.")

# Phần "Tổng tiền"
st.header("Tổng tiền: 0 VNĐ")

# Các khoản chi phí
col1, col2, col3, col4 = st.columns(4)
with col1:
    deposit = st.number_input("Tiền cọc", min_value=0, step=1)
with col2:
    labor_fee = st.number_input("Phí công thợ", min_value=0, step=1)
with col3:
    transport_fee = st.number_input("Phí vận chuyển", min_value=0, step=1)
with col4:
    surcharge = st.number_input("Phụ thu", min_value=0, step=1)

# Thời gian yêu cầu thực hiện đơn hàng, Số m2 yêu cầu gửi & Yêu cầu khác từ khách
col5, col6 = st.columns(2)
with col5:
    request_date = st.date_input("Thời gian yêu cầu thực hiện đơn hàng")
with col6:
    area_requested = st.text_input("Số m2 yêu cầu gửi & Yêu cầu khác từ khách", placeholder="Nhập dạng số vd: 26")

# Upload files
uploaded_files = st.file_uploader("Upload SƠ ĐỒ NHÀ KHÁCH & hình ảnh mặt bằng (nếu đơn hoàn thiện)", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

# Hiển thị các file đã upload
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"File uploaded: {uploaded_file.name}")

# Phần "Địa chỉ đơn hàng"
st.header("Địa chỉ đơn hàng")

# Chọn tỉnh/thành phố
city = st.selectbox("Chọn tỉnh/thành phố", ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Khác"])

# Địa chỉ chi tiết
address_detail = st.text_input("Địa chỉ chi tiết", placeholder="Nhập số nhà, tên đường...")
if not address_detail:
    st.warning("Vui lòng nhập chi tiết địa chỉ của khách!")

# Ghi chú
note = st.text_area("Ghi chú", placeholder="Yêu cầu thêm của khách hàng, ghi chú,... nhập vào đây!")

def send_data_to_lark_base(city, address_detail, note):
    # Thay thế API_ENDPOINT, API_KEY, và TABLE_ID với thông tin của bạn
    API_ENDPOINT = "https://api.larksuite.com/open-apis/bitable/v1/apps/APP_ID/tables/TABLE_ID/records"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "City": city,
            "AddressDetail": address_detail,
            "Note": note
        }
    }
    
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    
    return response.status_code, response.json()

# Nút "Lưu đơn hàng" và "Đăng xuất"
col1, col2 = st.columns(2)
with col1:
    if st.button("Lưu"):
        st.success("Đơn hàng đã được lưu!")
   
        status_code, response_data = send_data_to_lark_base(city, address_detail, note)
        if status_code == 200:
            st.success("Đơn hàng đã được lưu thành công!")
        else:
            st.error(f"Lỗi khi lưu đơn hàng: {response_data}")

with col2:
    if st.button("Đăng xuất"):
        st.write("Bạn đã đăng xuất!")



def send_data_to_lark_base(city, address_detail, note):
    # Thay thế API_ENDPOINT, API_KEY, và TABLE_ID với thông tin của bạn
    API_ENDPOINT = "https://api.larksuite.com/open-apis/bitable/v1/apps/APP_ID/tables/TABLE_ID/records"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "City": city,
            "AddressDetail": address_detail,
            "Note": note
        }
    }
    
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    
    return response.status_code, response.json()
