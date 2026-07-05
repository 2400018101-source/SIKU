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

    # Cek & Seed data user berdasarkan database terbaru
    cur.execute("SELECT COUNT(*) AS total FROM tb_user")
    if cur.fetchone()["total"] == 0:
        pertanyaan_default = "Apa nama hewan peliharaan favorit Anda?"
        
        # Data User sesuai tabel request
        data_user = [
            ("davahaidar", hash_password("1933"), "Dava Haidar", "Pemilik", pertanyaan_default, hash_password("kucing")),
            ("budi_karyawan", hash_password("budi123"), "Budi", "Karyawan", pertanyaan_default, hash_password("budi")),
            ("siti_karyawan", hash_password("siti123"), "Siti", "Karyawan", pertanyaan_default, hash_password("siti")),
            ("joko_karyawan", hash_password("joko123"), "Joko", "Karyawan", pertanyaan_default, hash_password("joko")),
            ("rina_karyawan", hash_password("rina123"), "Rina", "Karyawan", pertanyaan_default, hash_password("rina")),
            ("agus_karyawan", hash_password("agus123"), "Agus", "Karyawan", pertanyaan_default, hash_password("agus"))
        ]
        
        cur.executemany(
            """INSERT INTO tb_user (username, password, nama, role, pertanyaan_keamanan, jawaban_keamanan) VALUES (?, ?, ?, ?, ?, ?)""",
            data_user
        )
        conn.commit()
    conn.close()
