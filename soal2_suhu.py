"""
MODUL KONVERSI SUHU SOAL 2
File ini berisi logika untuk sistem konversi suhu yang mendukung:
- Konversi antar skala Celsius, Fahrenheit, Kelvin, dan Reaumur
- Pembuatan tabel konversi suhu dalam rentang tertentu
- Klasifikasi status suhu (Beku, Dingin, Normal, Panas, Sangat Panas)
"""

# --- MODUL SUHU SOAL 2 ---

def get_input(prompt):
    """Mengambil input dan menukar tanda koma menjadi titik agar bisa dikonversi ke float"""
    return input(prompt).replace(',', '.')

def classify_temp(celsius):
    """Mengelompokkan status suhu berdasarkan nilai Celsius"""
    if celsius <= 0:
        return "Beku" # Di bawah atau sama dengan 0 derajat
    elif 1 <= celsius <= 15:
        return "Dingin" # Rentang 1 sampai 15 derajat
    elif 16 <= celsius <= 25:
        return "Normal" # Rentang 16 sampai 25 derajat
    elif 26 <= celsius <= 35:
        return "Panas" # Rentang 26 sampai 35 derajat
    else:
        return "Sangat Panas" # Di atas 35 derajat

def convert_temp(val, from_scale, to_scale):
    """Fungsi inti untuk menghitung konversi nilai suhu antar skala"""
    # Tahap 1: Ubah suhu asal ke skala Celsius dahulu sebagai standar tengah
    if from_scale == 'C':
        c = val # Tetap Celsius
    elif from_scale == 'F':
        c = (val - 32) * 5/9 # Rumus Fahrenheit ke Celsius
    elif from_scale == 'K':
        c = val - 273.15     # Rumus Kelvin ke Celsius
    elif from_scale == 'R':
        c = val * 5/4        # Rumus Reaumur ke Celsius
    else:
        return None # Skala tidak dikenali
    
    # Tahap 2: Ubah dari Celsius ke skala tujuan yang diinginkan
    if to_scale == 'C':
        return c # Tetap Celsius
    elif to_scale == 'F':
        return (c * 9/5) + 32 # Skala Celsius ke Fahrenheit
    elif to_scale == 'K':
        return c + 273.15     # Skala Celsius ke Kelvin
    elif to_scale == 'R':
        return c * 4/5        # Skala Celsius ke Reaumur
    else:
        return None # Skala tujuan tidak dikenali

def temperature_conversion(add_to_history):
    """Antarmuka pengguna untuk melakukan konversi suhu tunggal"""
    print("\n=== KONVERSI SATUAN SUHU ===")
    names = {'C': 'Celsius', 'F': 'Fahrenheit', 'K': 'Kelvin', 'R': 'Reaumur'}
    
    # Menampilkan pilihan skala
    print("Pilih Satuan Asal: 1.C, 2.F, 3.K, 4.R")
    from_raw = input("Pilih: ").strip().upper()
    print("Pilih Satuan Tujuan: 1.C, 2.F, 3.K, 4.R")
    to_raw = input("Pilih: ").strip().upper()
    
    # Fungsi pencarian unit yang fleksibel (Fuzzy Matching)
    def find_unit(raw):
        if 'C' in raw or '1' in raw: return 'C'
        if 'F' in raw or '2' in raw: return 'F'
        if 'K' in raw or '3' in raw: return 'K'
        if 'R' in raw or '4' in raw: return 'R'
        return None

    unit_from = find_unit(from_raw) # Mencari unit asal
    unit_to = find_unit(to_raw)     # Mencari unit tujuan
    
    if not unit_from or not unit_to: # Jika input tidak valid
        print("Pilihan tidak valid.")
        return
        
    try:
        # Meminta nilai suhu dari user
        val = float(get_input(f"Masukkan nilai dalam {names[unit_from]}: "))
        res = convert_temp(val, unit_from, unit_to) # Hitung hasil konversi
        c_equiv = convert_temp(val, unit_from, 'C') # Cari padanan Celsius untuk klasifikasi
        classification = classify_temp(c_equiv)      # Tentukan status suhu
        
        # Menampilkan output hasil
        print(f"Hasil: {val}°{unit_from} = {res:.2f}°{unit_to}")
        print(f"Klasifikasi (berdasarkan Celsius): {classification}")
        # Menambahkan data ke riwayat integrasi
        add_to_history(f"Konversi {val}{unit_from} ke {unit_to}", f"{res:.2f}{unit_to}")
    except ValueError:
        print("Error: Input harus angka.")

