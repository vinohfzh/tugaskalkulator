import math       # untuk fungsi matematika (sin, cos, tan, log, sqrt)
import os         # untuk operasi file dan sistem
import datetime   # untuk timestamp pada riwayat dan export


# ============================================================
# BAGIAN 0: RIWAYAT PERHITUNGAN (digunakan oleh semua modul)
# ============================================================

# List global untuk menyimpan 10 riwayat terakhir
riwayat = []

def tambah_riwayat(kategori: str, operasi: str, hasil: str):
    """
    Menambahkan entri baru ke riwayat perhitungan.
    Hanya menyimpan 10 entri terakhir.
    
    Parameters:
        kategori (str): Nama modul (Aritmatika, Suhu, dll.)
        operasi  (str): Deskripsi operasi yang dilakukan
        hasil    (str): Hasil perhitungan sebagai string
    """
    global riwayat
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entri = {
        "waktu"   : waktu,
        "kategori": kategori,
        "operasi" : operasi,
        "hasil"   : hasil
    }
    riwayat.append(entri)
    # Batasi hanya 10 entri terakhir
    if len(riwayat) > 10:
        riwayat = riwayat[-10:]


def tampilkan_riwayat():
    """Menampilkan 10 riwayat perhitungan terakhir."""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║              RIWAYAT PERHITUNGAN (10 Terakhir)           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    if not riwayat:
        print("  (Belum ada riwayat perhitungan)")
        return
    for i, entri in enumerate(riwayat, 1):
        print(f"\n  [{i}] {entri['waktu']} | {entri['kategori']}")
        print(f"      Operasi : {entri['operasi']}")
        print(f"      Hasil   : {entri['hasil']}")


# ============================================================
# BAGIAN 1: KALKULATOR ARITMATIKA
# ============================================================

# --- 1a. Operasi dasar ---

def tambah(a: float, b: float) -> float:
    """Mengembalikan hasil penjumlahan a + b."""
    return a + b

def kurang(a: float, b: float) -> float:
    """Mengembalikan hasil pengurangan a - b."""
    return a - b

def kali(a: float, b: float) -> float:
    """Mengembalikan hasil perkalian a * b."""
    return a * b

def bagi(a: float, b: float) -> float:
    """
    Mengembalikan hasil pembagian a / b.
    Menangani error pembagian dengan nol.
    """
    if b == 0:
        raise ZeroDivisionError("Pembagian dengan nol tidak diperbolehkan!")
    return a / b

def pangkat(a: float, b: float) -> float:
    """Mengembalikan hasil perpangkatan a ^ b."""
    return a ** b

def modulo(a: float, b: float) -> float:
    """
    Mengembalikan sisa bagi a % b.
    Menangani error pembagian dengan nol.
    """
    if b == 0:
        raise ZeroDivisionError("Modulo dengan nol tidak diperbolehkan!")
    return a % b

def akar_kuadrat(a: float) -> float:
    """
    Mengembalikan akar kuadrat dari a.
    Menangani error untuk bilangan negatif.
    """
    if a < 0:
        raise ValueError("Akar kuadrat dari bilangan negatif tidak terdefinisi (bilangan real)!")
    return math.sqrt(a)


# --- 1b. Operasi ilmiah ---

def sinus(a: float, satuan: str = "derajat") -> float:
    """Menghitung sin(a). Satuan bisa 'derajat' atau 'radian'."""
    if satuan == "derajat":
        a = math.radians(a)   # konversi derajat ke radian
    return math.sin(a)

def cosinus(a: float, satuan: str = "derajat") -> float:
    """Menghitung cos(a). Satuan bisa 'derajat' atau 'radian'."""
    if satuan == "derajat":
        a = math.radians(a)
    return math.cos(a)

def tangen(a: float, satuan: str = "derajat") -> float:
    """Menghitung tan(a). Satuan bisa 'derajat' atau 'radian'."""
    if satuan == "derajat":
        a = math.radians(a)
    return math.tan(a)

def logaritma(a: float) -> float:
    """
    Menghitung log10(a).
    Menangani error untuk bilangan <= 0.
    """
    if a <= 0:
        raise ValueError("Logaritma hanya terdefinisi untuk bilangan positif!")
    return math.log10(a)

def logaritma_natural(a: float) -> float:
    """
    Menghitung ln(a) / log_e(a).
    Menangani error untuk bilangan <= 0.
    """
    if a <= 0:
        raise ValueError("Logaritma natural hanya terdefinisi untuk bilangan positif!")
    return math.log(a)


