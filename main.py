import streamlit as st
import database as db
from datetime import date
import matplotlib
import os

# Set Konfigurasi Halaman & Tema Visual Dasar
st.set_page_config(
    page_title="SIKU - Sistem Informasi Keuangan UMKM",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KUSTOMISASI VISUAL (Meniru tema dark mode merah-oranye dari desktop)
CUSTOM_CSS = """
<style>
    /* Mengubah latar belakang utama */
    .stApp {
        background-color: #1A1A1A;
        color: #FFFFFF;
    }
    /* Mengubah latar belakang Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333333;
    }
    /* Styling Kartu Profil & Metrik Keuangan */
    .metric-card {
        background-color: #242424;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    /* Tombol Utama (Merah Kuliner) */
    div.stButton > button:first-child {
        background-color: #D32F2F;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #B71C1C;
        border: none;
        color: white;
    }
    /* Form input styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #2D2D2D !important;
        color: white !important;
        border-color: #FF9800 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Pastikan database terinisialisasi
db.init_db()

# Inisialisasi Session State Pengguna
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# ==========================================
# HALAMAN LOGIN
# ==========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: center; color: #D32F2F; margin-bottom:0;'>🍜 SIKU</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888888; font-size:14px; margin-top:0;'>Sistem Informasi Keuangan UMKM</p>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #FF9800;'>Bakso Maenyos</h4>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Masuk")
            
            if submitted:
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
                        
        # Fitur Lupa Password terintegrasi secara modular
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
                            sukses = db.reset_password_via_keamanan(user_lupa, jawaban, pw_baru)
                            if sukses:
                                st.success("Password berhasil diperbarui! Silakan login.")
                            else:
                                st.error("Jawaban keamanan salah.")
                else:
                    st.error("Username tidak ditemukan atau tidak memiliki pertanyaan keamanan.")

# ==========================================
# DASHBOARD SETELAH LOGIN SUKSES
# ==========================================
else:
    user = st.session_state.user
    
    # --- SIDEBAR GLOBAL ---
    st.sidebar.markdown(f"<h2 style='color: #D32F2F; margin-bottom: 0;'>🍜 SIKU</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: #888888; font-size: 11px;'>Bakso Maenyos</p>", unsafe_allow_html=True)
    
    # Kartu Identitas Pengguna
    st.sidebar.markdown(
        f"<div class='metric-card' style='padding:12px; margin-bottom: 20px;'>"
        f"<b style='color: #FFFFFF;'>{user['nama']}</b><br>"
        f"<span style='color: #FF9800; font-size:12px;'>Role: {user['role']}</span>"
        f"</div>", 
        unsafe_allow_html=True
    )
    
    # Fitur Ganti Password Terintegrasi di Sidebar
    with st.sidebar.expander("🔒 Ganti Password"):
        pw_lama = st.text_input("Password Lama", type="password", key="chg_old")
        pw_baru_profile = st.text_input("Password Baru", type="password", key="chg_new")
        pw_konf_profile = st.text_input("Konfirmasi Password", type="password", key="chg_conf")
        if st.button("Simpan Password Baru"):
            if pw_baru_profile != pw_konf_profile:
                st.error("Konfirmasi tidak cocok.")
            elif len(pw_baru_profile) < 6:
                st.error("Minimal 6 karakter.")
            else:
                if db.ubah_password(user["id_user"], pw_lama, pw_baru_profile):
                    st.success("Password berhasil diubah!")
                else:
                    st.error("Password lama salah.")
                    
    if st.sidebar.button("Keluar / Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # --- KONTEN ROLE-BASED ACCESS CONTROL (RBAC) ---
    
    # ----------------------------------------------------
    # DASHBOARD PEMILIK (AKSES PENULISAN & FINANSIAL FULL)
    # ----------------------------------------------------
    if user["role"] == "Pemilik":
        tab_dasbor, tab_barang, tab_pengeluaran, tab_ekspor = st.tabs([
            "📊 Dasbor Finansial", "📦 Input Barang Bawaan", "💸 Input Pengeluaran", "📁 Ekspor Laporan"
        ])
        
        # 1. TAB DASBOR REAL-TIME FINANSIAL
        with tab_dasbor:
            st.markdown("<h3 style='color: #FFFFFF;'>Ringkasan Finansial Real-time</h3>", unsafe_allow_html=True)
            
            omset_data = db.rekap_omset_per_tanggal()
            pengeluaran_data = db.rekap_pengeluaran_per_tanggal()
            
            total_omset = sum(nilai for _, nilai in omset_data)
            total_pengeluaran = sum(nilai for _, nilai in pengeluaran_data)
            laba_bersih = total_omset - total_pengeluaran
            
            # Kartu Metrik Visual
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"<div class='metric-card'><span style='color: #888888; font-size: 12px;'>Total Pendapatan (Verified)</span><br><h2 style='color: #4CAF50; margin:0;'>Rp {total_omset:,.0f}</h2></div>", unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"<div class='metric-card'><span style='color: #888888; font-size: 12px;'>Total Pengeluaran</span><br><h2 style='color: #F44336; margin:0;'>Rp {total_pengeluaran:,.0f}</h2></div>", unsafe_allow_html=True)
            with m_col3:
                warna_laba = "#4CAF50" if laba_bersih >= 0 else "#F44336"
                st.markdown(f"<div class='metric-card'><span style='color: #888888; font-size: 12px;'>Estimasi Laba Bersih</span><br><h2 style='color: {warna_laba}; margin:0;'>Rp {laba_bersih:,.0f}</h2></div>", unsafe_allow_html=True)
            
            # Tren Grafik menggunakan Matplotlib Terintegrasi
            st.markdown("##### 📈 Tren Pendapatan vs Pengeluaran")
            from matplotlib.figure import Figure
            
            semua_tanggal = sorted(set([t for t, _ in omset_data] + [t for t, _ in pengeluaran_data]))
            map_omset = dict(omset_data)
            map_pengeluaran = dict(pengeluaran_data)
            y_omset = [map_omset.get(t, 0) for t in semua_tanggal]
            y_pengeluaran = [map_pengeluaran.get(t, 0) for t in semua_tanggal]
            
            fig = Figure(figsize=(10, 3.5), facecolor="#242424")
            ax = fig.add_subplot(111)
            ax.set_facecolor("#242424")
            
            if not semua_tanggal:
                ax.text(0.5, 0.5, "Belum ada data transaksi", ha="center", va="center", color="#888888", transform=ax.transAxes)
            else:
                ax.plot(semua_tanggal, y_omset, marker="o", color="#FF9800", linewidth=2.2, label="Pendapatan")
                ax.plot(semua_tanggal, y_pengeluaran, marker="o", color="#D32F2F", linewidth=2.2, label="Pengeluaran")
                ax.legend(facecolor="#242424", edgecolor="#242424", labelcolor="white", loc="upper left")
                ax.tick_params(axis="x", colors="#888888", labelsize=8, rotation=20)
                ax.tick_params(axis="y", colors="#888888", labelsize=8)
            
            for spine in ax.spines.values():
                spine.set_color("#333333")
            fig.tight_layout()
            st.pyplot(fig)

        # 2. TAB INPUT BARANG BAWAAN (DYNAMIC DATA EDITOR MENGGANTIKAN DYNAMIC ROWS DARI DESKTOP)
        with tab_barang:
            st.markdown("<h3 style='color: #D32F2F;'>📦 Input Barang Bawaan Karyawan</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #888888; font-size:12px;'>Gaji otomatis terhitung {db.PERSENTASE_GAJI*100:.1f}% dari omset.</p>", unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns([1.2, 1])
            with b_col1:
                daftar_karyawan = db.ambil_daftar_karyawan()
                map_nama_ke_id = {f"{k['nama']} ({k['username']})": k["id_user"] for k in daftar_karyawan}
                
                karyawan_pilih = st.selectbox("Pilih Karyawan", options=list(map_nama_ke_id.keys()))
                tgl_catat = st.date_input("Tanggal Catat", date.today())
                
                st.markdown("**Daftar Items Barang (Isi Jumlah Dibawa dan Kembali):**")
                
                # Menggunakan st.data_editor untuk replikasi Dynamic Add/Delete Rows Excel yang instan
                init_df = [{"Nama Barang": list(db.MASTER_BARANG.keys())[0], "Jumlah Dibawa": 0, "Jumlah Kembali": 0}]
                edited_df = st.data_editor(
                    init_df, 
                    num_rows="dynamic", 
                    column_config={
                        "Nama Barang": st.column_config.SelectboxColumn(options=list(db.MASTER_BARANG.keys()), required=True),
                        "Jumlah Dibawa": st.column_config.NumberColumn(min_value=0, default=0, required=True),
                        "Jumlah Kembali": st.column_config.NumberColumn(min_value=0, default=0, required=True)
                    },
                    key="editor_barang"
                )
                
                # Hitung Ringkasan Live Preview sebelum disimpan
                preview_omset = 0.0
                daftar_barang_final = []
                valid = True
                
                for row in edited_df:
                    nb = row.get("Nama Barang")
                    dbw = row.get("Jumlah Dibawa", 0)
                    kmb = row.get("Jumlah Kembali", 0)
                    
                    if kmb > dbw:
                        st.error(f"Kesalahan pada item {nb}: Jumlah kembali melebihi jumlah dibawa.")
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
                
                st.markdown(f"**Total Omset Harian:** <span style='color:#FF9800;'>Rp {preview_omset:,.0f}</span>", unsafe_allow_html=True)
                st.markdown(f"**Estimasi Gaji Karyawan:** <span style='color:#4CAF50;'>Rp {preview_omset*db.PERSENTASE_GAJI:,.0f}</span>", unsafe_allow_html=True)
                
                if st.button("💾 Simpan & Hitung Gaji Otomatis") and valid:
                    if not daftar_barang_final:
                        st.warning("Minimal harus ada 1 baris barang.")
                    else:
                        db.tambah_barang_bawaan_multi(
                            tgl_catat=tgl_catat.isoformat(),
                            id_user=map_nama_ke_id[karyawan_pilih],
                            daftar_barang=daftar_barang_final,
                            id_user_pencatat=user["id_user"]
                        )
                        st.success("✅ Seluruh jenis barang dan Gaji Harian berhasil disimpan!")
                        st.rerun()
                        
            with b_col2:
                st.markdown("##### 📜 Riwayat Barang Bawaan Terakhir")
                riwayat_b = db.ambil_semua_barang_bawaan()
                for rb in riwayat_b[:10]:
                    st.markdown(
                        f"<div style='background-color:#2D2D2D; padding:8px; border-radius:6px; margin-bottom:6px; font-size:12px;'>"
                        f"<b>{rb['tgl_catat']} • {rb['nama_karyawan']}</b><br>"
                        f"{rb['nama_barang']} | Dibawa: {rb['jumlah_dibawa']} Terjual: {rb['jumlah_terjual']}<br>"
                        f"<span style='color:#FF9800;'>Omset: Rp {rb['nilai_omset']:,.0f}</span>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )

        # 3. TAB INPUT PENGELUARAN
        with tab_pengeluaran:
            st.markdown("<h3 style='color: #D32F2F;'>💸 Input Pengeluaran Baru</h3>", unsafe_allow_html=True)
            p_col1, p_col2 = st.columns(2)
            
            with p_col1:
                tgl_peng = st.date_input("Tanggal Pengeluaran", date.today())
                kat_biaya = st.selectbox("Kategori Biaya", ["Bahan Baku", "Energi", "Operasional"])
                nama_item = st.text_input("Nama Barang / Kegiatan", placeholder="Contoh: Daging, Bensin Pegawai")
                nominal = st.number_input("Nominal Pengeluaran (Rp)", min_value=0.0, step=1000.0)
                
                # Pengganti FileDialog Desktop Ke Web File Uploader
                foto_nota = st.file_uploader("Upload Foto Nota (Optional)", type=["png", "jpg", "jpeg"])
                path_nota = ""
                if foto_nota:
                    path_nota = os.path.join("nota_uploads", foto_nota.name)
                    # Simpan file nota secara lokal di direktori server
                    os.makedirs("nota_uploads", exist_ok=True)
                    with open(path_nota, "wb") as f:
                        f.write(foto_nota.getbuffer())
                
                if st.button("Simpan Pengeluaran"):
                    if not nama_item or nominal <= 0:
                        st.error("Nama item dan nominal wajib diisi dengan benar.")
                    else:
                        db.tambah_pengeluaran(tgl_peng.isoformat(), kat_biaya, nama_item, nominal, path_nota, user["id_user"])
                        st.success("Data pengeluaran berhasil disimpan.")
                        st.rerun()
            
            with p_col2:
                st.markdown("##### 📜 Riwayat Pengeluaran")
                riwayat_p = db.ambil_semua_pengeluaran()
                for rp in riwayat_p[:10]:
                    nota_lbl = "📎 ada nota" if rp["foto_nota"] else "tanpa nota"
                    st.markdown(
                        f"<div style='background-color:#2D2D2D; padding:8px; border-radius:6px; margin-bottom:6px; font-size:12px;'> "
                        f"<b>{rp['tgl_pengeluaran']} • {rp['kategori_biaya']} • {rp['nama_item']}</b><br>"
                        f"<span style='color:#FF9800;'>Rp {rp['nominal_biaya']:,.0f}</span> ({nota_lbl})"
                        f"</div>", unsafe_allow_html=True
                    )

        # 4. TAB EKSPOR LAPORAN LABA RUGI
        with tab_ekspor:
            st.markdown("<h3 style='color: #D32F2F;'>📁 Ekspor Laporan Laba Rugi Bulanan</h3>", unsafe_allow_html=True)
            bulan_ekspor = st.text_input("Pilih Bulan (Format YYYY-MM)", value=date.today().strftime("%Y-%m"))
            
            if bulan_ekspor:
                rekap = db.rekap_laba_rugi_bulan(bulan_ekspor)
                
                st.markdown(
                    f"<div class='metric-card' style='font-family: monospace; font-size:14px; white-space: pre;'>"
                    f"Bulan          : {rekap['bulan']}\n"
                    f"Pendapatan     : Rp {rekap['total_pendapatan']:,.0f}\n"
                    f"Pengeluaran    : Rp {rekap['total_pengeluaran']:,.0f}\n"
                    f"Gaji Karyawan  : Rp {rekap['total_gaji']:,.0f}\n"
                    f"-----------------------------------------\n"
                    f"Laba Bersih    : Rp {rekap['laba_bersih']:,.0f}"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
                # Download Button Menggantikan SaveAs Dialong Desktop
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

    # ----------------------------------------------------
    # DASHBOARD KARYAWAN (AKSES READ-ONLY PENUH)
    # ----------------------------------------------------
    else:
        st.markdown(f"<h2 style='color:white;'>Halo, {user['nama']} 👋</h2>", unsafe_allow_html=True)
        st.info("Halaman ini bersifat lihat-saja (read-only). Seluruh pencatatan dilakukan oleh Pemilik.")
        
        k_col1, k_col2 = st.columns([1, 1.2])
        
        with k_col1:
            st.markdown("<h4 style='color:#FF9800;'>🍊 Notifikasi Gaji Transparan</h4>", unsafe_allow_html=True)
            daftar_gaji = db.ambil_gaji_by_user(user["id_user"])
            
            if not daftar_gaji:
                st.text("Belum ada gaji yang tercatat.")
            else:
                total_gaji_k = sum(g["jumlah_gaji"] for g in daftar_gaji)
                st.markdown(f"**Total Gaji Terkumpul:** <span style='color:#4CAF50; font-size:18px; font-weight:bold;'>Rp {total_gaji_k:,.0f}</span>", unsafe_allow_html=True)
                
                for gaji in daftar_gaji[:10]:
                    st.markdown(
                        f"<div style='background-color:#2D2D2D; padding:10px; border-radius:6px; margin-bottom:5px; display:flex; justify-content:space-between;'>"
                        f"<span>📅 {gaji['tgl_gaji']}</span>"
                        f"<b style='color:white;'>Rp {gaji['jumlah_gaji']:,.0f}</b>"
                        f"</div>", unsafe_allow_html=True
                    )
                    
        with k_col2:
            st.markdown("#### 📦 Riwayat Barang Bawaan & Performa Saya")
            riwayat_k = db.ambil_barang_by_user(user["id_user"])
            
            if not riwayat_k:
                st.text("Belum ada riwayat barang.")
            else:
                for rk in riwayat_k:
                    gaji_per_item = rk["nilai_omset"] * db.PERSENTASE_GAJI
                    st.markdown(
                        f"<div style='background-color:#2D2D2D; padding:10px; border-radius:6px; margin-bottom:5px; font-size:13px;'>"
                        f"<b>Tanggal: {rk['tgl_catat']} | Barang: {rk['nama_barang']}</b><br>"
                        f"Bawa: {rk['jumlah_dibawa']} • Terjual: {rk['jumlah_terjual']} • Kembali: {rk['jumlah_kembali']}<br>"
                        f"Omset: Rp {rk['nilai_omset']:,.0f} | <span style='color:#4CAF50;'>Gaji: Rp {gaji_per_item:,.0f}</span>"
                        f"</div>", unsafe_allow_html=True
                    )
