import streamlit as st
import database as db
from datetime import date
import matplotlib
import os

# Set Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="SIKU - Sistem Informasi Keuangan UMKM",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# INJEKSI CSS PREMIUM (Mengubah Total Elemen Web Menjadi GUI Desktop SIKU)
# ==============================================================================
DESKTOP_GUI_CSS = """
<style>
    /* Mengubah Latar Belakang Utama Aplikasi (Gelap Pekat) */
    .stApp {
        background-color: #1A1A1A !important;
        color: #F5F5F5 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Desain Sidebar GUI Desktop */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 2px solid #3A1010 !important;
    }

    /* Kartu Metrik / Kotak Informasi dengan Border Tegas */
    .metric-card {
        background-color: #242424 !important;
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Kartu Utama di Dashboard Karyawan / Pemilik */
    .dashboard-panel {
        background-color: #242424 !important;
        border: 1px solid #4A1212 !important; /* Border merah tua khas desktop Anda */
        border-radius: 8px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }

    /* Tombol Utama - Merah Kuliner (Hover Oranye Menyala) */
    div.stButton > button:first-child {
        background-color: #D32F2F !important;
        color: #FFFFFF !important;
        border: 1px solid #B71C1C !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #B71C1C !important;
        border-color: #FF9800 !important; /* Aksen tepi oranye saat disentuh */
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
    }

    /* Desain Kotak Input & Dropdown Bergaya Oranye Desktop */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid #FF9800 !important; /* Garis tepi oranye khas */
        border-radius: 6px !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #F57C00 !important;
        box-shadow: 0 0 5px rgba(255, 152, 0, 0.4) !important;
    }
    
    /* Desain Tab Web */
    button[data-baseweb="tab"] {
        background-color: #242424 !important;
        color: #888888 !important;
        border: 1px solid #333333 !important;
        border-bottom: none !important;
        padding: 10px 20px !important;
        border-top-left-radius: 6px !important;
        border-top-right-radius: 6px !important;
    }
    button[aria-selected="true"] {
        background-color: #D32F2F !important;
        color: #FFFFFF !important;
        border-color: #D32F2F !important;
        font-weight: bold !important;
    }

    /* Teks Muted / Sekunder */
    .text-muted {
        color: #AAAAAA !important;
        font-size: 12px;
    }
</style>
"""
st.markdown(DESKTOP_GUI_CSS, unsafe_allow_html=True)

# Pastikan database terinisialisasi
db.init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# ==============================================================================
# 1. HALAMAN LOGIN (Dibuat Presisi Tengah dengan Bingkai Merah Tua SIKU)
# ==============================================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.write("")
        st.write("")
        # Membungkus form ke dalam satu panel terpadu seperti widget desktop Anda
        st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #D32F2F; margin-bottom:0; font-size: 38px;'>🍜 SIKU</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #AAAAAA; font-size:12px; margin-top:0;'>Sistem Informasi Keuangan UMKM</p>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #FF9800; margin-top:0; margin-bottom: 25px;'>Bakso Maenyos</h4>", unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
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
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Fitur Lupa Password
        with st.expander("🔑 Lupa password?"):
            user_lupa = st.text_input("Masukkan Username Anda", key="lupa_user")
            if user_lupa:
                pertanyaan = db.ambil_pertanyaan_keamanan(user_lupa)
                if pertanyaan:
                    st.warning(f"❓ Pertanyaan Keamanan: {pertanyaan}")
                    jawaban = st.text_input("Jawaban Anda", key="lupa_jawab")
                    pw_baru = st.text_input("Password Baru (Min. 6 karakter)", type="password", key="lupa_pw")
                    pw_konf = st.text_input("Ulangi Password Baru", type="password", key="lupa_pw_konf")
                    
                    if st.button("Reset Password"):
                        if pw_baru != pw_konf:
                            st.error("Konfirmasi password tidak cocok.")
                        elif len(pw_baru) < 6:
                            st.error("Password baru minimal 6 karakter.")
                        else:
                            if db.reset_password_via_keamanan(user_lupa, jawaban, pw_baru):
                                st.success("Password berhasil diperbarui!")
                            else:
                                st.error("Jawaban keamanan salah.")
                else:
                    st.error("Username tidak ditemukan.")