# --- 1c. Evaluasi ekspresi berantai dengan precedence ---

def tokenize(ekspresi: str) -> list:
    """
    Memecah string ekspresi menjadi list token (angka dan operator).
    Contoh: "5 + 3 * 2" → ['5', '+', '3', '*', '2']
    
    Parameters:
        ekspresi (str): String ekspresi matematika
    Returns:
        list: Daftar token
    """
    token_list = []
    i = 0
    ekspresi = ekspresi.replace(" ", "")  # hapus semua spasi

    while i < len(ekspresi):
        ch = ekspresi[i]
        # Baca angka (termasuk desimal dan tanda minus di awal)
        if ch.isdigit() or ch == '.':
            j = i
            while j < len(ekspresi) and (ekspresi[j].isdigit() or ekspresi[j] == '.'):
                j += 1
            token_list.append(ekspresi[i:j])
            i = j
        elif ch in '+-*/^%':
            token_list.append(ch)
            i += 1
        else:
            raise ValueError(f"Karakter tidak dikenal: '{ch}'")
    return token_list


def evaluasi_ekspresi(ekspresi: str):
    """
    Mengevaluasi ekspresi matematika berantai dengan mematuhi
    operator precedence: ^ lebih tinggi dari * dan /, lalu + dan -.
    
    Parameters:
        ekspresi (str): String ekspresi (misal: "5 + 3 * 2 - 4 / 2")
    Returns:
        tuple: (hasil: float, langkah: str)
    """
    tokens = tokenize(ekspresi)
    
    # Konversi semua angka ke float
    # tokens[0], tokens[2], dst. adalah angka (indeks genap)
    # tokens[1], tokens[3], dst. adalah operator (indeks ganjil)
    
    # --- Tahap 1: Selesaikan ^ (pangkat) terlebih dahulu ---
    i = 1
    while i < len(tokens):
        if tokens[i] == '^':
            hasil = pangkat(float(tokens[i-1]), float(tokens[i+1]))
            # Ganti tiga elemen (a, ^, b) dengan hasilnya
            tokens[i-1:i+2] = [str(hasil)]
            i = max(1, i - 1)   # kembali satu langkah
        else:
            i += 2

    # --- Tahap 2: Selesaikan * / % ---
    langkah_detail = list(tokens)  # simpan untuk ditampilkan
    i = 1
    while i < len(tokens):
        op = tokens[i]
        if op in ('*', '/', '%'):
            a, b = float(tokens[i-1]), float(tokens[i+1])
            if op == '*':
                hasil = kali(a, b)
            elif op == '/':
                hasil = bagi(a, b)
            else:
                hasil = modulo(a, b)
            tokens[i-1:i+2] = [str(hasil)]
        else:
            i += 2

    # Bangun string langkah setelah * / diselesaikan
    langkah_str = " ".join(tokens)

    # --- Tahap 3: Selesaikan + - ---
    i = 1
    while i < len(tokens):
        op = tokens[i]
        if op == '+':
            hasil = tambah(float(tokens[i-1]), float(tokens[i+1]))
            tokens[i-1:i+2] = [str(hasil)]
        elif op == '-':
            hasil = kurang(float(tokens[i-1]), float(tokens[i+1]))
            tokens[i-1:i+2] = [str(hasil)]
        else:
            i += 2

    hasil_akhir = float(tokens[0])
    langkah_tampil = f"{langkah_str} = {hasil_akhir}"
    return hasil_akhir, langkah_tampil


# --- 1d. Menu Kalkulator Aritmatika ---

