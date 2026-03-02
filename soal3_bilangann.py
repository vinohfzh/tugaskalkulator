"""
MODUL KONVERSI BILANGAN SOAL 3
File ini berisi logika untuk kalkulator sistem bilangan:
- Konversi manual antar basis Desimal, Biner, Oktal, dan Heksadesimal
- Dukungan untuk angka desimal/pecahan dalam semua basis
- Menampilkan langkah-langkah matematis proses konversi
- Operasi aritmatika (tambah/kurang) langsung pada basis non-desimal
"""

# --- MODUL BASIS BILANGAN SOAL 3 ---

def val_to_char(val):
    """Mengonversi nilai angka (0-15) menjadi karakter (0-9, A-F)"""
    if 0 <= val <= 9:
        return str(val) # Jika 0-9, kembalikan string angka tersebut
    return chr(ord('A') + val - 10) # Jika 10-15, kembalikan A-F

def char_to_val(c):
    """Mengonversi karakter (0-9, A-F) menjadi nilai angka (0-15)"""
    c = c.upper() # Pastikan karakter adalah huruf besar
    if '0' <= c <= '9':
        return int(c) # Jika angka, langsung ubah ke integer
    return ord(c) - ord('A') + 10 # Jika huruf (A-F), hitung nilainya

def decimal_to_base(n, base, precision=10):
    """Konversi manual dari Desimal ke Basis lain (Biner/Oktal/Heks) termasuk pecahan"""
    # Tahap 1: Pisahkan bagian bulat dan bagian pecahan
    integer_part = int(n)
    fractional_part = n - integer_part
    
    # Bagian A: Konversi Bagian Bulat (Metode Sisa Bagi)
    if integer_part == 0:
        res_int = "0"
        steps = ["0 / {} = 0 sisa 0".format(base)]
    else:
        res_int = ""
        steps = []
        temp_n = integer_part
        while temp_n > 0:
            remainder = temp_n % base # Cari sisa bagi (mod)
            char = val_to_char(remainder) # Ubah sisa jadi karakter
            steps.append(f"{temp_n:4} / {base} = {temp_n // base:4} sisa {char} ↑") # Catat langkah
            res_int = char + res_int # Tempelkan di depan (urutannya terbalik)
            temp_n //= base # Kurangi angka utama
    
    # Jika tidak ada bagian pecahan, langsung kembalikan hasil bagian bulat
    if fractional_part == 0:
        return res_int, steps
    
    # Bagian B: Konversi Bagian Pecahan (Metode Perkalian Berulang)
    res_frac = ""
    steps.append("\nBagian Pecahan:")
    temp_f = fractional_part
    for _ in range(precision): # Batasi presisi agar tidak loop selamanya
        if temp_f == 0: break
        mult = temp_f * base # Kalikan pecahan dengan basis
        digit = int(mult)    # Digit di depan koma adalah hasil konversi
        char = val_to_char(digit)
        steps.append(f"{temp_f:.4f} * {base} = {mult:.4f} -> Digit: {char} ↓") # Catat langkah
        res_frac += char # Tempelkan digit di belakang
        temp_f = mult - digit # Ambil sisa pecahan untuk perkalian berikutnya
        
    return f"{res_int}.{res_frac}", steps # Gabungkan bagian bulat dan pecahan

