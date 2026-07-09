import streamlit as st
import pandas as pd

# ======================================
# CẤU HÌNH
# ======================================

st.set_page_config(
    page_title="Quản lý tiền phòng trọ",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 HỆ THỐNG QUẢN LÝ TIỀN DÃY PHÒNG TRỌ")

# ======================================
# SIDEBAR
# ======================================

st.sidebar.header("⚙️ ĐƠN GIÁ")

gia_dien = st.sidebar.number_input(
    "⚡ Giá điện",
    min_value=0,
    value=3500,
    step=100
)

gia_nuoc = st.sidebar.number_input(
    "💧 Giá nước",
    min_value=0,
    value=15000,
    step=500
)

phi_khac = st.sidebar.number_input(
    "📦 Phí khác",
    min_value=0,
    value=150000,
    step=10000
)

so_phong = st.sidebar.slider(
    "Số phòng",
    min_value=1,
    max_value=100,
    value=10,
    step=1
)

# ======================================
# KHỞI TẠO DỮ LIỆU
# ======================================

if "phong_data" not in st.session_state:
    st.session_state.phong_data = {}

# Tạo dữ liệu cho các phòng chưa có
for i in range(1, so_phong + 1):
    if i not in st.session_state.phong_data:
        st.session_state.phong_data[i] = {
            "gia_phong": 2500000,
            "dien_cu": 0,
            "dien_moi": 0,
            "nuoc_cu": 0,
            "nuoc_moi": 0,
            "ghi_chu": ""
        }

# ======================================
# CHỌN PHÒNG
# ======================================

st.header("📋 Nhập dữ liệu")

phong = st.selectbox(
    "Chọn phòng cần nhập",
    range(1, so_phong + 1)
)

data = st.session_state.phong_data[phong]

st.subheader(f"🏠 Phòng {phong}")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    data["gia_phong"] = st.number_input(
        "Giá phòng",
        value=data["gia_phong"],
        step=50000
    )

with c2:
    data["dien_cu"] = st.number_input(
        "Điện cũ",
        value=data["dien_cu"]
    )

with c3:
    data["dien_moi"] = st.number_input(
        "Điện mới",
        value=data["dien_moi"]
    )

with c4:
    data["nuoc_cu"] = st.number_input(
        "Nước cũ",
        value=data["nuoc_cu"]
    )

with c5:
    data["nuoc_moi"] = st.number_input(
        "Nước mới",
        value=data["nuoc_moi"]
    )

st.session_state.phong_data[phong] = data
st.text_input(
    "📝 Ghi chú",
    value=data["ghi_chu"],
    key=f"ghichu_{phong}"
)
st.session_state.phong_data[phong] = data
# ======================================
# TÍNH TOÁN
# ======================================

ket_qua = []
tong_doanh_thu = 0

for i in range(1, so_phong + 1):

    d = st.session_state.phong_data[i]

    so_dien = max(d["dien_moi"] - d["dien_cu"],0)
    so_nuoc = max(d["nuoc_moi"] - d["nuoc_cu"],0)

    tien_dien = so_dien * gia_dien
    tien_nuoc = so_nuoc * gia_nuoc

    tong_tien = (
        d["gia_phong"]
        + tien_dien
        + tien_nuoc
        + phi_khac
    )

    tong_doanh_thu += tong_tien

    ket_qua.append({

        "Phòng":i,
        "Giá phòng":f'{d["gia_phong"]:,.0f}',
        "Điện cũ":d["dien_cu"],
        "Điện mới":d["dien_moi"],
        "Tiền điện":f"{tien_dien:,.0f}",
        "Nước cũ":d["nuoc_cu"],
        "Nước mới":d["nuoc_moi"],
        "Tiền nước":f"{tien_nuoc:,.0f}",
        "Phí khác":f"{phi_khac:,.0f}",
        "Tổng tiền":f"{tong_tien:,.0f}",
        "Ghi chú":d["ghi_chu"]
    })

# ======================================
# BẢNG KẾT QUẢ
# ======================================

st.divider()

st.header("📊 Bảng tổng hợp")

df = pd.DataFrame(ket_qua)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.metric(
    "💰 Tổng doanh thu",
    f"{tong_doanh_thu:,.0f} VNĐ"
)

csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "📥 Xuất CSV",
    csv,
    "BangTienPhong.csv",
    "text/csv"
)
