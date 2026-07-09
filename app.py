import streamlit as st
import pandas as pd
from datetime import datetime

# ======================================
# CẤU HÌNH TRANG
# ======================================
st.set_page_config(
    page_title="Quản lý tiền phòng trọ",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 PHẦN MỀM QUẢN LÝ THU TIỀN DÃY TRỌ_VŨ ĐỨC BÌNH")

# ======================================
# SIDEBAR - ĐƠN GIÁ & CẤU HÌNH
# ======================================
st.sidebar.header("⚙️ ĐƠN GIÁ ĐIỆN NƯỚC")

gia_dien = st.sidebar.number_input(
    "⚡ Giá điện (đ/kWh)",
    min_value=0,
    value=3500,
    step=100
)

gia_nuoc = st.sidebar.number_input(
    "💧 Giá nước (đ/m³)",
    min_value=0,
    value=15000,
    step=500
)

phi_khac = st.sidebar.number_input(
    "📦 Phí khác (wifi, vệ sinh...)",
    min_value=0,
    value=150000,
    step=10000
)

so_phong = st.sidebar.slider(
    "Số lượng phòng",
    min_value=1,
    max_value=100,
    value=10,
    step=1
)

# ======================================
# CẢI TIẾN: CHỌN NĂM VÀ THÁNG RIÊNG BIỆT
# ======================================
st.sidebar.markdown("---")
st.sidebar.header("📅 THỜI GIAN LÀM VIỆC")

# Cấu hình danh sách năm (Cho phép chọn từ 3 năm trước đến 2 năm sau năm hiện tại)
nam_hien_tai = datetime.now().year
danh_sach_nam = list(range(nam_hien_tai - 3, nam_hien_tai + 3))
nam_chon = st.sidebar.selectbox(
    "Chọn năm:",
    danh_sach_nam,
    index=danh_sach_nam.index(nam_hien_tai)
)

# Cấu hình danh sách 12 tháng
thang_hien_tai = datetime.now().month
danh_sach_thang = list(range(1, 13))
idx_thang_chon = st.sidebar.selectbox(
    "Chọn tháng:",
    danh_sach_thang,
    index=thang_hien_tai - 1,
    format_func=lambda x: f"Tháng {x}"
)

thang_chon_str = f"Tháng {idx_thang_chon}/{nam_chon}"

# ======================================
# KHỞI TẠO & ĐỒNG BỘ DỮ LIỆU ĐA TẦNG (NĂM -> THÁNG)
# ======================================
if "phong_data_theo_thang" not in st.session_state:
    st.session_state.phong_data_theo_thang = {}

# Cấu hình cây dữ liệu cho Năm -> Tháng nếu chưa tồn tại
if nam_chon not in st.session_state.phong_data_theo_thang:
    st.session_state.phong_data_theo_thang[nam_chon] = {}

if idx_thang_chon not in st.session_state.phong_data_theo_thang[nam_chon]:
    st.session_state.phong_data_theo_thang[nam_chon][idx_thang_chon] = {}

for i in range(1, so_phong + 1):
    if i not in st.session_state.phong_data_theo_thang[nam_chon][idx_thang_chon]:
        
        # LOGIC TỰ ĐỘNG KẾ THỪA SỐ CŨ TỪ THÁNG TRƯỚC
        dien_cu_mac_dinh = 0
        nuoc_cu_mac_dinh = 0
        
        # Xác định tháng trước và năm trước phòng trường hợp là Tháng 1
        if idx_thang_chon == 1:
            thang_truoc = 12
            nam_truoc = nam_chon - 1
        else:
            thang_truoc = idx_thang_chon - 1
            nam_vor = nam_chon  # Giữ nguyên năm hiện tại
            nam_truoc = nam_chon

        # Truy vết dữ liệu tháng trước để lấy số mới làm số cũ tháng này
        if nam_truoc in st.session_state.phong_data_theo_thang:
            if thang_truoc in st.session_state.phong_data_theo_thang[nam_truoc]:
                if i in st.session_state.phong_data_theo_thang[nam_truoc][thang_truoc]:
                    thang_truoc_data = st.session_state.phong_data_theo_thang[nam_truoc][thang_truoc][i]
                    dien_cu_mac_dinh = thang_truoc_data.get("dien_moi", 0)
                    nuoc_cu_mac_dinh = thang_truoc_data.get("nuoc_moi", 0)

        st.session_state.phong_data_theo_thang[nam_chon][idx_thang_chon][i] = {
            "gia_phong": 2500000,
            "dien_cu": dien_cu_mac_dinh,
            "dien_moi": dien_cu_mac_dinh, 
            "nuoc_cu": nuoc_cu_mac_dinh,
            "nuoc_moi": nuoc_cu_mac_dinh, 
            "ghi_chu": ""
        }

# ======================================
# GIAO DIỆN NHẬP DỮ LIỆU
# ======================================
st.header(f"📋 Nhập số liệu - {thang_chon_str}")

phong = st.selectbox(
    "Chọn phòng cần nhập dữ liệu:",
    range(1, so_phong + 1),
    key=f"selectbox_phong_{nam_chon}_{idx_thang_chon}" 
)

# Lấy dữ liệu của phòng thuộc đúng Năm và Tháng đang chọn
data = st.session_state.phong_data_theo_thang[nam_chon][idx_thang_chon][phong]

st.subheader(f"🏠 Cập nhật: Phòng {phong} ({thang_chon_str})")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    data["gia_phong"] = st.number_input(
        "Giá phòng (VNĐ)",
        min_value=0,
        value=int(data["gia_phong"]),
        step=50000,
        key=f"gia_{nam_chon}_{idx_thang_chon}_{phong}"
    )

with c2:
    data["dien_cu"] = st.number_input(
        "Số điện CŨ",
        min_value=0,
        value=int(data["dien_cu"]),
        key=f"diencu_{nam_chon}_{idx_thang_chon}_{phong}"
    )

with c3:
    data["dien_moi"] = st.number_input(
        "Số điện MỚI",
        min_value=0,
        value=int(data["dien_moi"]),
        key=f"dienmoi_{nam_chon}_{idx_thang_chon}_{phong}"
    )

with c4:
    data["nuoc_cu"] = st.number_input(
        "Số nước CŨ",
        min_value=0,
        value=int(data["nuoc_cu"]),
        key=f"nuoccu_{nam_chon}_{idx_thang_chon}_{phong}"
    )

with c5:
    data["nuoc_moi"] = st.number_input(
        "Số nước MỚI",
        min_value=0,
        value=int(data["nuoc_moi"]),
        key=f"nuocmoi_{nam_chon}_{idx_thang_chon}_{phong}"
    )

data["ghi_chu"] = st.text_input(
    "📝 Ghi chú (Ví dụ: Đã thanh toán, chưa thanh toán...)",
    value=data["ghi_chu"],
    key=f"ghichu_{nam_chon}_{idx_thang_chon}_{phong}"
)

# Lưu dữ liệu trở lại bộ nhớ session_state
st.session_state.phong_data_theo_thang[nam_chon][idx_thang_chon][phong] = data

# ĐỒNG BỘ: Nếu đổi số mới ở tháng này, cập nhật ngay lập tức vào số cũ của tháng kế tiếp
if idx_thang_chon == 12:
    thang_sau = 1
    nam_sau = nam_chon + 1
else:
    thang_sau = idx_thang_chon + 1
    nam_sau = nam_chon

if nam_sau in st.session_state.phong_data_theo_thang:
    if thang_sau in st.session_state.phong_data_theo_thang[nam_sau]:
        if phong in st.session_state.phong_data_theo_thang[nam_sau][thang_sau]:
            st.session_state.phong_data_theo_thang[nam_sau][thang_sau][phong]["dien_cu"] = data["dien_moi"]
            st.session_state.phong_data_theo_thang[nam_sau]
