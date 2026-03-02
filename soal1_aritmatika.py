"""
MODUL ARITMATIKA SOAL 1
File ini berisi logika untuk kalkulator aritmatika yang mendukung:
- Operasi dasar (+, -, *, /, ^, %, akar kuadrat)
- Operasi ilmiah (sin, cos, tan, log, ln)
- Evaluasi ekspresi matematika berantai dengan prioritas operator
"""

import math  # Mengimpor modul matematika standar Python
import re    # Mengimpor modul regex untuk pengolahan teks

# --- MODUL ARITMATIKA SOAL 1 ---

def get_input(prompt):
    """Fungsi pembantu untuk mengambil input dan mengganti koma dengan titik"""
    return input(prompt).replace(',', '.') # Mengambil input teks lalu menukar ',' jadi '.' agar terbaca float

def arithmetic_basic(add_to_history):
    """Fungsi untuk operasi dasar seperti tambah, kurang, kali, bagi, dll"""
    print("\n=== OPERASI DASAR ===")
    print("1. Penjumlahan (+)")
    print("2. Pengurangan (-)")
    print("3. Perkalian (*)")
    print("4. Pembagian (/)")
    print("5. Pangkat (^)")
    print("6. Modulo (%)")
    print("7. Akar Kuadrat (√)")
    
    # Mengambil input pilihan operasi dan mengubah ke huruf kecil
    raw = input("Pilih operasi: ").strip().lower()
    
    def find_op(r):
        """Fungsi internal untuk mencocokkan input user dengan pilihan operasi (Fuzzy Matching)"""
        if '1' in r or '+' in r or 'jumlah' in r: return '1' # Jika ada angka 1, tanda +, atau kata jumlah
        if '2' in r or '-' in r or 'kurang' in r: return '2'
        if '3' in r or '*' in r or 'x' in r or 'kali' in r: return '3'
        if '4' in r or '/' in r or 'bagi' in r: return '4'
        if '5' in r or '^' in r or 'pangkat' in r: return '5'
        if '6' in r or '%' in r or 'modulo' in r: return '6'
        if '7' in r or '√' in r or 'akar' in r or 'sqrt' in r: return '7'
        return None # Jika tidak ada yang cocok

    choice = find_op(raw) # Mencari pilihan berdasarkan input user
    if not choice: # Jika pilihan tidak ditemukan
        print("Pilihan tidak valid.")
        return

    try:
        if choice == '7': # Khusus untuk Akar Kuadrat (hanya butuh 1 angka)
            val = float(get_input("Masukkan angka: ")) # Mengambil input angka
            if val < 0: # Validasi angka negatif
                print("Error: Tidak bisa akar kuadrat angka negatif.")
                return
            res = math.sqrt(val) # Menghitung akar
            print(f"Hasil: √{val} = {res}") # Menampilkan hasil
            add_to_history(f"√{val}", res) # Simpan ke riwayat
        elif choice in ['1', '2', '3', '4', '5', '6']: # Operasi yang butuh 2 angka (binary operations)
            a = float(get_input("Masukkan angka pertama: ")) # Input angka 1
            b = float(get_input("Masukkan angka kedua: "))   # Input angka 2
            
            if choice == '1': # Penjumlahan
                res = a + b
                op = "+"
            elif choice == '2': # Pengurangan
                res = a - b
                op = "-"
            elif choice == '3': # Perkalian
                res = a * b
                op = "*"
            elif choice == '4': # Pembagian
                if b == 0: # Validasi pembagian nol
                    print("Error: Pembagian dengan nol.")
                    return
                res = a / b
                op = "/"
            elif choice == '5': # Perpangkatan
                res = a ** b
                op = "^"
            elif choice == '6': # Sisa Bagi (Modulo)
                res = a % b
                op = "%"
            
            print(f"Hasil: {a} {op} {b} = {res}") # Cetak hasil ke layar
            add_to_history(f"{a} {op} {b}", res)  # Simpan ke riwayat
        else:
            print("Pilihan tidak valid.")
    except ValueError: # Menangani jika user memasukkan bukan angka
        print("Error: Input harus angka.")