def base_to_decimal(s, base):
    """Konversi manual dari Basis lain ke Desimal termasuk pecahan"""
    # Bersihkan input dan standarisasi tanda koma menjadi titik
    s = s.upper().replace(',', '.')
    if '.' in s: # Jika ada tanda titik, pecah menjadi bagian bulat dan pecahan
        integer_str, fractional_str = s.split('.')
    else: # Jika tidak ada, anggap bagian pecahannya kosong
        integer_str, fractional_str = s, ""
        
    res = 0
    steps = []
    
    # Bagian A: Konversi Bagian Bulat (Setiap digit dikali basis pangkat posisinya)
    n = len(integer_str)
    for i, char in enumerate(integer_str):
        val = char_to_val(char) # Nilai asli digit
        power = n - 1 - i # Pangkat (mulai dari n-1 ke arah kanan sampai 0)
        term = val * (base ** power) # Hitung nilai posisi
        steps.append(f"{char} * {base}^{power} = {term}") # Catat langkah
        res += term # Jumlahkan ke total desimal
        
    # Bagian B: Konversi Bagian Pecahan (Digit dikali basis pangkat negatif)
    for i, char in enumerate(fractional_str):
        val = char_to_val(char) # Nilai asli digit
        power = -(i + 1) # Pangkat mulai dari -1, -2, dst ke kanan
        term = val * (base ** power) # Hitung nilai pecahan
        steps.append(f"{char} * {base}^{power} = {term}") # Catat langkah
        res += term # Jumlahkan ke total desimal
        
    return res, steps # Kembalikan nilai desimal total dan list langkahnya

def base_conversion_ui(add_to_history):
    """Antarmuka pengguna untuk melakukan konversi basis bilangan"""
    print("\n=== KONVERSI BASIS BILANGAN ===")
    bases = {'1': 10, '2': 2, '3': 8, '4': 16}
    names = {'1': 'Desimal', '2': 'Biner', '3': 'Oktal', '4': 'Heksadesimal'}
    
    # Memilih Basis Asal dan Tujuan
    print("Dari: 1.Desimal, 2.Biner, 3.Oktal, 4.Heksadesimal")
    from_raw = input("Pilih: ").strip().upper()
    print("Ke: 1.Desimal, 2.Biner, 3.Oktal, 4.Heksadesimal")
    to_raw = input("Pilih: ").strip().upper()
    
    # Fungsi pencarian basis (Fuzzy Matching)
    def find_base_idx(raw):
        if 'D' in raw or '1' in raw: return '1'
        if 'B' in raw or '2' in raw: return '2'
        if 'O' in raw or '3' in raw: return '3'
        if 'H' in raw or '4' in raw: return '4'
        return None

    f_idx = find_base_idx(from_raw)
    t_idx = find_base_idx(to_raw)

    if not f_idx or not t_idx: # Validasi pilihan
        print("Pilihan tidak valid.")
        return
        
    val_str = input(f"Masukkan nilai ({names[f_idx]}): ") # Ambil nilai input
    try:
        # Normalisasi input agar seragam menggunakan titik sebagai desimal
        val_str = val_str.replace(',', '.')
        
        # Langkah 1: Berapapun basis asalnya, kita ubah ke Desimal dulu
        if f_idx == '1': # Jika asal sudah desimal
            dec_val = float(val_str)
            dec_steps = [f"Nilai desimal: {dec_val}"]
        else: # Jika asal biner/oktal/heks
            dec_val, dec_steps = base_to_decimal(val_str, bases[f_idx])
            
        # Langkah 2: Ubah dari Desimal ke basis tujuan yang diinginkan
        if t_idx == '1': # Jika tujuan adalah desimal
            target_val = str(round(dec_val, 10)) # Bulatkan biar rapi
            target_steps = []
        else: # Jika tujuan biner/oktal/heks
            target_val, target_steps = decimal_to_base(dec_val, bases[t_idx])
            
        # Tampilkan Langkah Matematikanya ke Layar
        print("\nLangkah Konversi:")
        if f_idx != '1':
            print(f"Langkah ke Desimal:")
            for s in dec_steps: print(s)
            print(f"Total Desimal: {dec_val}")
        
        if t_idx != '1':
            print(f"\nLangkah dari Desimal ke {names[t_idx]}:")
            for s in target_steps: print(s)
            
        # Tampilkan Hasil Akhir
        print(f"\nHasil: {target_val}")
        print(f"Verifikasi: {target_val} ({names[t_idx]}) -> {dec_val} (Desimal) ✓")
        # Simpan aksi ke riwayat
        add_to_history(f"Konversi {val_str}({names[f_idx]}) ke {names[t_idx]}", target_val)
    except Exception as e:
        print(f"Error: {e}")

