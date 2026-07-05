import sqlite3
import hashlib
import os

# REVISI: Disesuaikan langsung ke nama file lokal root untuk kompabilitas cloud hosting
DB_NAME = "moniva.db"

PERSENTASE_GAJI = 0.175

MASTER_BARANG = {
    "Mie": 2000,
    "Pangsit Mekar": 2000,
    "Tahu": 2000,
    "Siomay": 2000,
    "Bakso Halus": 1500,
    "Bakso Urat": 3000,
    "Bakso Cincang": 6000,
}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_user (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nama TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Karyawan', 'Pemilik')),
            pertanyaan_keamanan TEXT,
            jawaban_keamanan TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_setoran_harian (
            id_setoran INTEGER PRIMARY KEY AUTOINCREMENT,
            tgl_setoran TEXT NOT NULL,
            nominal_setoran REAL NOT NULL,
            status_setoran TEXT NOT NULL DEFAULT 'Pending' CHECK(status_setoran IN ('Pending', 'Verified')),
            id_user INTEGER NOT NULL,
            FOREIGN KEY (id_user) REFERENCES tb_user(id_user)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_barang_bawaan (
            id_barang INTEGER PRIMARY KEY AUTOINCREMENT,
            tgl_catat TEXT NOT NULL,
            id_user INTEGER NOT NULL,
            nama_barang TEXT NOT NULL,
            harga_satuan REAL NOT NULL DEFAULT 0,
            jumlah_dibawa INTEGER NOT NULL,
            jumlah_terjual INTEGER NOT NULL,
            jumlah_kembali INTEGER NOT NULL,
            nilai_omset REAL NOT NULL,
            id_user_pencatat INTEGER NOT NULL,
            id_sesi_input INTEGER,
            FOREIGN KEY (id_user) REFERENCES tb_user(id_user),
            FOREIGN KEY (id_user_pencatat) REFERENCES tb_user(id_user)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_gaji_harian (
            id_gaji INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_setoran INTEGER,
            id_barang INTEGER,
            id_sesi_input INTEGER,
            tgl_gaji TEXT NOT NULL,
            total_omset REAL NOT NULL,
            jumlah_gaji REAL NOT NULL,
            FOREIGN KEY (id_user) REFERENCES tb_user(id_user),
            FOREIGN KEY (id_setoran) REFERENCES tb_setoran_harian(id_setoran),
            FOREIGN KEY (id_barang) REFERENCES tb_barang_bawaan(id_barang)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tb_pengeluaran (
            id_pengeluaran INTEGER PRIMARY KEY AUTOINCREMENT,
            tgl_pengeluaran TEXT NOT NULL,
            kategori_biaya TEXT NOT NULL,
            nama_item TEXT NOT NULL DEFAULT '',
            nominal_biaya REAL NOT NULL,
            foto_nota TEXT,
            id_user INTEGER NOT NULL,
            FOREIGN KEY (id_user) REFERENCES tb_user(id_user)
        )
    """)
    conn.commit()

    # Cek Seed data dummy
    pertanyaan_default = "Apa nama hewan peliharaan favorit Anda?"
    daftar_user_default = [
        ("davahaidar", hash_password("1933"), "Dava (Pemilik)", "Pemilik", pertanyaan_default, hash_password("kucing")),
        ("budi_karyawan", hash_password("budi123"), "Budi Santoso", "Karyawan", pertanyaan_default, hash_password("rocky")),
        ("siti_karyawan", hash_password("siti123"), "Siti Aminah", "Karyawan", pertanyaan_default, hash_password("milo")),
        ("joko_karyawan", hash_password("joko123"), "Joko Widodo", "Karyawan", pertanyaan_default, hash_password("kancil")),
        ("rina_karyawan", hash_password("rina123"), "Rina Wulandari", "Karyawan", pertanyaan_default, hash_password("kelinci")),
        ("agus_karyawan", hash_password("agus123"), "Agus Setiawan", "Karyawan", pertanyaan_default, hash_password("harimau")),
    ]

    # REVISI: cek per-username (bukan hanya total==0) supaya user baru tetap
    # otomatis ditambahkan meski database lama (yang sudah berisi user lain) sudah ada
    for username, password, nama, role, pertanyaan, jawaban in daftar_user_default:
        ada = cur.execute("SELECT 1 FROM tb_user WHERE username = ?", (username,)).fetchone()
        if ada is None:
            cur.execute(
                """INSERT INTO tb_user (username, password, nama, role, pertanyaan_keamanan, jawaban_keamanan) VALUES (?, ?, ?, ?, ?, ?)""",
                (username, password, nama, role, pertanyaan, jawaban)
            )
    conn.commit()
    conn.close()

def tambah_user(username: str, password: str, nama: str, role: str, pertanyaan_keamanan: str = "", jawaban_keamanan: str = "") -> bool:
    """Menambah user baru secara manual (mis. dari halaman admin). Return False jika username sudah dipakai."""
    conn = get_connection()
    ada = conn.execute("SELECT 1 FROM tb_user WHERE username = ?", (username,)).fetchone()
    if ada is not None:
        conn.close()
        return False
    conn.execute(
        """INSERT INTO tb_user (username, password, nama, role, pertanyaan_keamanan, jawaban_keamanan) VALUES (?, ?, ?, ?, ?, ?)""",
        (username, hash_password(password), nama, role, pertanyaan_keamanan, hash_password(jawaban_keamanan.strip().lower()) if jawaban_keamanan else "")
    )
    conn.commit()
    conn.close()
    return True

def verifikasi_login(username: str, password: str):
    conn = get_connection()
    user = conn.execute("SELECT * FROM tb_user WHERE username = ? AND password = ?", (username, hash_password(password))).fetchone()
    conn.close()
    return user

def ambil_pertanyaan_keamanan(username: str):
    conn = get_connection()
    user = conn.execute("SELECT pertanyaan_keamanan FROM tb_user WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user["pertanyaan_keamanan"] if user else None

def verifikasi_jawaban_keamanan(username: str, jawaban: str) -> bool:
    conn = get_connection()
    user = conn.execute("SELECT jawaban_keamanan FROM tb_user WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user["jawaban_keamanan"] == hash_password(jawaban.strip().lower()) if user else False

def reset_password_via_keamanan(username: str, jawaban: str, password_baru: str) -> bool:
    if not verifikasi_jawaban_keamanan(username, jawaban): return False
    conn = get_connection()
    conn.execute("UPDATE tb_user SET password = ? WHERE username = ?", (hash_password(password_baru), username))
    conn.commit()
    conn.close()
    return True

def ubah_password(id_user: int, password_lama: str, password_baru: str) -> bool:
    conn = get_connection()
    user = conn.execute("SELECT password FROM tb_user WHERE id_user = ?", (id_user,)).fetchone()
    if user is None or user["password"] != hash_password(password_lama):
        conn.close()
        return False
    conn.execute("UPDATE tb_user SET password = ? WHERE id_user = ?", (hash_password(password_baru), id_user))
    conn.commit()
    conn.close()
    return True

def tambah_barang_bawaan_multi(tgl_catat: str, id_user: int, daftar_barang: list, id_user_pencatat: int):
    conn = get_connection()
    total_omset_sesi = 0.0
    id_barang_pertama = None

    for barang in daftar_barang:
        conn.execute(
            """INSERT INTO tb_barang_bawaan (tgl_catat, id_user, nama_barang, harga_satuan, jumlah_dibawa, jumlah_terjual, jumlah_kembali, nilai_omset, id_user_pencatat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (tgl_catat, id_user, barang["nama_barang"], barang["harga_satuan"], barang["jumlah_dibawa"], barang["jumlah_terjual"], barang["jumlah_kembali"], barang["nilai_omset"], id_user_pencatat)
        )
        id_baru = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        if id_barang_pertama is None: id_barang_pertama = id_baru
        total_omset_sesi += barang["nilai_omset"]

    jumlah_gaji = total_omset_sesi * PERSENTASE_GAJI
    conn.execute("""INSERT INTO tb_gaji_harian (id_user, id_barang, tgl_gaji, total_omset, jumlah_gaji) VALUES (?, ?, ?, ?, ?)""", (id_user, id_barang_pertama, tgl_catat, total_omset_sesi, jumlah_gaji))
    conn.commit()
    conn.close()

def ambil_barang_by_user(id_user: int):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tb_barang_bawaan WHERE id_user = ? ORDER BY tgl_catat DESC", (id_user,)).fetchall()
    conn.close()
    return rows

def ambil_semua_barang_bawaan():
    conn = get_connection()
    rows = conn.execute("""SELECT b.*, u.nama AS nama_karyawan FROM tb_barang_bawaan b JOIN tb_user u ON b.id_user = u.id_user ORDER BY b.tgl_catat DESC""").fetchall()
    conn.close()
    return rows

def ambil_daftar_karyawan():
    conn = get_connection()
    rows = conn.execute("SELECT id_user, nama, username FROM tb_user WHERE role = 'Karyawan' ORDER BY nama ASC").fetchall()
    conn.close()
    return rows

def ambil_gaji_by_user(id_user: int):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tb_gaji_harian WHERE id_user = ? ORDER BY tgl_gaji DESC", (id_user,)).fetchall()
    conn.close()
    return rows

def tambah_pengeluaran(tgl_pengeluaran: str, kategori_biaya: str, nama_item: str, nominal_biaya: float, foto_nota: str, id_user: int):
    conn = get_connection()
    conn.execute("""INSERT INTO tb_pengeluaran (tgl_pengeluaran, kategori_biaya, nama_item, nominal_biaya, foto_nota, id_user) VALUES (?, ?, ?, ?, ?, ?)""", (tgl_pengeluaran, kategori_biaya, nama_item, nominal_biaya, foto_nota, id_user))
    conn.commit()
    conn.close()

def ambil_semua_pengeluaran():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tb_pengeluaran ORDER BY tgl_pengeluaran DESC").fetchall()
    conn.close()
    return rows

def rekap_omset_per_tanggal():
    conn = get_connection()
    rows = conn.execute("SELECT tgl_catat AS tanggal, SUM(nilai_omset) AS total FROM tb_barang_bawaan GROUP BY tgl_catat ORDER BY tgl_catat ASC").fetchall()
    conn.close()
    return [(r["tanggal"], r["total"]) for r in rows]

def rekap_pengeluaran_per_tanggal():
    conn = get_connection()
    rows = conn.execute("SELECT tgl_pengeluaran AS tanggal, SUM(nominal_biaya) AS total FROM tb_pengeluaran GROUP BY tgl_pengeluaran ORDER BY tgl_pengeluaran ASC").fetchall()
    conn.close()
    return [(r["tanggal"], r["total"]) for r in rows]

def rekap_laba_rugi_bulan(bulan: str):
    conn = get_connection()
    total_pendapatan = conn.execute("SELECT COALESCE(SUM(nilai_omset), 0) AS total FROM tb_barang_bawaan WHERE tgl_catat LIKE ?", (f"{bulan}%",)).fetchone()["total"]
    total_pengeluaran = conn.execute("SELECT COALESCE(SUM(nominal_biaya), 0) AS total FROM tb_pengeluaran WHERE tgl_pengeluaran LIKE ?", (f"{bulan}%",)).fetchone()["total"]
    total_gaji = conn.execute("SELECT COALESCE(SUM(jumlah_gaji), 0) AS total FROM tb_gaji_harian WHERE tgl_gaji LIKE ?", (f"{bulan}%",)).fetchone()["total"]
    conn.close()
    return {"bulan": bulan, "total_pendapatan": total_pendapatan, "total_pengeluaran": total_pengeluaran, "total_gaji": total_gaji, "laba_bersih": total_pendapatan - total_pengeluaran - total_gaji}