def menu_aritmatika():
    """Menu utama untuk modul Kalkulator Aritmatika."""
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║       KALKULATOR ARITMATIKA          ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Operasi Dasar                    ║")
        print("║  2. Operasi Ilmiah                   ║")
        print("║  3. Ekspresi Berantai                ║")
        print("║  0. Kembali ke Menu Utama            ║")
        print("╚══════════════════════════════════════╝")

        pilihan = input("  Pilih: ").strip()

        if pilihan == "1":
            # ---- Sub-menu Operasi Dasar ----
            print("\n  Operator yang tersedia: + - * / ^ % √")
            try:
                op = input("  Masukkan operator: ").strip()
                if op == "√":
                    # Akar kuadrat hanya butuh satu angka
                    a = float(input("  Masukkan bilangan: "))
                    hasil = akar_kuadrat(a)
                    info = f"√{a}"
                    print(f"\n  Hasil: {hasil}")
                else:
                    a = float(input("  Masukkan bilangan pertama : "))
                    b = float(input("  Masukkan bilangan kedua   : "))
                    # Pilih fungsi berdasarkan operator
                    if   op == '+': hasil = tambah(a, b);   info = f"{a} + {b}"
                    elif op == '-': hasil = kurang(a, b);   info = f"{a} - {b}"
                    elif op == '*': hasil = kali(a, b);     info = f"{a} * {b}"
                    elif op == '/': hasil = bagi(a, b);     info = f"{a} / {b}"
                    elif op == '^': hasil = pangkat(a, b);  info = f"{a} ^ {b}"
                    elif op == '%': hasil = modulo(a, b);   info = f"{a} % {b}"
                    else:
                        print("  Operator tidak dikenal!")
                        continue
                    print(f"\n  Hasil: {hasil}")
                tambah_riwayat("Aritmatika", info, str(hasil))
            except (ValueError, ZeroDivisionError) as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "2":
            # ---- Sub-menu Operasi Ilmiah ----
            print("\n  Fungsi: sin | cos | tan | log | ln")
            try:
                fungsi = input("  Masukkan fungsi: ").strip().lower()
                a = float(input("  Masukkan nilai : "))
                if fungsi in ("sin", "cos", "tan"):
                    satuan = input("  Satuan (derajat/radian) [default: derajat]: ").strip().lower()
                    if satuan not in ("derajat", "radian"):
                        satuan = "derajat"
                    if   fungsi == "sin": hasil = sinus(a, satuan)
                    elif fungsi == "cos": hasil = cosinus(a, satuan)
                    else:                 hasil = tangen(a, satuan)
                    info = f"{fungsi}({a} {satuan})"
                elif fungsi == "log":
                    hasil = logaritma(a)
                    info = f"log10({a})"
                elif fungsi == "ln":
                    hasil = logaritma_natural(a)
                    info = f"ln({a})"
                else:
                    print("  Fungsi tidak dikenal!")
                    continue
                print(f"\n  Hasil: {hasil:.6f}")
                tambah_riwayat("Ilmiah", info, f"{hasil:.6f}")
            except (ValueError, ZeroDivisionError) as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "3":
            # ---- Sub-menu Ekspresi Berantai ----
            try:
                expr = input("\n  Masukkan ekspresi: ").strip()
                hasil, langkah = evaluasi_ekspresi(expr)
                print(f"  Hasil  : {hasil}")
                print(f"  Langkah: {langkah}")
                tambah_riwayat("Ekspresi", expr, str(hasil))
            except (ValueError, ZeroDivisionError) as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "0":
            break  # kembali ke menu utama
        else:
            print("  Pilihan tidak valid. Silakan coba lagi.")


# ============================================================
# BAGIAN 2: KALKULATOR KONVERSI SUHU
# ============================================================

def celsius_ke_fahrenheit(c: float) -> float:
    """Mengkonversi Celsius ke Fahrenheit. Rumus: (C × 9/5) + 32"""
    return (c * 9 / 5) + 32

def celsius_ke_kelvin(c: float) -> float:
    """Mengkonversi Celsius ke Kelvin. Rumus: C + 273.15"""
    return c + 273.15

def celsius_ke_reaumur(c: float) -> float:
    """Mengkonversi Celsius ke Reaumur. Rumus: C × 4/5"""
    return c * 4 / 5

def fahrenheit_ke_celsius(f: float) -> float:
    """Mengkonversi Fahrenheit ke Celsius. Rumus: (F - 32) × 5/9"""
    return (f - 32) * 5 / 9

def kelvin_ke_celsius(k: float) -> float:
    """Mengkonversi Kelvin ke Celsius. Rumus: K - 273.15"""
    return k - 273.15

def reaumur_ke_celsius(r: float) -> float:
    """Mengkonversi Reaumur ke Celsius. Rumus: R × 5/4"""
    return r * 5 / 4


