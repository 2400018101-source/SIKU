import streamlit as st
import database as db
from datetime import date
import matplotlib
import os

# Set Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="SIKU - Sistem Informasi Keuangan UMKM | Bakso Maenyos",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS REPLIKASI TOTAL (Mengikuti Skema Warna Muted Brown, Merah, & Oranye SIKU)
# ==============================================================================
SIKU_EXACT_CSS = """
<style>
    /* Latar Belakang Utama Aplikasi - Cokelat Gelap Eksklusif SIKU */
    .stApp {
        background-color: #201612 !important;
        color: #D5C7BC !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Desain Sidebar Cokelat Pekat Tanpa Border Terang */
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
    
    /* Panel Kotak Utama Utama (Login & Dashboard) */
    .dashboard-panel {
        background-color: #2B1E19 !important;
        border: 1px solid #D32F2F !important; /* Garis Tepi Merah Halus SIKU */
        border-radius: 14px !important;
        padding: 35px 30px !important;
        margin-bottom: 20px !important;
    }

    /* Tombol Utama SIKU - Merah Solid Melengkung */
    div.stButton > button:first-child {
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
    div.stButton > button:first-child:hover {
        background-color: #B71C1C !important;
        color: #FFFFFF !important;
    }

    /* Input Fields & ComboBox - Cokelat dengan Border Tepi Oranye */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #251B17 !important;
        color: #EFEFEF !important;
        border: 1.5px solid #E65100 !important; /* Tepi Oranye SIKU */
        border-radius: 8px !important;
        padding: 8px !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #FF9800 !important;
        box-shadow: 0 0 4px rgba(255, 152, 0, 0.3) !important;
    }
    
    /* Modifikasi Bilah Navigasi Tab di Sisi Atas */
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
        background-color: #C62828 !important; /* Tab Merah Aktif */
        color: #FFFFFF !important;
        border-color: #C62828 !important;
        font-weight: bold !important;
    }

    /* Label & Keterangan Kecil */
    .text-muted {
        color: #8C7B72 !important;
        font-size: 12px;
    }
    .hint-box {
        background-color: #1A110E !important;
        padding: 12px;
        border-radius: 8px;
        font-size: 11px;
        color: #8C7B72;
    }
</style>
"""
st.markdown(SIKU_EXACT_CSS, unsafe_allow_html=True)