def base_arithmetic_ui(add_to_history):
    """Antarmuka pengguna untuk operasi aritmatika (Tambah/Kurang) pada basis non-desimal"""
    print("\n=== ARITMATIKA NON-DESIMAL ===")
    bases = {'1': 2, '2': 8, '3': 16}
    names = {'1': 'Biner', '2': 'Oktal', '3': 'Heksadesimal'}
    
    # Pilih basis yang ingin dihitung
    print("Pilih Basis: 1.Biner, 2.Oktal, 3.Heksadesimal")
    raw = input("Pilih: ").strip().upper()
    
    def find_base_idx(r):
        """Fuzzy Matching untuk pilihan basis"""
        if 'B' in r or '1' in r: return '1'
        if 'O' in r or '2' in r: return '2'
        if 'H' in r or '3' in r: return '3'
        return None

    idx = find_base_idx(raw)
    if not idx:
        print("Pilihan tidak valid.")
        return
    
    base = bases[idx] # Tentukan basis (2, 8, atau 16)
    name = names[idx] # Nama basis
    
    try:
        # Masukkan angka-angka dalam basis tersebut
        a_str = input(f"Masukkan angka pertama ({name}): ")
        b_str = input(f"Masukkan angka kedua ({name}): ")
        op = input("Pilih operasi (+ atau -): ") # Pilih operasinya
        
        if op not in ['+', '-']: # Validasi operasis
            print("Operasi tidak didukung.")
            return
            
        # Logika: Ubah angka asal ke Desimal dulu, hitung, lalu balikkan lagi ke Basis asal
        a_dec, _ = base_to_decimal(a_str, base)
        b_dec, _ = base_to_decimal(b_str, base)
        
        if op == '+':
            res_dec = a_dec + b_dec
        else:
            res_dec = a_dec - b_dec
            
        # Balikkan hasil hitungan desimal ke basis awal
        res_str, _ = decimal_to_base(abs(res_dec), base) # abs() biar aman dari angka negatif di fungsi base
        if res_dec < 0: res_str = "-" + res_str # Tambahkan tanda minus jika hasilnya negatif
        
        # Tampilkan Proses "Manual-style"
        print(f"\nProses Perhitungan (Manual-style):")
        print(f"  {a_str.upper():>15}  (Desimal: {a_dec})")
        print(f"{op} {b_str.upper():>15}  (Desimal: {b_dec})")
        print("-" * 18)
        print(f"  {res_str.upper():>15}  (Desimal: {res_dec})")
        
        # Simpan ke riwayat
        add_to_history(f"{a_str}{op}{b_str} (Base {base})", res_str)
    except Exception as e:
        print(f"Error: {e}")

def base_converter_menu(add_to_history):
    """Menu utama untuk modul Kalkulator Bilangan (Soal 3)"""
    while True:
        print("\n=== KALKULATOR BILANGAN (SOAL 3) ===")
        print("1. Konversi Basis")
        print("2. Operasi Aritmatika Biner/Oktal/Heks")
        print("0. Kembali")
        
        choice = input("Pilih: ")
        if choice == '1': # Masuk ke menu konversi
            base_conversion_ui(add_to_history)
        elif choice == '2': # Masuk ke menu aritmatika basis
            base_arithmetic_ui(add_to_history)
        elif choice == '0': # Kembali ke menu integrasi
            break
        else:
            print("Pilihan tidak valid.")

# Jika file ini dipanggil langsung
if __name__ == "__main__":
    def standalone_history(desc, res):
        """Riwayat dummy untuk testing terpisah"""
        print(f"[Riwayat Standalone] {desc} = {res}")
    
    base_converter_menu(standalone_history) # Jalankan menu konversi bilangan