# ==============================================================================
# 2. PANEL DASHBOARD UTAMA
# ==============================================================================
else:
    user = st.session_state.user
    
    # --- SIDEBAR KUSTOM ---
    st.sidebar.markdown(f"<h2 style='color: #D32F2F; margin-bottom: 0;'>🍜 SIKU</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: #AAAAAA; font-size: 11px; margin-top:0;'>Bakso Maenyos</p>", unsafe_allow_html=True)
    
    # Kartu Identitas Pengguna di Sidebar
    st.sidebar.markdown(
        f"<div class='metric-card' style='padding:12px; margin-bottom: 20px; border-color:#FF9800 !important;'>"
        f"<b style='color: #FFFFFF; font-size:14px;'>{user['nama']}</b><br>"
        f"<span style='color: #FF9800; font-size:11px;'>Role: {user['role']}</span>"
        f"</div>", 
        unsafe_allow_html=True
    )
    
    # Ganti Password
    with st.sidebar.expander("🔒 Ganti Password"):
        pw_lama = st.text_input("Password Lama", type="password", key="chg_old")
        pw_baru_profile = st.text_input("Password Baru", type="password", key="chg_new")
        pw_konf_profile = st.text_input("Konfirmasi Password", type="password", key="chg_conf")
        if st.sidebar.button("Simpan Password Baru"):
            if pw_baru_profile != pw_konf_profile:
                st.sidebar.error("Konfirmasi tidak cocok.")
            elif len(pw_baru_profile) < 6:
                st.sidebar.error("Minimal 6 karakter.")
            else:
                if db.ubah_password(user["id_user"], pw_lama, pw_baru_profile):
                    st.sidebar.success("Password berhasil diubah!")
                else:
                    st.sidebar.error("Password lama salah.")
                    
    st.sidebar.write("")
    if st.sidebar.button("Keluar / Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # ==========================================================================
    # A. DASHBOARD ROLE: PEMILIK
    # ==========================================================================
    if user["role"] == "Pemilik":
        tab_dasbor, tab_barang, tab_pengeluaran, tab_ekspor = st.tabs([
            "📊 Dasbor Finansial", "📦 Input Barang Bawaan", "💸 Input Pengeluaran", "📁 Ekspor Laporan"
        ])
        
        # ----------------------------------------------------------------------
        # Tab 1: Dasbor Real-time Finansial
        # ----------------------------------------------------------------------
        with tab_dasbor:
            st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
            st.markdown("<h3 style='color: #FFFFFF; margin-top:0;'>Ringkasan Finansial Real-time</h3>", unsafe_allow_html=True)
            
            omset_data = db.rekap_omset_per_tanggal()
            pengeluaran_data = db.rekap_pengeluaran_per_tanggal()
            
            total_omset = sum(nilai for _, nilai in omset_data)
            total_pengeluaran = sum(nilai for _, nilai in pengeluaran_data)
            laba_bersih = total_omset - total_pengeluaran
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"<div class='metric-card' style='border-left: 4px solid #4CAF50 !important;'><span class='text-muted'>Total Pendapatan (Verified)</span><br><h2 style='color: #4CAF50; margin:0;'>Rp {total_omset:,.0f}</h2></div>", unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"<div class='metric-card' style='border-left: 4px solid #F44336 !important;'><span class='text-muted'>Total Pengeluaran</span><br><h2 style='color: #F44336; margin:0;'>Rp {total_pengeluaran:,.0f}</h2></div>", unsafe_allow_html=True)
            with m_col3:
                warna_laba = "#4CAF50" if laba_bersih >= 0 else "#F44336"
                st.markdown(f"<div class='metric-card' style='border-left: 4px solid #FF9800 !important;'><span class='text-muted'>Estimasi Laba Bersih</span><br><h2 style='color: {warna_laba}; margin:0;'>Rp {laba_bersih:,.0f}</h2></div>", unsafe_allow_html=True)
            
            st.markdown("<br>##### 📈 Tren Pendapatan vs Pengeluaran", unsafe_allow_html=True)
            from matplotlib.figure import Figure
            
            semua_tanggal = sorted(set([t for t, _ in omset_data] + [t for t, _ in pengeluaran_data]))
            map_omset = dict(omset_data)
            map_pengeluaran = dict(pengeluaran_data)
            y_omset = [map_omset.get(t, 0) for t in semua_tanggal]
            y_pengeluaran = [map_pengeluaran.get(t, 0) for t in semua_tanggal]
            
            fig = Figure(figsize=(10, 3.2), facecolor="#242424")
            ax = fig.add_subplot(111)
            ax.set_facecolor("#242424")
            
            if not semua_tanggal:
                ax.text(0.5, 0.5, "Belum ada data transaksi", ha="center", va="center", color="#AAAAAA", transform=ax.transAxes)
            else:
                ax.plot(semua_tanggal, y_omset, marker="o", color="#FF9800", linewidth=2.2, label="Pendapatan")
                ax.plot(semua_tanggal, y_pengeluaran, marker="o", color="#D32F2F", linewidth=2.2, label="Pengeluaran")
                ax.legend(facecolor="#242424", edgecolor="#242424", labelcolor="white", loc="upper left")
                ax.tick_params(axis="x", colors="#AAAAAA", labelsize=8, rotation=15)
                ax.tick_params(axis="y", colors="#AAAAAA", labelsize=8)
                ax.grid(True, color="#333333", linestyle="--", alpha=0.5)
            
            for spine in ax.spines.values():
                spine.set_color("#444444")
            fig.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 2: Input Barang Bawaan (Panel Kiri Form, Panel Kanan Riwayat)
        # ----------------------------------------------------------------------
        with tab_barang:
            b_col1, b_col2 = st.columns([1.3, 1])
            with b_col1:
                st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: #D32F2F; margin-top:0;'>Catat Barang Bawaan Hari Ini</h3>", unsafe_allow_html=True)
                
                daftar_karyawan = db.ambil_daftar_karyawan()
                map_nama_ke_id = {f"{k['nama']} ({k['username']})": k["id_user"] for k in daftar_karyawan}
                
                karyawan_pilih = st.selectbox("Karyawan", options=list(map_nama_ke_id.keys()))
                tgl_catat = st.date_input("Tanggal Catat (YYYY-MM-DD)", date.today())
                
                st.write("")
                st.markdown("<span class='text-muted'>Isi daftar item di bawah ini:</span>", unsafe_allow_html=True)
                
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
                valid = True
                
                for row in edited_df:
                    nb = row.get("Nama Barang")
                    dbw = row.get("Jumlah Dibawa", 0)
                    kmb = row.get("Jumlah Kembali", 0)
                    
                    if kmb > dbw:
                        st.error(f"Jumlah kembali pada ({nb}) melebihi jumlah dibawa.")
                        valid = False
                        break
                    
                    tj = dbw - kmb
                    hrg = db.MASTER_BARANG.get(nb, 0)
                    oms = tj * hrg
                    preview_omset += oms
                    daftar_barang_final.append({
                        "nama_barang": nb, "harga_satuan": hrg, "jumlah_dibawa": dbw,
                        "jumlah_terjual": tj, "jumlah_kembali": kmb, "nilai_omset": oms
                    })
                
                st.write("")
                st.markdown(
                    f"<div style='background-color: #2D2D2D; padding: 12px; border-radius: 6px; border: 1px solid #444444;'>"
                    f"<span class='text-muted'>Total Omset Harian:</span> <b style='color:#FF9800; float:right;'>Rp {preview_omset:,.0f}</b><br>"
                    f"<span class='text-muted'>Estimasi Gaji ({db.PERSENTASE_GAJI*100:.1f}%):</span> <b style='color:#4CAF50; float:right;'>Rp {preview_omset*db.PERSENTASE_GAJI:,.0f}</b>"
                    f"</div>", unsafe_allow_html=True
                )
                st.write("")
                
                if st.button("💾 Simpan & Hitung Gaji Otomatis") and valid:
                    if not daftar_barang_final:
                        st.warning("Data barang masih kosong.")
                    else:
                        db.tambah_barang_bawaan_multi(tgl_catat.isoformat(), map_nama_ke_id[karyawan_pilih], daftar_barang_final, user["id_user"])
                        st.success("Data berhasil dimasukkan ke sistem!")
                        st.date_input("Tanggal Catat (YYYY-MM-DD)", date.today()) # pemicu refresh form
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                        
            with b_col2:
                st.markdown('<div class="dashboard-panel" style="border-color:#444444 !important;">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: #FFFFFF; margin-top:0;'>📜 Riwayat Barang Bawaan</h3>", unsafe_allow_html=True)
                riwayat_b = db.ambil_semua_barang_bawaan()
                for rb in riwayat_b[:12]:
                    st.markdown(
                        f"<div style='background-color:#1E1E1E; padding:10px; border-radius:6px; border-left: 3px solid #FF9800; margin-bottom:8px; font-size:12px;'>"
                        f"<b>{rb['tgl_catat']} • {rb['nama_karyawan']}</b><br>"
                        f"<span style='color:#AAAAAA;'>{rb['nama_barang']} (Bawa:{rb['jumlah_dibawa']} | Kembali:{rb['jumlah_kembali']})</span><br>"
                        f"<span style='color:#FF9800; font-weight:bold;'>Omset: Rp {rb['nilai_omset']:,.0f}</span>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 3: Form Input Pengeluaran
        # ----------------------------------------------------------------------
        with tab_pengeluaran:
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: #D32F2F; margin-top:0;'>💸 Input Pengeluaran Baru</h3>", unsafe_allow_html=True)
                tgl_peng = st.date_input("Tanggal Pengeluaran", date.today())
                kat_biaya = st.selectbox("Kategori Biaya", ["Bahan Baku", "Energi", "Operasional"])
                nama_item = st.text_input("Nama Barang / Kegiatan", placeholder="Contoh: Daging, Bensin Pegawai")
                nominal = st.number_input("Nominal Pengeluaran (Rp)", min_value=0.0, step=5000.0)
                
                foto_nota = st.file_uploader("Upload Foto Nota", type=["png", "jpg", "jpeg"])
                path_nota = ""
                if foto_nota:
                    path_nota = os.path.join("nota_uploads", foto_nota.name)
                    os.makedirs("nota_uploads", exist_ok=True)
                    with open(path_nota, "wb") as f: f.write(foto_nota.getbuffer())
                st.write("")
                
                if st.button("Simpan Pengeluaran"):
                    if not nama_item or nominal <= 0:
                        st.error("Lengkapi formulir pengeluaran dengan benar.")
                    else:
                        db.tambah_pengeluaran(tgl_peng.isoformat(), kat_biaya, nama_item, nominal, path_nota, user["id_user"])
                        st.success("Data pengeluaran berhasil disimpan.")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with p_col2:
                st.markdown('<div class="dashboard-panel" style="border-color:#444444 !important;">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: #FFFFFF; margin-top:0;'>📜 Riwayat Pengeluaran</h3>", unsafe_allow_html=True)
                riwayat_p = db.ambil_semua_pengeluaran()
                for rp in riwayat_p[:12]:
                    nota_lbl = "📎 ada nota" if rp["foto_nota"] else "tanpa nota"
                    st.markdown(
                        f"<div style='background-color:#1E1E1E; padding:10px; border-radius:6px; border-left: 3px solid #D32F2F; margin-bottom:8px; font-size:12px;'> "
                        f"<b>{rp['tgl_pengeluaran']} • {rp['kategori_biaya']}</b><br>"
                        f"<span style='color:#AAAAAA;'>Item: {rp['nama_item']} ({nota_lbl})</span><br>"
                        f"<span style='color:#D32F2F; font-weight:bold;'>Rp {rp['nominal_biaya']:,.0f}</span>"
                        f"</div>", unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Tab 4: Ekspor Laporan Laba Rugi
        # ----------------------------------------------------------------------
        with tab_ekspor:
            st.markdown('<div class="dashboard-panel" style="max-width: 600px;">', unsafe_allow_html=True)
            st.markdown("<h3 style='color: #D32F2F; margin-top:0;'>📁 Laporan Laba Rugi Bulanan</h3>", unsafe_allow_html=True)
            bulan_ekspor = st.text_input("Pilih Bulan (YYYY-MM)", value=date.today().strftime("%Y-%m"))
            
            if bulan_ekspor:
                rekap = db.rekap_laba_rugi_bulan(bulan_ekspor)
                st.markdown(
                    f"<div class='metric-card' style='font-family: monospace; font-size:13px; background-color:#1E1E1E !important; border:1px solid #333 !important; white-space: pre;'>"
                    f"Bulan          : {rekap['bulan']}\n"
                    f"Pendapatan     : Rp {rekap['total_pendapatan']:,.0f}\n"
                    f"Pengeluaran    : Rp {rekap['total_pengeluaran']:,.0f}\n"
                    f"Gaji Karyawan  : Rp {rekap['total_gaji']:,.0f}\n"
                    f"-----------------------------------------\n"
                    f"LABA / RUGI    : Rp {rekap['laba_bersih']:,.0f}"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
                txt_data = (
                    f"==========================================\n"
                    f"   LAPORAN LABA RUGI - BAKSO MAENYOS\n"
                    f"   Periode: {rekap['bulan']}\n"
                    f"==========================================\n\n"
                    f"Total Pendapatan              : Rp {rekap['total_pendapatan']:,.0f}\n"
                    f"Total Pengeluaran Operasional : Rp {rekap['total_pengeluaran']:,.0f}\n"
                    f"Total Gaji Harian Karyawan    : Rp {rekap['total_gaji']:,.0f}\n"
                    f"------------------------------------------\n"
                    f"LABA / RUGI BERSIH            : Rp {rekap['laba_bersih']:,.0f}\n"
                )
                
                st.download_button(
                    label="Ekspor sebagai .TXT",
                    data=txt_data,
                    file_name=f"Laporan_LabaRugi_{bulan_ekspor}.txt",
                    mime="text/plain"
                )
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================================
    # B. DASHBOARD ROLE: KARYAWAN (Lihat-Saja)
    # ==========================================================================
    else:
        st.markdown(f"<h2 style='color:white; margin-bottom:0;'>Halo, {user['nama']} 👋</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-muted' style='font-size:13px; color:#FF9800 !important;'>Halaman bersifat lihat-saja (read-only). Seluruh data dikelola oleh Pemilik.</p>", unsafe_allow_html=True)
        st.write("")
        
        k_col1, k_col2 = st.columns([1, 1.3])
        
        with k_col1:
            st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#FF9800; margin-top:0;'>🍊 Notifikasi Gaji Transparan</h3>", unsafe_allow_html=True)
            daftar_gaji = db.ambil_gaji_by_user(user["id_user"])
            
            if not daftar_gaji:
                st.text("Belum ada slip gaji harian masuk.")
            else:
                total_gaji_k = sum(g["jumlah_gaji"] for g in daftar_gaji)
                st.markdown(f"<div class='metric-card' style='border-color:#4CAF50 !important;'><span class='text-muted'>Total Gaji Terkumpul:</span><br><h2 style='color:#4CAF50; margin:0;'>Rp {total_gaji_k:,.0f}</h2></div>", unsafe_allow_html=True)
                
                for gaji in daftar_gaji[:10]:
                    st.markdown(
                        f"<div style='background-color:#1E1E1E; padding:10px; margin-bottom:6px; border-radius:6px; border-left:3px solid #4CAF50; font-size:13px;'>"
                        f"📅 {gaji['tgl_gaji']} <b style='color:white; float:right;'>Rp {gaji['jumlah_gaji']:,.0f}</b>"
                        f"</div>", unsafe_allow_html=True
                    )
            st.markdown('</div>', unsafe_allow_html=True)
                    
        with k_col2:
            st.markdown('<div class="dashboard-panel" style="border-color:#444444 !important;">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:white; margin-top:0;'>📦 Riwayat Performa & Barang Bawaan</h3>", unsafe_allow_html=True)
            riwayat_k = db.ambil_barang_by_user(user["id_user"])
            
            if not riwayat_k:
                st.text("Belum ada riwayat distribusi barang.")
            else:
                for rk in riwayat_k:
                    gaji_per_item = rk["nilai_omset"] * db.PERSENTASE_GAJI
                    st.markdown(
                        f"<div style='background-color:#1E1E1E; padding:12px; border-radius:6px; margin-bottom:8px; font-size:12px; border-left:1px solid #555;'>"
                        f"<b>Tanggal: {rk['tgl_catat']} | Item: {rk['nama_barang']}</b><br>"
                        f"<span style='color:#AAAAAA;'>Bawa: {rk['jumlah_dibawa']} • Jual: {rk['jumlah_terjual']} • Sisa: {rk['jumlah_kembali']}</span><br>"
                        f"Omset: Rp {rk['nilai_omset']:,.0f} | <b style='color:#4CAF50;'>Gaji: Rp {gaji_per_item:,.0f}</b>"
                        f"</div>", unsafe_allow_html=True
                    )
            st.markdown('</div>', unsafe_allow_html=True)