def konversi_suhu(nilai: float, dari: str, ke: str) -> float:
    """
    Mengkonversi suhu dari satu skala ke skala lain.
    Strategi: konversi dulu ke Celsius, lalu ke skala tujuan.
    
    Parameters:
        nilai (float): Nilai suhu asal
        dari  (str)  : Skala asal ('C', 'F', 'K', 'R')
        ke    (str)  : Skala tujuan ('C', 'F', 'K', 'R')
    Returns:
        float: Nilai suhu hasil konversi
    """
    # Langkah 1: Konversi ke Celsius terlebih dahulu
    if   dari == 'C': celsius = nilai
    elif dari == 'F': celsius = fahrenheit_ke_celsius(nilai)
    elif dari == 'K': celsius = kelvin_ke_celsius(nilai)
    elif dari == 'R': celsius = reaumur_ke_celsius(nilai)
    else: raise ValueError(f"Skala suhu tidak dikenal: {dari}")

    # Langkah 2: Konversi Celsius ke skala tujuan
    if   ke == 'C': return celsius
    elif ke == 'F': return celsius_ke_fahrenheit(celsius)
    elif ke == 'K': return celsius_ke_kelvin(celsius)
    elif ke == 'R': return celsius_ke_reaumur(celsius)
    else: raise ValueError(f"Skala suhu tidak dikenal: {ke}")


def klasifikasi_suhu(celsius: float) -> str:
    """
    Mengklasifikasikan suhu berdasarkan nilai Celsius.
    
    Returns:
        str: Kategori suhu
    """
    if   celsius <= 0:            return "Beku"
    elif 1 <= celsius <= 15:      return "Dingin"
    elif 16 <= celsius <= 25:     return "Normal"
    elif 26 <= celsius <= 35:     return "Panas"
    else:                         return "Sangat Panas"


def nama_skala(kode: str) -> str:
    """Mengembalikan nama lengkap dan simbol skala suhu."""
    mapping = {'C': 'Celsius (°C)', 'F': 'Fahrenheit (°F)',
               'K': 'Kelvin (K)',    'R': 'Reaumur (°R)'}
    return mapping.get(kode, kode)


def simbol_skala(kode: str) -> str:
    """Mengembalikan simbol skala suhu."""
    mapping = {'C': '°C', 'F': '°F', 'K': 'K', 'R': '°R'}
    return mapping.get(kode, '')


def menu_suhu():
    """Menu utama untuk modul Kalkulator Suhu."""
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║         KALKULATOR SUHU              ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Konversi Satuan                  ║")
        print("║  2. Tabel Konversi                   ║")
        print("║  3. Klasifikasi Suhu                 ║")
        print("║  0. Kembali ke Menu Utama            ║")
        print("╚══════════════════════════════════════╝")

        pilihan = input("  Pilih: ").strip()

        if pilihan == "1":
            # ---- Konversi Satuan ----
            print("\n  Skala yang tersedia: C (Celsius), F (Fahrenheit), K (Kelvin), R (Reaumur)")
            try:
                dari = input("  Dari : ").strip().upper()
                ke   = input("  Ke   : ").strip().upper()
                nilai = float(input("  Nilai: "))

                if dari not in ('C','F','K','R') or ke not in ('C','F','K','R'):
                    print("  Kode skala tidak valid!")
                    continue

                hasil = konversi_suhu(nilai, dari, ke)
                # Tentukan klasifikasi berdasarkan suhu Celsius
                celsius_val = konversi_suhu(nilai, dari, 'C')
                kelas = klasifikasi_suhu(celsius_val)

                print(f"\n  Hasil         : {hasil:.2f}{simbol_skala(ke)}")
                print(f"  Klasifikasi   : {kelas}")
                info = f"{nilai}{simbol_skala(dari)} → {nama_skala(ke)}"
                tambah_riwayat("Suhu", info, f"{hasil:.2f}{simbol_skala(ke)}")
            except ValueError as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "2":
            # ---- Tabel Konversi ----
            print("\n  Contoh: Tabel 0°C - 100°C dengan step 10°C")
            try:
                awal  = float(input("  Suhu awal (°C) : "))
                akhir = float(input("  Suhu akhir (°C): "))
                step  = float(input("  Step           : "))
                if step <= 0:
                    print("  Step harus positif!")
                    continue

                # Header tabel
                print(f"\n  {'°C':>8} {'°F':>10} {'K':>10} {'°R':>10} {'Klasifikasi':<15}")
                print("  " + "-" * 60)

                # Isi tabel
                suhu = awal
                while suhu <= akhir + 1e-9:   # 1e-9 toleransi float
                    f_val = celsius_ke_fahrenheit(suhu)
                    k_val = celsius_ke_kelvin(suhu)
                    r_val = celsius_ke_reaumur(suhu)
                    kelas = klasifikasi_suhu(suhu)
                    print(f"  {suhu:>8.1f} {f_val:>10.2f} {k_val:>10.2f} {r_val:>10.2f} {kelas:<15}")
                    suhu += step
            except ValueError as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "3":
            # ---- Klasifikasi Suhu ----
            try:
                nilai = float(input("\n  Masukkan suhu dalam °C: "))
                kelas = klasifikasi_suhu(nilai)
                print(f"  Klasifikasi: {kelas}")
                tambah_riwayat("Suhu-Klasifikasi", f"{nilai}°C", kelas)
            except ValueError:
                print("  Input tidak valid!")

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