# Pastikan database terinisialisasi
db.init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# ==============================================================================
# 1. FORM LOGIN KUSTOM (Sesuai image_44f9af.png)
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
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        st.markdown("<p style='text-align: right; margin-top: -10px; font-size: 12px;'><a href='#lupa-password' style='color:#FF9800; text-decoration:none; font-weight:bold;'>Lupa password?</a></p>", unsafe_allow_html=True)
        st.write("")
        
        if st.button("Masuk"):
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
# 2. AREA LOGIN UTAMA (Sesuai Dashboard image_44f9eb.png)
# ==============================================================================
else:
    user = st.session_state.user
    
    # --- NAVIGATION SIDEBAR ---
    st.sidebar.markdown(f"<h2 style='color: #C62828; margin-bottom: 0; font-weight:bold;'>🍜 SIKU</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: #8C7B72; font-size: 11px; margin-top:0;'>Bakso Maenyos</p>", unsafe_allow_html=True)
    st.sidebar.write("")
    
    # Identitas Akun
    st.sidebar.markdown(
        f"<div class='metric-card' style='background-color: #251B17 !important; border: 1px solid #3A2A22 !important;'>"
        f"<b style='color: #FF9800; font-size:14px;'>{user['nama']}</b><br>"
        f"<span class='text-muted'>Role: {user['role']}</span>"
        f"</div>", 
        unsafe_allow_html=True
    )
    
    # Space filler agar tombol menempel di bagian bawah sidebar (Sesuai gambar referensi)
    for _ in range(12): st.sidebar.write("")
    
    # Tombol Ganti Password & Keluar
    with st.sidebar.expander("🔒 Ganti Password"):
        pw_lama = st.text_input("Password Lama", type="password", key="chg_old")
        pw_baru_profile = st.text_input("Password Baru", type="password", key="chg_new")
        if st.sidebar.button("Simpan Baru"):
            if db.ubah_password(user["id_user"], pw_lama, pw_baru_profile):
                st.sidebar.success("Berhasil diubah!")
            else:
                st.sidebar.error("Gagal mengubah.")

    if st.sidebar.button("Keluar / Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # --- PENATAAN NAVIGASI TAB ---
    if user["role"] == "Pemilik":
        tab_dasbor, tab_barang, tab_pengeluaran, tab_ekspor = st.tabs([
            "📊 Dasbor Finansial", "📦 Input Barang Bawaan", "💸 Input Pengeluaran", "📁 Ekspor Laporan"
        ])
        
        # ----------------------------------------------------------------------
        # Tab 1: Dasbor Real-time Finansial (Sesuai image_44f9eb.png)
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
            
            # Pengaturan Grafik Matplotlib Agar Selaras dengan Cokelat SIKU
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
            
            for spine in ax.spines.values(): spine.set_color("#3A2A22")
            fig.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 2: Input Barang Bawaan (Sesuai image_44fa09.png)
        # ----------------------------------------------------------------------
        with tab_barang:
            st.markdown("<h3 style='color: white; margin-top:10px;'>📦 Input Barang Bawaan Karyawan</h3>", unsafe_allow_html=True)
            st.markdown("<p class='text-muted' style='margin-top:-10px;'>Hanya Pemilik yang dapat menginput data ini. Gaji karyawan (17.5% dari total omset) otomatis tersimpan.</p>", unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns([1.3, 1])
            with b_col1:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: #D32F2F; margin-top:0;'>Catat Barang Bawaan Hari Ini</h4>", unsafe_allow_html=True)
                
                daftar_karyawan = db.ambil_daftar_karyawan()
                map_nama_ke_id = {f"{k['nama']} ({k['username']})": k["id_user"] for k in daftar_karyawan}
                
                karyawan_pilih = st.selectbox("Karyawan", options=list(map_nama_ke_id.keys()))
                tgl_catat = st.date_input("Tanggal Catat (YYYY-MM-DD)", date.today())
                
                st.write("")
                init_df = [{"Nama Barang": list(db.MASTER_BARANG.keys())[0], "Jumlah Dibawa": 0, "Jumlah Kembali": 0}]
                edited_df = st.data_editor(
                    init_df, 
                    num_rows="dynamic", 
                    column_config={
                        "Nama Barang": st.column_config.SelectboxColumn(options=list(db.MASTER_BARANG.keys()), required=True),
                        "Jumlah Dibawa": st.column_config.NumberColumn(min_value=0, default=0, required=True),
                        "Jumlah Kembali": st.column_config.NumberColumn(min_value=0, default=0, required=True)
                    }
                )
                
                preview_omset = 0.0
                daftar_barang_final = []
                
                for row in edited_df:
                    nb = row.get("Nama Barang")
                    dbw = row.get("Jumlah Dibawa", 0)
                    kmb = row.get("Jumlah Kembali", 0)
                    tj = max(0, dbw - kmb)
                    hrg = db.MASTER_BARANG.get(nb, 0)
                    oms = tj * hrg
                    preview_omset += oms
                    daftar_barang_final.append({
                        "nama_barang": nb, "harga_satuan": hrg, "jumlah_dibawa": dbw,
                        "jumlah_terjual": tj, "jumlah_kembali": kmb, "nilai_omset": oms
                    })
                
                st.write("")
                st.markdown(
                    f"<div style='background-color: #251B17; padding: 12px; border-radius: 6px; border: 1px solid #3A2A22;'>"
                    f"<span class='text-muted'>Total Omset Harian:</span> <b style='color:#FF9800; float:right;'>Rp {preview_omset:,.0f}</b><br>"
                    f"<span class='text-muted'>Estimasi Gaji (17.5%):</span> <b style='color:#4CAF50; float:right;'>Rp {preview_omset*db.PERSENTASE_GAJI:,.0f}</b>"
                    f"</div>", unsafe_allow_html=True
                )
                st.write("")
                
                if st.button("💾 Simpan & Hitung Gaji Otomatis"):
                    db.tambah_barang_bawaan_multi(tgl_catat.isoformat(), map_nama_ke_id[karyawan_pilih], daftar_barang_final, user["id_user"])
                    st.success("Data Berhasil Disimpan!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                        
            with b_col2:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: white; margin-top:0;'>📋 Riwayat Barang Bawaan</h4>", unsafe_allow_html=True)
                riwayat_b = db.ambil_semua_barang_bawaan()
                for rb in riwayat_b[:10]:
                    st.markdown(
                        f"<div style='background-color:#251B17; padding:12px; border-radius:8px; margin-bottom:8px; font-size:12px; border: 1px solid #3A2A22;'>"
                        f"<b>{rb['tgl_catat']} • {rb['nama_karyawan']} • {rb['nama_barang']}</b><br>"
                        f"<span class='text-muted'>Dibawa {rb['jumlah_dibawa']} • Terjual {rb['jumlah_terjual']} • Kembali {rb['jumlah_kembali']}</span><br>"
                        f"<span style='color:#FF9800; font-weight:bold;'>Omset Rp {rb['nilai_omset']:,.0f}</span>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 3: Form Input Pengeluaran (Sesuai image_44fa10.png)
        # ----------------------------------------------------------------------
        with tab_pengeluaran:
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: #D32F2F; margin-top:0;'>💸 Input Pengeluaran Baru</h4>", unsafe_allow_html=True)
                tgl_peng = st.date_input("Tanggal Pengeluaran (YYYY-MM-DD)", date.today())
                kat_biaya = st.selectbox("Kategori Biaya", ["Bahan Baku", "Energi", "Operasional"])
                nama_item = st.text_input("Nama Barang / Kegiatan", placeholder="Contoh: Daging, Bensin Pegawai")
                nominal = st.number_input("Nominal Pengeluaran (Rp)", min_value=0.0, step=1000.0)
                st.write("")
                
                if st.button("Simpan Pengeluaran"):
                    db.tambah_pengeluaran(tgl_peng.isoformat(), kat_biaya, nama_item, nominal, "", user["id_user"])
                    st.success("Pengeluaran disimpan!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with p_col2:
                st.markdown('<div class="dashboard-panel" style="border-color:#3A2A22 !important;">', unsafe_allow_html=True)
                st.markdown("<h4 style='color: white; margin-top:0;'>📋 Riwayat Pengeluaran</h4>", unsafe_allow_html=True)
                riwayat_p = db.ambil_semua_pengeluaran()
                for rp in riwayat_p[:10]:
                    st.markdown(
                        f"<div style='background-color:#251B17; padding:12px; border-radius:8px; margin-bottom:8px; font-size:12px; border: 1px solid #3A2A22;'> "
                        f"<b>{rp['tgl_pengeluaran']} • {rp['kategori_biaya']} • {rp['nama_item']}</b><br>"
                        f"<span style='color:#FF9800; font-weight:bold;'>Rp {rp['nominal_biaya']:,.0f}</span>"
                        f"</div>", unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 4: Ekspor Laporan Laba Rugi (Sesuai image_44fa2a.png)
        # ----------------------------------------------------------------------
        with tab_ekspor:
            st.markdown('<div class="dashboard-panel" style="max-width: 700px; border-color:#3A2A22 !important;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color: #D32F2F; margin-top:0;'>📁 Ekspor Laporan Laba Rugi Bulanan</h4>", unsafe_allow_html=True)
            bulan_ekspor = st.text_input("Pilih Bulan (format YYYY-MM)", value=date.today().strftime("%Y-%m"))
            
            if bulan_ekspor:
                rekap = db.rekap_laba_rugi_bulan(bulan_ekspor)
                st.markdown(
                    f"<div class='metric-card' style='font-family: monospace; font-size:13px; background-color:#1A110E !important; white-space: pre;'>"
                    f"Bulan          : {rekap['bulan']}\n"
                    f"Pendapatan     : Rp {rekap['total_pendapatan']:,.0f}\n"
                    f"Pengeluaran    : Rp {rekap['total_pengeluaran']:,.0f}\n"
                    f"Gaji Karyawan  : Rp {rekap['total_gaji']:,.0f}\n"
                    f"Laba Bersih    : Rp {rekap['laba_bersih']:,.0f}"
                    f"</div>", 
                    unsafe_allow_html=True
                )
