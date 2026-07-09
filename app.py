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

st.title("🏠 PHẦN MỀM QUẢN LÝ THU TIỀN DÃY TRỌ_VỦ ĐỨC BÌNH")

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
# CHỌN THÁNG QUẢN LÝ
# ======================================
st.sidebar.markdown("---")
st.sidebar.header("📅 THỜI GIAN")

# Danh sách 12 tháng trong năm hiện tại
nam_hien_tai = datetime.now().year
danh_sach_thang = [f"Tháng {m}/{nam_hien_tai}" for m in range(1, 13)]

# Lấy tháng hiện tại làm mặc định
thang_hien_tai_idx = datetime.now().month - 1
thang_chon = st.sidebar.selectbox(
    "Chọn tháng làm việc:",
    danh_sach_thang,
    index=thang_hien_tai_idx
)

# Lấy số tháng (int) để tính toán tháng trước/tháng sau
idx_thang_chon = danh_sach_thang.index(thang_chon) + 1 

# ======================================
# KHỞI TẠO & ĐỒNG BỘ DỮ LIỆU THEO THÁNG
# ======================================
if "phong_data_theo_thang" not in st.session_state:
    st.session_state.phong_data_theo_thang = {}

# Khởi tạo dữ liệu cho tháng hiện tại nếu chưa từng có
if idx_thang_chon not in st.session_state.phong_data_theo_thang:
    st.session_state.phong_data_theo_thang[idx_thang_chon] = {}

for i in range(1, so_phong + 1):
    if i not in st.session_state.phong_data_theo_thang[idx_thang_chon]:
        
        # TỰ ĐỘNG LẤY SỐ CŨ TỪ SỐ MỚI CỦA THÁNG TRƯỚC
        dien_cu_mac_dinh = 0
        nuoc_cu_mac_dinh = 0
        thang_truoc = idx_thang_chon - 1
        
        # Nếu có dữ liệu tháng trước, kế thừa số điện/nước mới của tháng trước
        if thang_truoc in st.session_state.phong_data_theo_thang:
            if i in st.session_state.phong_data_theo_thang[thang_truoc]:
                dien_cu_mac_dinh = st.session_state.phong_data_theo_thang[thang_truoc][i].get("dien_moi", 0)
                nuoc_cu_mac_dinh = st.session_state.phong_data_theo_thang[thang_truoc][i].get("nuoc_moi", 0)

        st.session_state.phong_data_theo_thang[idx_thang_chon][i] = {
            "gia_phong": 2500000,
            "dien_cu": dien_cu_mac_dinh,
            "dien_moi": dien_cu_mac_dinh, # Mặc định số mới bằng số cũ nếu chưa nhập
            "nuoc_cu": nuoc_cu_mac_dinh,
            "nuoc_moi": nuoc_cu_mac_dinh, # Mặc định số mới bằng số cũ nếu chưa nhập
            "ghi_chu": ""
        }

# ======================================
# GIAO DIỆN NHẬP DỮ LIỆU
# ======================================
st.header(f"📋 Nhập số liệu - {thang_chon}")

phong = st.selectbox(
    "Chọn phòng cần nhập dữ liệu:",
    range(1, so_phong + 1),
    key=f"selectbox_phong_{idx_thang_chon}" # Đảm bảo không lỗi cache khi đổi tháng
)

# Lấy dữ liệu của phòng được chọn trong tháng được chọn
data = st.session_state.phong_data_theo_thang[idx_thang_chon][phong]

st.subheader(f"🏠 Cập nhật: Phòng {phong} ({thang_chon})")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    data["gia_phong"] = st.number_input(
        "Giá phòng (VNĐ)",
        min_value=0,
        value=int(data["gia_phong"]),
        step=50000,
        key=f"gia_{idx_thang_chon}_{phong}"
    )

with c2:
    data["dien_cu"] = st.number_input(
        "Số điện CŨ",
        min_value=0,
        value=int(data["dien_cu"]),
        key=f"diencu_{idx_thang_chon}_{phong}"
    )