# ============================================================
# BAGIAN 3: KALKULATOR KONVERSI BILANGAN
# ============================================================

# --- 3a. Konversi Desimal ke Basis Lain (algoritma manual) ---

DIGIT_HEX = "0123456789ABCDEF"   # karakter untuk representasi heksadesimal

def desimal_ke_basis(nilai: int, basis: int) -> tuple:
    """
    Mengkonversi bilangan desimal ke basis target menggunakan
    algoritma pembagian beruntun (manual, tanpa bin/hex/oct built-in).
    
    Parameters:
        nilai (int): Bilangan desimal non-negatif
        basis (int): Basis tujuan (2, 8, atau 16)
    Returns:
        tuple: (hasil: str, langkah: list of str)
    """
    if nilai == 0:
        return "0", ["0 / {} = 0 sisa 0".format(basis)]

    langkah = []   # menyimpan string setiap langkah pembagian
    sisa_list = [] # menyimpan sisa tiap langkah (untuk dibaca dari bawah)
    n = nilai

    # Lakukan pembagian berulang sampai hasil bagi = 0
    while n > 0:
        hasil_bagi = n // basis
        sisa = n % basis
        digit_sisa = DIGIT_HEX[sisa]   # representasi karakter (A-F untuk hex)
        langkah.append(f"  {n:>6} / {basis} = {hasil_bagi:>6} sisa {digit_sisa}  ↑")
        sisa_list.append(digit_sisa)
        n = hasil_bagi

    # Hasil dibaca dari bawah ke atas (balik list sisa)
    hasil = "".join(reversed(sisa_list))
    return hasil, langkah


def basis_ke_desimal(nilai_str: str, basis: int) -> tuple:
    """
    Mengkonversi bilangan dari basis tertentu ke desimal menggunakan
    penjumlahan perpangkatan (algoritma manual).
    
    Parameters:
        nilai_str (str): Representasi bilangan dalam basis asal
        basis     (int): Basis asal (2, 8, atau 16)
    Returns:
        tuple: (hasil: int, langkah: str)
    """
    nilai_str = nilai_str.upper().strip()
    total = 0
    n = len(nilai_str)
    detail_langkah = []

    for i, ch in enumerate(nilai_str):
        # Dapatkan nilai numerik dari karakter
        if ch.isdigit():
            angka = int(ch)
        elif 'A' <= ch <= 'F':
            angka = ord(ch) - ord('A') + 10
        else:
            raise ValueError(f"Karakter tidak valid untuk basis {basis}: '{ch}'")

        if angka >= basis:
            raise ValueError(f"Digit '{ch}' tidak valid untuk basis {basis}!")

        pangkat_val = n - 1 - i          # pangkat saat ini
        kontribusi = angka * (basis ** pangkat_val)
        total += kontribusi
        detail_langkah.append(f"{ch}×{basis}^{pangkat_val}={kontribusi}")

    langkah_str = "  " + " + ".join(detail_langkah) + f" = {total}"
    return total, langkah_str


def konversi_bilangan(nilai_str: str, dari: str, ke: str) -> tuple:
    """
    Konversi bilangan antar semua basis yang didukung.
    Strategi: konversi ke desimal dulu, lalu ke basis tujuan.
    
    Parameters:
        nilai_str (str): Nilai asal
        dari (str): 'DEC', 'BIN', 'OCT', 'HEX'
        ke   (str): 'DEC', 'BIN', 'OCT', 'HEX'
    Returns:
        tuple: (hasil: str, langkah_list: list)
    """
    basis_map = {'DEC': 10, 'BIN': 2, 'OCT': 8, 'HEX': 16}
    basis_dari = basis_map[dari]
    basis_ke   = basis_map[ke]

    semua_langkah = []

    # --- Langkah 1: Konversi ke desimal ---
    if dari == 'DEC':
        desimal = int(nilai_str)
        semua_langkah.append(f"  Nilai desimal: {desimal}")
    else:
        desimal, lk = basis_ke_desimal(nilai_str, basis_dari)
        semua_langkah.append(f"  Konversi {dari} → DEC:")
        semua_langkah.append(lk)
        semua_langkah.append(f"  = {desimal}")

    # --- Langkah 2: Konversi desimal ke basis tujuan ---
    if ke == 'DEC':
        hasil = str(desimal)
    else:
        hasil, lk2 = desimal_ke_basis(desimal, basis_ke)
        semua_langkah.append(f"\n  Konversi DEC → {ke}:")
        semua_langkah.extend(lk2)
        semua_langkah.append(f"\n  Hasil: {hasil}")

    return hasil, semua_langkah