def display_formulas():
    """Fungsi untuk menampilkan tabel rumus konversi sesuai permintaan User"""
    print("\n=== RUMUS KONVERSI SUHU ===")
    print("┌─────────┬──────────────────────┐")
    print("│ Dari/Ke │ Rumus                │")
    print("├─────────┼──────────────────────┤")
    print("│ C -> F  │ (C * 9/5) + 32       │")
    print("│ C -> K  │ C + 273.15           │")
    print("│ C -> R  │ C * 4/5              │")
    print("│ F -> C  │ (F - 32) * 5/9       │")
    print("│ K -> C  │ K - 273.15           │")
    print("└─────────┴──────────────────────┘")

def temperature_table():
    """Fungsi untuk membuat dan menampilkan tabel konversi suhu dalam rentang Celsius"""
    print("\n=== TABEL KONVERSI (Celsius ke Lainnya) ===")
    try:
        # Mengambil parameter tabel dari user
        start = float(get_input("Mulai (°C): "))
        end = float(get_input("Selesai (°C): "))
        step = float(get_input("Step: "))
        
        if step <= 0: # Validasi step harus angka positif
            print("Error: Step harus positif.")
            return
            
        # Mencetak header tabel
        print("-" * 65)
        print(f"{'Celsius':<10} | {'Fahr':<10} | {'Kelvin':<10} | {'Reau':<10} | {'Status'}")
        print("-" * 65)
        
        # Logika pengumpulan nilai yang akan ditampilkan (Mendukung rentang naik atau turun)
        vals = []
        if start <= end: # Jika rentang naik
            curr = start
            while curr <= end + 0.000001: # Pakai toleransi kecil untuk floating point
                vals.append(curr)
                curr += step
        else: # Jika rentang turun
            curr = start
            while curr >= end - 0.000001:
                vals.append(curr)
                curr -= step
        
        # Jika loop tidak menghasilkan apapun, paksa cetak baris awal
        if not vals:
            vals = [start]

        # Iterasi setiap nilai untuk dihitung konversinya dan dicetak ke tabel
        for v in vals:
            f = convert_temp(v, 'C', 'F') # Konversi ke Fahrenheit
            k = convert_temp(v, 'C', 'K') # Konversi ke Kelvin
            r = convert_temp(v, 'C', 'R') # Konversi ke Reaumur
            status = classify_temp(v)     # Ambil status (Panas/Normal/dll)
            # Cetak baris data dengan format kolom yang rapi
            print(f"{v:<10.2f} | {f:<10.2f} | {k:<10.2f} | {r:<10.2f} | {status}")
            
        print("-" * 65) # Garis penutup tabel
    except ValueError:
        print("Error: Input harus angka.")

def temperature_menu(add_to_history):
    """Menu navigasi utama untuk modul Kalkulator Suhu"""
    while True:
        print("\n=== KALKULATOR SUHU (SOAL 2) ===")
        print("1. Konversi Satuan")
        print("2. Tabel Konversi")
        print("3. Klasifikasi Suhu Langsung")
        print("4. Lihat Rumus Konversi")
        print("0. Kembali")
        
        # Mengambil input menu dengan pengenalan kata kunci (Fuzzy)
        raw = input("Pilih: ").strip().lower()
        if '1' in raw or 'konversi' in raw:
            temperature_conversion(add_to_history)
        elif '2' in raw or 'tabel' in raw:
            temperature_table()
        elif '3' in raw or 'klasifikasi' in raw:
            try:
                # Meminta input suhu khusus untuk diklasifikasikan statusnya
                val = float(get_input("Masukkan suhu dalam Celsius: "))
                print(f"Klasifikasi: {classify_temp(val)}")
            except ValueError:
                print("Error: Input harus angka.")
        elif '4' in raw or 'rumus' in raw:
            display_formulas() # Tampilkan tabel rumus
        elif '0' in raw or 'kembali' in raw:
            break # Kembali ke menu integrasi utama
        else:
            print("Pilihan tidak valid.")

# Dijalankan jika file ini dieksekusi sebagai program utama
if __name__ == "__main__":
    def standalone_history(desc, res):
        """Riwayat sementara untuk penggunaan tanpa file integrasi"""
        print(f"[Riwayat Standalone] {desc} = {res}")
    
    temperature_menu(standalone_history) # Masuk ke menu kalkulator suhu