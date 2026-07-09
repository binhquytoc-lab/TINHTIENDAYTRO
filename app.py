import streamlit as st
import pandas as pd

# ======================================
# CẤU HÌNH TRANG
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

st.sidebar.header("⚙️ CẤU HÌNH")

gia_dien = st.sidebar.number_input(
    "⚡ Giá điện (VNĐ/số)",
    min_value=0,
    value=3500,
    step=100
)

gia_nuoc = st.sidebar.number_input(
    "💧 Giá nước (VNĐ/m³)",
    min_value=0,
    value=15000,
    step=500
)

phi_khac = st.sidebar.number_input(
    "📦 Phí khác (Wifi, Rác...)",
    min_value=0,
    value=150000,
    step=10000
)

so_phong = st.sidebar.slider(
    "🏠 Số phòng",
    min_value=1,
    max_value=50,
    value=10
)

st.divider()

st.header("📋 NHẬP CHỈ SỐ ĐIỆN NƯỚC TỪNG PHÒNG")

ket_qua = []
tong_doanh_thu = 0

for i in range(1, so_phong + 1):

    st.subheader(f"🏠 Phòng {i}")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        gia_phong = st.number_input(
            "Giá phòng",
            min_value=0,
            value=2500000,
            step=50000,
            key=f"gp{i}"
        )

    with c2:
        dien_cu = st.number_input(
            "Số điện cũ",
            min_value=0,
            key=f"dc{i}"
        )

    with c3:
        dien_moi = st.number_input(
            "Số điện mới",
            min_value=0,
            key=f"dm{i}"
        )

    with c4:
        nuoc_cu = st.number_input(
            "Số nước cũ",
            min_value=0,
            key=f"nc{i}"
        )

    with c5:
        nuoc_moi = st.number_input(
            "Số nước mới",
            min_value=0,
            key=f"nm{i}"
        )

    # Kiểm tra dữ liệu

    if dien_moi < dien_cu:
        st.warning(f"⚠️ Phòng {i}: Điện mới phải lớn hơn hoặc bằng điện cũ.")

    if nuoc_moi < nuoc_cu:
        st.warning(f"⚠️ Phòng {i}: Nước mới phải lớn hơn hoặc bằng nước cũ.")

    so_dien = max(dien_moi - dien_cu, 0)
    so_nuoc = max(nuoc_moi - nuoc_cu, 0)

    tien_dien = so_dien * gia_dien
    tien_nuoc = so_nuoc * gia_nuoc

    tong_tien = (
        gia_phong
        + tien_dien
        + tien_nuoc
        + phi_khac
    )

    tong_doanh_thu += tong_tien

    ket_qua.append({
        "Phòng": i,
        "Giá phòng": f"{gia_phong:,.0f}",
        "Số điện cũ": dien_cu,
        "Số điện mới": dien_moi,
        "Tiền điện": f"{tien_dien:,.0f}",
        "Số nước cũ": nuoc_cu,
        "Số nước mới": nuoc_moi,
        "Tiền nước": f"{tien_nuoc:,.0f}",
        "Phí khác": f"{phi_khac:,.0f}",
        "Tổng tiền": f"{tong_tien:,.0f}"
    })

st.divider()

st.header("📊 BẢNG TÍNH TIỀN TRỌ")

df = pd.DataFrame(ket_qua)

st.dataframe(
    df,
    use_container_width=True,
hide_index=True
)

st.divider()

st.metric(
    "💰 TỔNG THU NHẬP CẢ DÃY TRỌ",
    f"{tong_doanh_thu:,.0f} VNĐ"
)

st.divider()

csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "📥 Xuất file CSV",
    data=csv,
    file_name="BangTinhTienPhong.csv",
    mime="text/csv"
)