# --- 3b. Operasi Aritmatika Non-Desimal ---

def tambah_basis(a_str: str, b_str: str, basis: int) -> tuple:
    """
    Penjumlahan dua bilangan dalam basis tertentu.
    
    Parameters:
        a_str, b_str (str): Bilangan dalam basis yang ditentukan
        basis        (int): Basis (2, 8, atau 16)
    Returns:
        tuple: (hasil: str, langkah: list)
    """
    # Konversi ke desimal, jumlahkan, kembalikan ke basis asal
    a_dec, _ = basis_ke_desimal(a_str, basis)
    b_dec, _ = basis_ke_desimal(b_str, basis)
    hasil_dec = a_dec + b_dec
    hasil_str, _ = desimal_ke_basis(hasil_dec, basis)

    langkah = [
        f"  {a_str}",
        f"+ {b_str}",
        "  " + "-" * max(len(a_str), len(b_str), len(hasil_str)),
        f"  {hasil_str}  (basis {basis})"
    ]
    return hasil_str, langkah


def kurang_basis(a_str: str, b_str: str, basis: int) -> tuple:
    """
    Pengurangan dua bilangan dalam basis tertentu.
    
    Parameters:
        a_str, b_str (str): Bilangan dalam basis yang ditentukan
        basis        (int): Basis (2, 8, atau 16)
    Returns:
        tuple: (hasil: str, langkah: list)
    """
    a_dec, _ = basis_ke_desimal(a_str, basis)
    b_dec, _ = basis_ke_desimal(b_str, basis)
    hasil_dec = a_dec - b_dec

    tanda = ""
    if hasil_dec < 0:
        hasil_dec = abs(hasil_dec)
        tanda = "-"

    hasil_str, _ = desimal_ke_basis(hasil_dec, basis)
    hasil_str = tanda + hasil_str

    langkah = [
        f"  {a_str}",
        f"- {b_str}",
        "  " + "-" * max(len(a_str), len(b_str), len(hasil_str)),
        f"  {hasil_str}  (basis {basis})"
    ]
    return hasil_str, langkah


def menu_konversi_bilangan():
    """Menu utama untuk modul Kalkulator Konversi Bilangan."""
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║     KALKULATOR KONVERSI BILANGAN     ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Konversi Basis                   ║")
        print("║  2. Operasi Aritmatika (BIN/OCT/HEX) ║")
        print("║  0. Kembali ke Menu Utama            ║")
        print("╚══════════════════════════════════════╝")

        pilihan = input("  Pilih: ").strip()

        if pilihan == "1":
            # ---- Konversi Basis ----
            print("\n  Basis: DEC (Desimal), BIN (Biner), OCT (Oktal), HEX (Heksadesimal)")
            try:
                dari  = input("  Dari : ").strip().upper()
                ke    = input("  Ke   : ").strip().upper()
                nilai = input("  Nilai: ").strip().upper()

                if dari not in ('DEC','BIN','OCT','HEX') or ke not in ('DEC','BIN','OCT','HEX'):
                    print("  Kode basis tidak valid!")
                    continue

                print("\n  Langkah Konversi:")
                hasil, langkah_list = konversi_bilangan(nilai, dari, ke)
                for baris in langkah_list:
                    print(baris)
                print(f"\n  Hasil: {hasil}")

                # Verifikasi: konversi kembali ke desimal
                if ke != 'DEC':
                    basis_ke_map = {'BIN': 2, 'OCT': 8, 'HEX': 16}
                    verif, _ = basis_ke_desimal(hasil, basis_ke_map[ke])
                    desimal_asal, _ = basis_ke_desimal(nilai, {'DEC':10,'BIN':2,'OCT':8,'HEX':16}[dari])
                    if verif == desimal_asal:
                        print(f"  Verifikasi: {hasil} → {verif} ✓")
                    else:
                        print(f"  Verifikasi: {hasil} → {verif} (ada perbedaan, cek input)")

                tambah_riwayat("Bilangan", f"{nilai} ({dari}) → ({ke})", hasil)
            except (ValueError, KeyError) as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "2":
            # ---- Operasi Aritmatika Non-Desimal ----
            print("\n  Basis: BIN (2), OCT (8), HEX (16)")
            print("  Operator: + (tambah) | - (kurang)")
            try:
                basis_kode = input("  Basis    : ").strip().upper()
                if basis_kode not in ('BIN', 'OCT', 'HEX'):
                    print("  Basis tidak valid!")
                    continue
                basis_val = {'BIN': 2, 'OCT': 8, 'HEX': 16}[basis_kode]

                a = input("  Bilangan 1: ").strip().upper()
                op = input("  Operator  : ").strip()
                b = input("  Bilangan 2: ").strip().upper()

                print("\n  Proses Perhitungan:")
                if op == '+':
                    hasil, langkah = tambah_basis(a, b, basis_val)
                elif op == '-':
                    hasil, langkah = kurang_basis(a, b, basis_val)
                else:
                    print("  Operator tidak dikenal!")
                    continue

                for baris in langkah:
                    print(baris)
                tambah_riwayat("Bilangan-Aritm", f"{a} {op} {b} ({basis_kode})", hasil)
            except (ValueError, KeyError) as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


