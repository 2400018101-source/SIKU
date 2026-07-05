import streamlit as st
import database as db
from datetime import date, datetime
from matplotlib.figure import Figure
import os
import io
import csv
import uuid

# ==============================================================================
# Konfigurasi Halaman
# ==============================================================================
st.set_page_config(
    page_title="SIKU - Sistem Informasi Keuangan UMKM | Bakso Maenyos",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Folder penyimpanan foto nota (lokal, kompatibel dengan Streamlit Cloud)
NOTA_DIR = "uploads_nota"
os.makedirs(NOTA_DIR, exist_ok=True)

# ==============================================================================
# CSS REPLIKASI TOTAL (Skema Warna Cokelat Gelap, Merah, & Oranye SIKU)
# ==============================================================================
SIKU_EXACT_CSS = """
<style>
    /* Latar Belakang Utama Aplikasi */
    .stApp {
        background-color: #201612 !important;
        color: #D5C7BC !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar Cokelat Pekat */
    [data-testid="stSidebar"] {
        background-color: #1A110E !important;
        border-right: 1px solid #2B1E19 !important;
    }

    /* Kartu Metrik Ringkasan Finansial */
    .metric-card {
        background-color: #2B1E19 !important;
        border: 1px solid #3A2A22 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }

    /* Panel Kotak Utama (Login & Dashboard) */
    .dashboard-panel {
        background-color: #2B1E19 !important;
        border: 1px solid #D32F2F !important;
        border-radius: 14px !important;
        padding: 35px 30px !important;
        margin-bottom: 20px !important;
    }

    /* ====== TOMBOL UTAMA (type="primary") - Merah Solid ====== */
    button[kind="primary"] {
        background-color: #C62828 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        width: 100% !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2) !important;
        transition: background-color 0.2s !important;
    }
    button[kind="primary"]:hover {
        background-color: #B71C1C !important;
        color: #FFFFFF !important;
    }

    /* ====== TOMBOL SEKUNDER (type="secondary", default) - Outline ====== */
    button[kind="secondary"] {
        background-color: #251B17 !important;
        color: #D5C7BC !important;
        border: 1px solid #4A362C !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    button[kind="secondary"]:hover {
        border-color: #E65100 !important;
        color: #FF9800 !important;
    }

    /* Sidebar: tombol Ganti Password / Keluar selalu outline gelap */
    [data-testid="stSidebar"] button {
        background-color: #251B17 !important;
        color: #D5C7BC !important;
        border: 1px solid #3A2A22 !important;
        border-radius: 8px !important;
        width: 100% !important;
        text-align: left !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] button:hover {
        border-color: #E65100 !important;
        color: #FF9800 !important;
    }

    /* Tombol kecil "hapus baris" (X) pada Input Barang Bawaan */
    .st-key-barang_rows_box button[kind="secondary"] {
        width: 100% !important;
        padding: 2px 0px !important;
        color: #D32F2F !important;
        border-color: #3A2A22 !important;
        font-weight: bold !important;
    }
    .st-key-barang_rows_box button[kind="secondary"]:hover {
        background-color: #3A2A22 !important;
        border-color: #D32F2F !important;
        color: #FF5252 !important;
    }

    /* Tombol toggle mata (lihat password) - kecil, kotak */
    .st-key-pw_eye_box button {
        padding: 8px 0px !important;
        min-height: 42px !important;
    }

    /* Tombol ekspor CSV - Oranye Solid */
    .st-key-csv_export_box button {
        background-color: #E65100 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    .st-key-csv_export_box button:hover {
        background-color: #BF360C !important;
    }

    /* Input Fields & ComboBox */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #251B17 !important;
        color: #EFEFEF !important;
        border: 1.5px solid #E65100 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #FF9800 !important;
        box-shadow: 0 0 4px rgba(255, 152, 0, 0.3) !important;
    }

    /* File uploader (Foto Nota) */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #251B17 !important;
        border: 1.5px dashed #E65100 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #E65100 !important;
        color: #FFFFFF !important;
        border: none !important;
        width: auto !important;
    }

    /* Bilah Navigasi Tab Atas */
    button[data-baseweb="tab"] {
        background-color: #251B17 !important;
        color: #A5968E !important;
        border: 1px solid #3A2A22 !important;
        border-bottom: none !important;
        padding: 8px 18px !important;
        border-radius: 8px 8px 0 0 !important;
        margin-right: 4px !important;
    }
    button[aria-selected="true"] {
        background-color: #C62828 !important;
        color: #FFFFFF !important;
        border-color: #C62828 !important;
        font-weight: bold !important;
    }

    /* Label & Keterangan Kecil */
    .text-muted { color: #8C7B72 !important; font-size: 12px; }
    .hint-box {
        background-color: #1A110E !important;
        padding: 12px;
        border-radius: 8px;
        font-size: 11px;
        color: #8C7B72;
    }
    .row-header { color: #8C7B72; font-size: 12px; font-weight: 600; padding-bottom: 4px; }
    .row-value { padding-top: 9px; font-size: 14px; }
    .tag-nota {
        display: inline-block; padding: 2px 8px; border-radius: 6px;
        font-size: 11px; margin-left: 6px;
    }
    .tag-ada { background-color: #1B3B25; color: #4CAF50; }
    .tag-tanpa { background-color: #3A2A22; color: #8C7B72; }
</style>
"""
st.markdown(SIKU_EXACT_CSS, unsafe_allow_html=True)

# Pastikan database terinisialisasi
db.init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
if "show_pw" not in st.session_state:
    st.session_state.show_pw = False


def parse_tanggal(teks: str, fallback: date) -> date:
    """Validasi input tanggal berformat YYYY-MM-DD, kembali ke fallback jika salah."""
    try:
        return datetime.strptime(teks.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


# ==============================================================================
# 1. FORM LOGIN
# ==============================================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #C62828; margin-bottom:0; font-size: 42px; font-weight: bold;'>🍜 SIKU</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8C7B72; font-size:12px; margin-top:0;'>Sistem Informasi Keuangan UMKM</p>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #FF9800; margin-top:0; margin-bottom: 30px;'>Bakso Maenyos</h4>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Masukkan username", key="login_username_field")

        st.markdown("<span style='font-size:14px;'>Password</span>", unsafe_allow_html=True)
        with st.container(key="pw_eye_box"):
            col_pw, col_eye = st.columns([5, 1])
            with col_pw:
                pw_type = "default" if st.session_state.show_pw else "password"
                password = st.text_input(
                    "Password", type=pw_type, placeholder="Masukkan password",
                    key="login_password_field", label_visibility="collapsed"
                )
            with col_eye:
                if st.button("👁", key="toggle_pw_btn"):
                    st.session_state.show_pw = not st.session_state.show_pw
                    st.rerun()

        st.markdown("<p style='text-align: right; margin-top: -10px; font-size: 12px;'><a href='#lupa-password' style='color:#FF9800; text-decoration:none; font-weight:bold;'>Lupa password?</a></p>", unsafe_allow_html=True)
        st.write("")

        if st.button("Masuk", type="primary"):
            if not username or not password:
                st.error("Username dan password wajib diisi.")
            else:
                user = db.verifikasi_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Username atau password salah.")

        st.write("")
        st.markdown(
            '<div class="hint-box">'
            'Daftar username & password Pemilik/Karyawan ada di README.md'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. AREA SETELAH LOGIN
# ==============================================================================
else:
    user = st.session_state.user

    # --- SIDEBAR ---
    st.sidebar.markdown("<h2 style='color: #C62828; margin-bottom: 0; font-weight:bold;'>🍜 SIKU</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: #8C7B72; font-size: 11px; margin-top:0;'>Bakso Maenyos</p>", unsafe_allow_html=True)
    st.sidebar.write("")

    st.sidebar.markdown(
        f"<div class='metric-card' style='background-color: #251B17 !important; border: 1px solid #3A2A22 !important;'>"
        f"<b style='color: #FF9800; font-size:14px;'>{user['nama']}</b><br>"
        f"<span class='text-muted'>Role: {user['role']}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    for _ in range(12):
        st.sidebar.write("")

    with st.sidebar.expander("🔒 Ganti Password"):
        pw_lama = st.text_input("Password Lama", type="password", key="chg_old")
        pw_baru_profile = st.text_input("Password Baru", type="password", key="chg_new")
        if st.button("Simpan Baru", key="btn_simpan_pw"):
            if db.ubah_password(user["id_user"], pw_lama, pw_baru_profile):
                st.success("Berhasil diubah!")
            else:
                st.error("Gagal mengubah.")

    if st.sidebar.button("⏻ Keluar / Logout", use_container_width=True, key="btn_logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # --- NAVIGASI TAB ---
    if user["role"] == "Pemilik":
        tab_dasbor, tab_barang, tab_pengeluaran, tab_ekspor = st.tabs([
            "📊 Dasbor Finansial", "📦 Input Barang Bawaan", "💸 Input Pengeluaran", "📁 Ekspor Laporan"
        ])

        # ----------------------------------------------------------------------
        # Tab 1: Dasbor Real-time Finansial
        # ----------------------------------------------------------------------
        with tab_dasbor:
            st.markdown("<h3 style='color: #FFFFFF; margin-top:10px;'>Ringkasan Finansial Real-time</h3>", unsafe_allow_html=True)

            omset_data = db.rekap_omset_per_tanggal()
            pengeluaran_data = db.rekap_pengeluaran_per_tanggal()

            total_omset = sum(nilai for _, nilai in omset_data)
            total_pengeluaran = sum(nilai for _, nilai in pengeluaran_data)
            laba_bersih = total_omset - total_pengeluaran

            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"<div class='metric-card'><span class='text-muted'>Total Pendapatan (Verified)</span><br><h2 style='color: #4CAF50; margin:0; font-weight:bold;'>Rp {total_omset:,.0f}</h2></div>", unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"<div class='metric-card'><span class='text-muted'>Total Pengeluaran</span><br><h2 style='color: #D32F2F; margin:0; font-weight:bold;'>Rp {total_pengeluaran:,.0f}</h2></div>", unsafe_allow_html=True)
            with m_col3:
                warna_laba = "#4CAF50" if laba_bersih >= 0 else "#D32F2F"
                st.markdown(f"<div class='metric-card'><span class='text-muted'>Estimasi Laba Bersih</span><br><h2 style='color: {warna_laba}; margin:0; font-weight:bold;'>Rp {laba_bersih:,.0f}</h2></div>", unsafe_allow_html=True)

            st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important; padding:20px;">', unsafe_allow_html=True)
            st.markdown("##### 📋 Tren Pendapatan vs Pengeluaran")

            semua_tanggal = sorted(set([t for t, _ in omset_data] + [t for t, _ in pengeluaran_data]))
            map_omset = dict(omset_data)
            map_pengeluaran = dict(pengeluaran_data)
            y_omset = [map_omset.get(t, 0) for t in semua_tanggal]
            y_pengeluaran = [map_pengeluaran.get(t, 0) for t in semua_tanggal]

            fig = Figure(figsize=(10, 3.5), facecolor="#2B1E19")
            ax = fig.add_subplot(111)
            ax.set_facecolor("#2B1E19")

            if not semua_tanggal:
                ax.text(0.5, 0.5, "Belum ada transaksi", ha="center", va="center", color="#8C7B72", transform=ax.transAxes)
            else:
                ax.plot(semua_tanggal, y_omset, marker="o", color="#FF9800", linewidth=2.5, label="Pendapatan")
                ax.plot(semua_tanggal, y_pengeluaran, marker="o", color="#C62828", linewidth=2.5, label="Pengeluaran")
                ax.legend(facecolor="#2B1E19", edgecolor="#2B1E19", labelcolor="white", loc="upper left")
                ax.tick_params(axis='x', colors='#8C7B72', labelsize=8, rotation=10)
                ax.tick_params(axis='y', colors='#8C7B72', labelsize=8)
                ax.grid(True, color="#3A2A22", linestyle="--", alpha=0.5)

            for spine in ax.spines.values():
                spine.set_color("#3A2A22")
            fig.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 2: Input Barang Bawaan (baris dinamis kustom, sesuai referensi)
        # ----------------------------------------------------------------------
        with tab_barang:
            st.markdown("<h3 style='color: white; margin-top:10px;'>📦 Input Barang Bawaan Karyawan</h3>", unsafe_allow_html=True)
            st.markdown(
                "<p class='text-muted' style='margin-top:-10px;'>Hanya Pemilik yang dapat menginput data ini. "
                "Tambahkan beberapa jenis barang sekaligus, omset dihitung otomatis per baris. "
                "Gaji karyawan (17.5% dari total omset) otomatis tersimpan setelah klik Simpan.</p>",
                unsafe_allow_html=True
            )

            if "rows_barang" not in st.session_state:
                st.session_state.rows_barang = [{"id": 0, "nama_barang": list(db.MASTER_BARANG.keys())[0], "jumlah_dibawa": 0, "jumlah_kembali": 0}]
            if "next_row_id" not in st.session_state:
                st.session_state.next_row_id = 1

            def tambah_baris_barang():
                st.session_state.rows_barang.append({
                    "id": st.session_state.next_row_id,
                    "nama_barang": list(db.MASTER_BARANG.keys())[0],
                    "jumlah_dibawa": 0,
                    "jumlah_kembali": 0
                })
                st.session_state.next_row_id += 1

            def hapus_baris_barang(row_id):
                st.session_state.rows_barang = [r for r in st.session_state.rows_barang if r["id"] != row_id]

            b_col1, b_col2 = st.columns([1.3, 1])
            with b_col1:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: #D32F2F; margin-top:0;'>Catat Barang Bawaan Hari Ini</h4>", unsafe_allow_html=True)

                daftar_karyawan = db.ambil_daftar_karyawan()
                map_nama_ke_id = {f"{k['nama']} ({k['username']})": k["id_user"] for k in daftar_karyawan}

                if not map_nama_ke_id:
                    st.warning("Belum ada akun Karyawan terdaftar.")
                else:
                    karyawan_pilih = st.selectbox("Karyawan", options=list(map_nama_ke_id.keys()), key="sel_karyawan")
                    tgl_catat_teks = st.text_input("Tanggal Catat (YYYY-MM-DD)", value=date.today().isoformat(), key="tgl_catat_input")
                    tgl_catat = parse_tanggal(tgl_catat_teks, date.today())
                    if tgl_catat is None:
                        st.error("Format tanggal tidak valid. Gunakan YYYY-MM-DD.")

                    st.write("")
                    with st.container(key="barang_rows_box"):
                        h = st.columns([2.4, 1, 1, 1, 1.4, 0.5])
                        h[0].markdown("<span class='row-header'>Nama Barang</span>", unsafe_allow_html=True)
                        h[1].markdown("<span class='row-header'>Dibawa</span>", unsafe_allow_html=True)
                        h[2].markdown("<span class='row-header'>Kembali</span>", unsafe_allow_html=True)
                        h[3].markdown("<span class='row-header'>Terjual*</span>", unsafe_allow_html=True)
                        h[4].markdown("<span class='row-header'>Omset (Rp)*</span>", unsafe_allow_html=True)
                        h[5].markdown("")

                        preview_omset = 0.0
                        daftar_barang_final = []
                        opsi_barang = list(db.MASTER_BARANG.keys())

                        for row in st.session_state.rows_barang:
                            rid = row["id"]
                            c = st.columns([2.4, 1, 1, 1, 1.4, 0.5])
                            idx_default = opsi_barang.index(row["nama_barang"]) if row["nama_barang"] in opsi_barang else 0
                            nb = c[0].selectbox(
                                "Nama Barang", options=opsi_barang, index=idx_default,
                                key=f"nb_{rid}", label_visibility="collapsed"
                            )
                            dbw = c[1].number_input(
                                "Dibawa", min_value=0, value=int(row["jumlah_dibawa"]), step=1,
                                key=f"db_{rid}", label_visibility="collapsed"
                            )
                            kmb = c[2].number_input(
                                "Kembali", min_value=0, value=int(row["jumlah_kembali"]), step=1,
                                key=f"kb_{rid}", label_visibility="collapsed"
                            )
                            row["nama_barang"] = nb
                            row["jumlah_dibawa"] = dbw
                            row["jumlah_kembali"] = kmb

                            tj = max(0, dbw - kmb)
                            hrg = db.MASTER_BARANG.get(nb, 0)
                            oms = tj * hrg
                            preview_omset += oms

                            c[3].markdown(f"<div class='row-value'>{tj}</div>", unsafe_allow_html=True)
                            c[4].markdown(f"<div class='row-value'>Rp {oms:,.0f}</div>", unsafe_allow_html=True)
                            c[5].button("✕", key=f"del_{rid}", on_click=hapus_baris_barang, args=(rid,))

                            daftar_barang_final.append({
                                "nama_barang": nb, "harga_satuan": hrg, "jumlah_dibawa": dbw,
                                "jumlah_terjual": tj, "jumlah_kembali": kmb, "nilai_omset": oms
                            })

                        st.button("+ Tambah Baris Barang", on_click=tambah_baris_barang, key="btn_tambah_baris")

                    st.write("")
                    st.markdown(
                        f"<div style='background-color: #251B17; padding: 12px; border-radius: 6px; border: 1px solid #3A2A22;'>"
                        f"<span class='text-muted'>Total Omset Harian:</span> <b style='color:#FF9800; float:right;'>Rp {preview_omset:,.0f}</b><br>"
                        f"<span class='text-muted'>Estimasi Gaji (17.5%):</span> <b style='color:#4CAF50; float:right;'>Rp {preview_omset * db.PERSENTASE_GAJI:,.0f}</b>"
                        f"</div>", unsafe_allow_html=True
                    )
                    st.write("")

                    if st.button("💾 Simpan & Hitung Gaji Otomatis", type="primary"):
                        if tgl_catat is None:
                            st.error("Perbaiki format tanggal terlebih dahulu.")
                        else:
                            db.tambah_barang_bawaan_multi(tgl_catat.isoformat(), map_nama_ke_id[karyawan_pilih], daftar_barang_final, user["id_user"])
                            st.success("Data Berhasil Disimpan!")
                            st.session_state.rows_barang = [{"id": st.session_state.next_row_id, "nama_barang": opsi_barang[0], "jumlah_dibawa": 0, "jumlah_kembali": 0}]
                            st.session_state.next_row_id += 1
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with b_col2:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: white; margin-top:0;'>📋 Riwayat Barang Bawaan</h4>", unsafe_allow_html=True)
                riwayat_b = db.ambil_semua_barang_bawaan()
                if not riwayat_b:
                    st.markdown("<p class='text-muted'>Belum ada data barang bawaan.</p>", unsafe_allow_html=True)
                for rb in riwayat_b[:10]:
                    st.markdown(
                        f"<div style='background-color:#251B17; padding:12px; border-radius:8px; margin-bottom:8px; font-size:12px; border: 1px solid #3A2A22;'>"
                        f"<b>{rb['tgl_catat']} • {rb['nama_karyawan']} • {rb['nama_barang']}</b><br>"
                        f"<span class='text-muted'>Dibawa {rb['jumlah_dibawa']} • Terjual {rb['jumlah_terjual']} • Kembali {rb['jumlah_kembali']} • @Rp {rb['harga_satuan']:,.0f}</span><br>"
                        f"<span style='color:#FF9800; font-weight:bold;'>Omset Rp {rb['nilai_omset']:,.0f}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 3: Form Input Pengeluaran (dengan unggah foto nota)
        # ----------------------------------------------------------------------
        with tab_pengeluaran:
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: #D32F2F; margin-top:0;'>💸 Input Pengeluaran Baru</h4>", unsafe_allow_html=True)

                tgl_peng_teks = st.text_input("Tanggal Pengeluaran (YYYY-MM-DD)", value=date.today().isoformat(), key="tgl_peng_input")
                tgl_peng = parse_tanggal(tgl_peng_teks, date.today())
                if tgl_peng is None:
                    st.error("Format tanggal tidak valid. Gunakan YYYY-MM-DD.")

                kat_biaya = st.selectbox("Kategori Biaya", ["Bahan Baku", "Energi", "Operasional"], key="sel_kategori_biaya")
                nama_item = st.text_input("Nama Barang / Kegiatan", placeholder="Contoh: Daging, Bensin Pegawai, Listrik", key="input_nama_item")
                nominal = st.number_input("Nominal Pengeluaran (Rp)", min_value=0.0, step=1000.0, placeholder="Contoh: 150000", key="input_nominal")

                st.markdown("<span style='font-size:14px;'>Foto Nota</span>", unsafe_allow_html=True)
                foto_nota_file = st.file_uploader("Foto Nota", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="uploader_nota")

                st.write("")
                if st.button("Simpan Pengeluaran", type="primary"):
                    if tgl_peng is None:
                        st.error("Perbaiki format tanggal terlebih dahulu.")
                    elif not nama_item or nominal <= 0:
                        st.error("Nama barang/kegiatan dan nominal wajib diisi.")
                    else:
                        path_nota = ""
                        if foto_nota_file is not None:
                            ext = os.path.splitext(foto_nota_file.name)[1] or ".jpg"
                            nama_file = f"{uuid.uuid4().hex}{ext}"
                            path_nota = os.path.join(NOTA_DIR, nama_file)
                            with open(path_nota, "wb") as f:
                                f.write(foto_nota_file.getbuffer())
                        db.tambah_pengeluaran(tgl_peng.isoformat(), kat_biaya, nama_item, nominal, path_nota, user["id_user"])
                        st.success("Pengeluaran disimpan!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with p_col2:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: white; margin-top:0;'>📋 Riwayat Pengeluaran</h4>", unsafe_allow_html=True)
                riwayat_p = db.ambil_semua_pengeluaran()
                if not riwayat_p:
                    st.markdown("<p class='text-muted'>Belum ada data pengeluaran.</p>", unsafe_allow_html=True)
                for rp in riwayat_p[:10]:
                    ada_nota = bool(rp["foto_nota"])
                    tag = "<span class='tag-nota tag-ada'>📎 ada nota</span>" if ada_nota else "<span class='tag-nota tag-tanpa'>tanpa nota</span>"
                    st.markdown(
                        f"<div style='background-color:#251B17; padding:12px; border-radius:8px; margin-bottom:8px; font-size:12px; border: 1px solid #3A2A22;'>"
                        f"<b>{rp['tgl_pengeluaran']} • {rp['kategori_biaya']} • {rp['nama_item']}</b>{tag}<br>"
                        f"<span style='color:#FF9800; font-weight:bold;'>Rp {rp['nominal_biaya']:,.0f}</span>"
                        f"</div>", unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 4: Ekspor Laporan Laba Rugi (dengan tombol unduh sungguhan)
        # ----------------------------------------------------------------------
        with tab_ekspor:
            st.markdown('<div class="dashboard-panel" style="max-width: 700px; border-color:#3A2A22 !important;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color: #D32F2F; margin-top:0;'>📁 Ekspor Laporan Laba Rugi Bulanan</h4>", unsafe_allow_html=True)
            st.markdown("<p class='text-muted' style='margin-top:-8px;'>Pilih bulan (format YYYY-MM) yang ingin direkap, lalu pilih format ekspor.</p>", unsafe_allow_html=True)

            bulan_ekspor = st.text_input("Pilih Bulan (format YYYY-MM)", value=date.today().strftime("%Y-%m"), label_visibility="collapsed", key="input_bulan_ekspor")

            if "rekap_preview" not in st.session_state or st.session_state.get("rekap_bulan_cache") != bulan_ekspor:
                st.session_state.rekap_preview = db.rekap_laba_rugi_bulan(bulan_ekspor)
                st.session_state.rekap_bulan_cache = bulan_ekspor

            rekap = st.session_state.rekap_preview

            teks_laporan = (
                f"Bulan          : {rekap['bulan']}\n"
                f"Pendapatan     : Rp {rekap['total_pendapatan']:,.0f}\n"
                f"Pengeluaran    : Rp {rekap['total_pengeluaran']:,.0f}\n"
                f"Gaji Karyawan  : Rp {rekap['total_gaji']:,.0f}\n"
                f"Laba Bersih    : Rp {rekap['laba_bersih']:,.0f}"
            )

            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["Bulan", "Pendapatan", "Pengeluaran", "Gaji Karyawan", "Laba Bersih"])
            writer.writerow([rekap["bulan"], rekap["total_pendapatan"], rekap["total_pengeluaran"], rekap["total_gaji"], rekap["laba_bersih"]])

            col_txt, col_csv = st.columns(2)
            with col_txt:
                st.download_button(
                    "Ekspor sebagai .TXT", data=teks_laporan.encode("utf-8"),
                    file_name=f"laporan_{rekap['bulan']}.txt", mime="text/plain",
                    type="primary", use_container_width=True, key="dl_txt"
                )
            with col_csv:
                with st.container(key="csv_export_box"):
                    st.download_button(
                        "Ekspor sebagai .CSV", data=csv_buffer.getvalue().encode("utf-8"),
                        file_name=f"laporan_{rekap['bulan']}.csv", mime="text/csv",
                        use_container_width=True, key="dl_csv"
                    )

            st.write("")
            st.markdown("<p style='font-weight:bold;'>Pratinjau Ringkasan:</p>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='metric-card' style='font-family: monospace; font-size:13px; background-color:#1A110E !important; white-space: pre;'>"
                f"{teks_laporan}"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("🔄 Perbarui Pratinjau", key="btn_refresh_preview"):
                st.session_state.rekap_preview = db.rekap_laba_rugi_bulan(bulan_ekspor)
                st.session_state.rekap_bulan_cache = bulan_ekspor
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================================
    # DASHBOARD KARYAWAN (Read-Only)
    # ==========================================================================
    else:
        st.markdown(f"<h3 style='color:white;'>Selamat datang, {user['nama']} 👋</h3>", unsafe_allow_html=True)
        st.markdown("<p class='text-muted'>Anda memiliki akses read-only untuk memantau riwayat barang bawaan, performa penjualan, dan gaji harian.</p>", unsafe_allow_html=True)

        gaji_rows = db.ambil_gaji_by_user(user["id_user"])
        if gaji_rows:
            gaji_terbaru = gaji_rows[0]
            st.markdown(
                f"<div class='dashboard-panel'>"
                f"<span class='text-muted'>Notifikasi Gaji Terbaru ({gaji_terbaru['tgl_gaji']})</span><br>"
                f"<h2 style='color:#4CAF50; margin:5px 0;'>Rp {gaji_terbaru['jumlah_gaji']:,.0f}</h2>"
                f"<span class='text-muted'>Dihitung otomatis dari total omset Rp {gaji_terbaru['total_omset']:,.0f} × 17,5%</span>"
                f"</div>", unsafe_allow_html=True
            )
        else:
            st.info("Belum ada data gaji yang tercatat.")

        st.markdown("<h4 style='color:white; margin-top:20px;'>📋 Riwayat Barang Bawaan & Performa</h4>", unsafe_allow_html=True)
        riwayat_saya = db.ambil_barang_by_user(user["id_user"])
        if not riwayat_saya:
            st.markdown("<p class='text-muted'>Belum ada riwayat barang bawaan.</p>", unsafe_allow_html=True)
        for rb in riwayat_saya[:20]:
            st.markdown(
                f"<div style='background-color:#251B17; padding:12px; border-radius:8px; margin-bottom:8px; font-size:12px; border: 1px solid #3A2A22;'>"
                f"<b>{rb['tgl_catat']} • {rb['nama_barang']}</b><br>"
                f"<span class='text-muted'>Dibawa {rb['jumlah_dibawa']} • Terjual {rb['jumlah_terjual']} • Kembali {rb['jumlah_kembali']}</span><br>"
                f"<span style='color:#FF9800; font-weight:bold;'>Omset Rp {rb['nilai_omset']:,.0f}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        # Catatan: expander "Ganti Password" dan tombol "Keluar/Logout" untuk Karyawan
        # sudah dirender bersama di bagian sidebar umum di atas (berlaku untuk semua role).
