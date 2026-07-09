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
# KHỞI TẠO & ĐỒNG BỘ DỮ LIỆU
# ======================================
if "phong_data" not in st.session_state:
    st.session_state.phong_data = {}

# Khởi tạo dữ liệu mặc định cho các phòng mới nếu chưa có
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
# GIAO DIỆN NHẬP DỮ LIỆU
# ======================================
st.header("📋 Nhập số điện và số nước")

phong = st.selectbox(
    "Chọn phòng cần nhập dữ liệu:",
    range(1, so_phong + 1)
)

# Lấy dữ liệu hiện tại của phòng được chọn
data = st.session_state.phong_data[phong]

st.subheader(f"🏠 Cập nhật: Phòng {phong}")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    data["gia_phong"] = st.number_input(
        "Giá phòng (VNĐ)",
        min_value=0,
        value=int(data["gia_phong"]),
        step=50000,
        key=f"gia_{phong}"
    )

with c2:
    data["dien_cu"] = st.number_input(
        "Số điện CŨ",
        min_value=0,
        value=int(data["dien_cu"]),
        key=f"diencu_{phong}"
    )

with c3:
    data["dien_moi"] = st.number_input(
        "Số điện MỚI",
        min_value=0,
        value=int(data["dien_moi"]),
        key=f"dienmoi_{phong}"
    )

with c4:
    data["nuoc_cu"] = st.number_input(
        "Số nước CŨ",
        min_value=0,
        value=int(data["nuoc_cu"]),
        key=f"nuoccu_{phong}"
    )

with c5:
    data["nuoc_moi"] = st.number_input(
        "Số nước MỚI",
        min_value=0,
        value=int(data["nuoc_moi"]),
        key=f"nuocmoi_{phong}"
    )

# Sửa lỗi: Nhận giá trị ghi chú và lưu trực tiếp vào data
data["ghi_chu"] = st.text_input(
    "📝 Ghi chú (Ví dụ: Đã thanh toán, chưa thanh toán...)",
    value=data["ghi_chu"],
    key=f"ghichu_{phong}"
)

# Lưu ngược lại session_state sau khi người dùng thay đổi
st.session_state.phong_data[phong] = data

# ======================================
# XỬ LÝ & TÍNH TOÁN DỮ LIỆU
# ======================================
ket_qua = []
tong_doanh_thu = 0

# Chỉ duyệt qua đúng số lượng phòng đang được chọn trên slider
for i in range(1, so_phong + 1):
    d = st.session_state.phong_data[i]

    so_dien = max(d["dien_moi"] - d["dien_cu"], 0)
    so_nuoc = max(d["nuoc_moi"] - d["nuoc_cu"], 0)

    tien_dien = so_dien * gia_dien
    tien_nuoc = so_nuoc * gia_nuoc
    tong_tien = d["gia_phong"] + tien_dien + tien_nuoc + phi_khac

    tong_doanh_thu += tong_tien

    # Giữ nguyên kiểu dữ liệu Số (Numeric) để hiển thị/xuất file chuẩn hơn
    ket_qua.append({
        "Phòng": f"Phòng {i}",
        "Giá phòng": d["gia_phong"],
        "Số điện tiêu thụ": so_dien,
        "Tiền điện": tien_dien,
        "Số nước tiêu thụ": so_nuoc,
        "Tiền nước": tien_nuoc,
        "Phí khác": phi_khac,
        "Tổng tiền": tong_tien,
        "Ghi chú": d["ghi_chu"]
    })

# ======================================
# HIỂN THỊ BẢNG KẾT QUẢ & XUẤT FILE
# ======================================
st.divider()
st.header("📊 Bảng tổng hợp tiền trọ")

df = pd.DataFrame(ket_qua)

# Hiển thị số tiền được định dạng phân tách dấu phẩy đẹp mắt qua st.column_config
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Giá phòng": st.column_config.NumberColumn(format="%d VNĐ"),
        "Tiền điện": st.column_config.NumberColumn(format="%d VNĐ"),
        "Tiền nước": st.column_config.NumberColumn(format="%d VNĐ"),
        "Phí khác": st.column_config.NumberColumn(format="%d VNĐ"),
        "Tổng tiền": st.column_config.NumberColumn(format="%d VNĐ"),
    }
)

# Hiển thị tổng doanh thu tổng quan
st.metric(
    "💰 TỔNG THU NHẬP CÁC PHÒNG",
    f"{tong_doanh_thu:,.0f} VNĐ"
)

# Nút xuất file dữ liệu CSV
csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="📥 Xuất Báo Cáo ( CSV )",
    data=csv,
    file_name="Bang_Thanh_Toan_Tien_Phong.csv",
    mime="text/csv"
)