# ============================================================
# BAGIAN 4: EXPORT HASIL KE FILE
# ============================================================

def export_ke_file():
    """
    Mengekspor seluruh riwayat perhitungan ke file .txt.
    Nama file otomatis diberi timestamp.
    """
    if not riwayat:
        print("\n  Tidak ada riwayat untuk diekspor.")
        return

    # Buat nama file dengan timestamp
    waktu_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nama_file = f"riwayat_kalkulator_{waktu_str}.txt"

    try:
        with open(nama_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("    LAPORAN RIWAYAT KALKULATOR MULTI-FUNGSI\n")
            f.write(f"    Digenerate pada: {datetime.datetime.now()}\n")
            f.write("=" * 60 + "\n\n")

            for i, entri in enumerate(riwayat, 1):
                f.write(f"[{i}] {entri['waktu']}\n")
                f.write(f"    Kategori : {entri['kategori']}\n")
                f.write(f"    Operasi  : {entri['operasi']}\n")
                f.write(f"    Hasil    : {entri['hasil']}\n")
                f.write("\n")

            f.write("=" * 60 + "\n")
            f.write("    Akhir Laporan\n")
            f.write("=" * 60 + "\n")

        print(f"\n  Berhasil diekspor ke: {nama_file}")
    except IOError as e:
        print(f"\n  [ERROR] Gagal menulis file: {e}")


# ============================================================
# BAGIAN BONUS: KALKULATOR IP ADDRESS
# ============================================================

def prefix_ke_subnet_mask(prefix: int) -> str:
    """
    Menghitung subnet mask dari prefix length.
    Contoh: /24 → 255.255.255.0
    
    Parameters:
        prefix (int): Prefix length (0-32)
    Returns:
        str: Subnet mask dalam notasi desimal bertitik
    """
    if not (0 <= prefix <= 32):
        raise ValueError("Prefix harus antara 0 dan 32!")

    # Buat angka biner 32-bit: prefix angka 1, sisanya 0
    mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    # Pecah menjadi 4 oktet
    oktet = [(mask_int >> shift) & 0xFF for shift in (24, 16, 8, 0)]
    return ".".join(str(o) for o in oktet)


def ip_ke_int(ip: str) -> int:
    """Mengkonversi IP address string ke integer 32-bit."""
    bagian = ip.split('.')
    if len(bagian) != 4:
        raise ValueError("Format IP tidak valid! Gunakan format: x.x.x.x")
    hasil = 0
    for o in bagian:
        val = int(o)
        if not (0 <= val <= 255):
            raise ValueError(f"Nilai oktet {val} tidak valid (harus 0-255)!")
        hasil = (hasil << 8) | val
    return hasil


def int_ke_ip(n: int) -> str:
    """Mengkonversi integer 32-bit ke string IP address."""
    oktet = [(n >> shift) & 0xFF for shift in (24, 16, 8, 0)]
    return ".".join(str(o) for o in oktet)


def ip_ke_biner(ip: str) -> str:
    """Mengkonversi IP address ke representasi biner (4 grup 8-bit)."""
    bagian = ip.split('.')
    biner_list = [format(int(o), '08b') for o in bagian]  # format 8-digit biner
    return ".".join(biner_list)


def hitung_subnet(ip: str, prefix: int):
    """
    Menghitung informasi subnet:
    - Subnet Mask
    - Network Address
    - Broadcast Address
    - Jumlah host tersedia
    - Representasi biner
    
    Parameters:
        ip     (str): IP address
        prefix (int): Prefix length (CIDR)
    """
    ip_int = ip_ke_int(ip)
    mask_str = prefix_ke_subnet_mask(prefix)
    mask_int = ip_ke_int(mask_str)

    # Network address: IP AND mask
    network_int = ip_int & mask_int
    network_str = int_ke_ip(network_int)

    # Broadcast address: Network OR (NOT mask)
    wildcard = ~mask_int & 0xFFFFFFFF
    broadcast_int = network_int | wildcard
    broadcast_str = int_ke_ip(broadcast_int)

    # Jumlah host: 2^(32-prefix) - 2 (dikurangi network & broadcast)
    if prefix < 31:
        jumlah_host = (2 ** (32 - prefix)) - 2
    elif prefix == 31:
        jumlah_host = 2   # point-to-point link
    else:
        jumlah_host = 1   # /32 = host route

    print(f"\n  IP Address      : {ip}")
    print(f"  Prefix          : /{prefix}")
    print(f"  Subnet Mask     : {mask_str}")
    print(f"  Network Address : {network_str}")
    print(f"  Broadcast       : {broadcast_str}")
    print(f"  Jumlah Host     : {jumlah_host}")
    print(f"\n  IP (Biner)      : {ip_ke_biner(ip)}")
    print(f"  Mask (Biner)    : {ip_ke_biner(mask_str)}")
    print(f"  Network (Biner) : {ip_ke_biner(network_str)}")

    return network_str, broadcast_str, jumlah_host


def menu_ip_address():
    """Menu untuk modul Kalkulator IP Address (Bonus)."""
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║       KALKULATOR IP ADDRESS          ║")
        print("║             (BONUS)                  ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Hitung Subnet                    ║")
        print("║  2. Konversi IP ke Biner             ║")
        print("║  0. Kembali ke Menu Utama            ║")
        print("╚══════════════════════════════════════╝")

        pilihan = input("  Pilih: ").strip()

        if pilihan == "1":
            try:
                ip     = input("\n  Masukkan IP Address (misal: 192.168.1.1): ").strip()
                prefix = int(input("  Prefix length (misal: 24): ").strip())
                net, bcast, host = hitung_subnet(ip, prefix)
                tambah_riwayat("IP Address", f"{ip}/{prefix}",
                               f"Net:{net} Bcast:{bcast} Host:{host}")
            except (ValueError, Exception) as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "2":
            try:
                ip = input("\n  Masukkan IP Address: ").strip()
                # Validasi format
                ip_ke_int(ip)
                print(f"  Biner: {ip_ke_biner(ip)}")
                tambah_riwayat("IP-Biner", ip, ip_ke_biner(ip))
            except ValueError as e:
                print(f"\n  [ERROR] {e}")

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


# ============================================================
# BAGIAN 5: MENU UTAMA
# ============================================================

def tampilkan_menu_utama():
    """Menampilkan menu utama sistem kalkulator."""
    print("\n╔══════════════════════════════════════╗")
    print("║   SISTEM KALKULATOR MULTI-FUNGSI     ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Kalkulator Aritmatika            ║")
    print("║  2. Kalkulator Suhu                  ║")
    print("║  3. Kalkulator Konversi Bilangan     ║")
    print("║  4. Riwayat Perhitungan              ║")
    print("║  5. Export Hasil ke File             ║")
    print("║  6. Kalkulator IP Address (Bonus)    ║")
    print("║  0. Keluar                           ║")
    print("╚══════════════════════════════════════╝")


def main():
    """
    Fungsi utama program.
    Menjalankan loop menu utama dan memanggil modul yang sesuai.
    """
    print("\n" + "=" * 44)
    print("  Selamat datang di Sistem Kalkulator Multi-Fungsi!")
    print("=" * 44)

    while True:
        tampilkan_menu_utama()
        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            menu_aritmatika()
        elif pilihan == "2":
            menu_suhu()
        elif pilihan == "3":
            menu_konversi_bilangan()
        elif pilihan == "4":
            tampilkan_riwayat()
        elif pilihan == "5":
            export_ke_file()
        elif pilihan == "6":
            menu_ip_address()
        elif pilihan == "0":
            print("\n  Terima kasih telah menggunakan Sistem Kalkulator Multi-Fungsi!")
            print("  Sampai jumpa!\n")
            break
        else:
            print("\n  Pilihan tidak valid. Silakan masukkan angka 0-6.")


# Entry point: hanya dijalankan jika file ini dieksekusi langsung
if __name__ == "__main__":
    main()