with c3:
    data["dien_moi"] = st.number_input(
        "Số điện MỚI",
        min_value=0,
        value=int(data["dien_moi"]),
        key=f"dienmoi_{idx_thang_chon}_{phong}"
    )

with c4:
    data["nuoc_cu"] = st.number_input(
        "Số nước CŨ",
        min_value=0,
        value=int(data["nuoc_cu"]),
        key=f"nuoccu_{idx_thang_chon}_{phong}"
    )

with c5:
    data["nuoc_moi"] = st.number_input(
        "Số nước MỚI",
        min_value=0,
        value=int(data["nuoc_moi"]),
        key=f"nuocmoi_{idx_thang_chon}_{phong}"
    )

data["ghi_chu"] = st.text_input(
    "📝 Ghi chú (Ví dụ: Đã thanh toán, chưa thanh toán...)",
    value=data["ghi_chu"],
    key=f"ghichu_{idx_thang_chon}_{phong}"
)

# Lưu ngược lại session_state theo tháng và theo phòng
st.session_state.phong_data_theo_thang[idx_thang_chon][phong] = data

# Cập nhật nhanh số cũ cho tháng sau (nếu tháng sau đã được khởi tạo trước đó)
thang_sau = idx_thang_chon + 1
if thang_sau in st.session_state.phong_data_theo_thang and phong in st.session_state.phong_data_theo_thang[thang_sau]:
    st.session_state.phong_data_theo_thang[thang_sau][phong]["dien_cu"] = data["dien_moi"]
    st.session_state.phong_data_theo_thang[thang_sau][phong]["nuoc_cu"] = data["nuoc_moi"]

# ======================================
# XỬ LÝ & TÍNH TOÁN DỮ LIỆU
# ======================================
ket_qua = []
tong_doanh_thu = 0

for i in range(1, so_phong + 1):
    # Đảm bảo phòng i có tồn tại trong bộ nhớ tháng này
    if i in st.session_state.phong_data_theo_thang[idx_thang_chon]:
        d = st.session_state.phong_data_theo_thang[idx_thang_chon][i]
    else:
        continue

    so_dien = max(d["dien_moi"] - d["dien_cu"], 0)
    so_nuoc = max(d["nuoc_moi"] - d["nuoc_cu"], 0)

    tien_dien = so_dien * gia_dien
    tien_nuoc = so_nuoc * gia_nuoc
    tong_tien = d["gia_phong"] + tien_dien + tien_nuoc + phi_khac

    tong_doanh_thu += tong_tien

    ket_qua.append({
        "Phòng": f"Phòng {i}",
        "Giá phòng": d["gia_phong"],
        "Số điện cũ": d["dien_cu"],
        "Số điện mới": d["dien_moi"],
        "Điện tiêu thụ": so_dien,
        "Tiền điện": tien_dien,
        "Số nước cũ": d["nuoc_cu"],
        "Số nước mới": d["nuoc_moi"],
        "Nước tiêu thụ": so_nuoc,
        "Tiền nước": tien_nuoc,
        "Phí khác": phi_khac,
        "Tổng tiền": tong_tien,
        "Ghi chú": d["ghi_chu"]
    })

# ======================================
# HIỂN THỊ BẢNG KẾT QUẢ & XUẤT FILE
# ======================================
st.divider()
st.header(f"📊 Bảng tổng hợp tiền trọ - {thang_chon}")

if ket_qua:
    df = pd.DataFrame(ket_qua)

    # Hiển thị số tiền được định dạng qua st.column_config
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

    # Hiển thị tổng doanh thu
    st.metric(
        f"💰 TỔNG THU NHẬP CÁC PHÒNG ({thang_chon})",
        f"{tong_doanh_thu:,.0f} VNĐ"
    )

    # Nút xuất file dữ liệu CSV kèm tên tháng
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label=f"📥 Xuất Báo Cáo {thang_chon} (CSV)",
        data=csv,
        file_name=f"Bang_Tien_Phong_{thang_chon.replace('/', '_')}.csv",
        mime="text/csv"
    )
else:
    st.info("Chưa có dữ liệu phòng nào cho tháng này.")