def arithmetic_scientific(add_to_history):
    """Fungsi untuk operasi matematika ilmiah (sin, cos, log, dll)"""
    print("\n=== OPERASI ILMIAH ===")
    print("1. Sin (Radian)")
    print("2. Cos (Radian)")
    print("3. Tan (Radian)")
    print("4. Log10")
    print("5. Ln (Log Natural)")
    
    # Input user untuk pilihan menu ilmiah
    raw = input("Pilih operasi: ").strip().lower()
    
    def find_sci_op(r):
        """Fungsi fuzzy matching khusus menu ilmiah"""
        if '1' in r or 'sin' in r: return '1'
        if '2' in r or 'cos' in r: return '2'
        if '3' in r or 'tan' in r: return '3'
        if '4' in r or 'log' in r: return '4'
        if '5' in r or 'ln' in r: return '5'
        return None

    choice = find_sci_op(raw) # Cari menu yang dipilih
    if not choice: # Validasi menu
        print("Pilihan tidak valid.")
        return

    try:
        val = float(get_input("Masukkan angka: ")) # Input angka untuk dihitung
        if choice == '1': # Sinus
            res = math.sin(val)
            desc = f"sin({val})"
        elif choice == '2': # Cosinus
            res = math.cos(val)
            desc = f"cos({val})"
        elif choice == '3': # Tangen
            res = math.tan(val)
            desc = f"tan({val})"
        elif choice == '4': # Logaritma Basis 10
            if val <= 0: # Validasi domain log
                print("Error: Logaritma harus positif.")
                return
            res = math.log10(val)
            desc = f"log10({val})"
        elif choice == '5': # Logaritma Natural (Ln)
            if val <= 0:
                print("Error: Ln harus positif.")
                return
            res = math.log(val)
            desc = f"ln({val})"
        else:
            print("Pilihan tidak valid.")
            return
            
        print(f"Hasil: {desc} = {res}") # Tampilkan hasil perhitungan
        add_to_history(desc, res) # Tambahkan ke riwayat
    except ValueError:
        print("Error: Input harus angka.")

def parse_expression(expr):
    """Parser sederhana untuk mengevaluasi ekspresi matematika berantai"""
    expr = expr.replace(" ", "") # Hilangkan semua spasi
    # Validasi input: hanya boleh angka, operator (+-*/), titik desimal, dan kurung
    if not re.match(r'^[0-9+\-*/().]+$', expr):
        raise ValueError("Karakter tidak valid dalam ekspresi.")
    try:
        result = eval(expr) # Mengevaluasi string sebagai kode Python
        original = expr     # Simpan ekspresi awal
        # Mencoba membuat "langkah sederhana" dengan mengeksekusi perkalian/pembagian dulu
        pattern = r'(\d+\.?\d*[\*/]\d+\.?\d*)'
        matches = re.findall(pattern, expr)
        step_expr = expr
        for m in matches:
            m_res = eval(m)
            step_expr = step_expr.replace(m, str(m_res), 1)
        return result, f"{original} -> {step_expr} = {result}"
    except Exception as e:
        raise ValueError(f"Ekspresi tidak valid: {e}")

def arithmetic_chained(add_to_history):
    """UI untuk menghitung ekspresi matematika berantai"""
    print("\n=== EKSPRESI BERANTAI ===")
    expr = input("Masukkan ekspresi (contoh: 5 + 3 * 2 - 4 / 2): ") # Input ekspresi user
    try:
        res, steps = parse_expression(expr) # Panggil fungsi parser
        print(f"Hasil: {res}") # Tampilkan hasil akhir
        print(f"Langkah: {steps}") # Tampilkan langkah sederhana
        add_to_history(expr, res) # Simpan ke riwayat
    except ValueError as e: # Tangani error format ekspresi
        print(f"Error: {e}")

def arithmetic_menu(add_to_history):
    """Menu utama untuk modul aritmatika (Soal 1)"""
    while True: # Loop menu agar terus berjalan sampai user keluar
        print("\n=== KALKULATOR ARITMATIKA (SOAL 1) ===")
        print("1. Operasi Dasar")
        print("2. Operasi Ilmiah")
        print("3. Ekspresi Berantai")
        print("0. Kembali")
        
        choice = input("Pilih: ").strip().lower() # Mintalah input user
        if choice in ['1', 'dasar', 'operasi dasar']: # Ke menu operasi dasar
            arithmetic_basic(add_to_history)
        elif choice in ['2', 'ilmiah', 'operasi ilmiah']: # Ke menu operasi ilmiah
            arithmetic_scientific(add_to_history)
        elif choice in ['3', 'berantai', 'ekspresi berantai']: # Ke menu ekspresi berantai
            arithmetic_chained(add_to_history)
        elif choice in ['0', 'kembali']: # Keluar dari menu aritmatika
            break
        else:
            print("Pilihan tidak valid.") # Jika menu tidak dikenali

# Blok ini dijalankan saat file dipanggil langsung (bukan di-import)
if __name__ == "__main__":
    def standalone_history(desc, res):
        """Fungsi riwayat dummy untuk testing standalone"""
        print(f"[Riwayat Standalone] {desc} = {res}")
    
    arithmetic_menu(standalone_history) # Jalankan menu utama