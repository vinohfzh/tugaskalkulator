"""
MAIN INTEGRATOR - SOAL 4
File ini adalah modul utama (entry point) yang menggabungkan semua modul:
- Modul 1: Aritmatika
- Modul 2: Suhu
- Modul 3: Bilangan
- Modul Bonus: IP Address
Serta fitur tambahan seperti Riwayat Perhitungan dan Export File.
"""

import os # Mengimpor modul OS untuk keperluan sistem (jika diperlukan)
from datetime import datetime # Mengimpor datetime untuk label waktu pada eksport
# Mengimpor modul-modul soal yang telah dibuat sebelumnya
from soal1_aritmatika import arithmetic_menu
from soal2_suhu import temperature_menu
from soal3_bilangan import base_converter_menu
from soal_bonus_ip import ip_calculator_menu

# Variabel global untuk menampung riwayat perhitungan selama program berjalan
calculation_history = []

def add_to_history(description, result):
    """Fungsi pembantu untuk mencatat setiap perhitungan yang dilakukan user"""
    global calculation_history
    # Format: "Deskripsi = Hasil"
    entry = f"{description} = {result}"
    calculation_history.append(entry) # Masukkan ke list riwayat
    # Batasi riwayat hanya menyimpan 10 item terbaru agar tidak terlalu berat
    if len(calculation_history) > 10:
        calculation_history.pop(0) # Hapus item paling lama

def export_history():
    """Fungsi untuk menyimpan riwayat perhitungan ke dalam satu file teks (Append Mode)"""
    if not calculation_history: # Cek jika riwayat masih kosong
        print("Tidak ada riwayat untuk di-export.")
        return
    
    filename = "export_kalkulator.txt" # Nama file tunggal untuk eksport
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Ambil waktu sekarang
    
    try:
        # Membuka file dengan mode 'a' (append) agar konten baru ditambahkan di akhir file
        with open(filename, "a", encoding="utf-8") as f:
            f.write("\n" + "="*40 + "\n") # Garis pembatas sesi
            f.write(f" SESI EXPORT: {current_time}\n") # Label waktu eksport
            f.write("="*40 + "\n")
            # Menuliskan satu per satu riwayat perhitungan
            for i, h in enumerate(calculation_history, 1):
                f.write(f"[{i:2}] {h}\n")
            f.write("-" * 40 + "\n") # Garis penutup sesi
            
        print(f"Berhasil memperbarui file: {filename}")
        print("Silakan cek file untuk melihat tambahan history terbaru.")
    except Exception as e:
        print(f"Gagal meng-export: {e}")

def show_history():
    """Fungsi untuk menampilkan isi riwayat perhitungan saat ini di layar console"""
    print("\n=== RIWAYAT 10 PERHITUNGAN TERAKHIR ===")
    if not calculation_history: # Validasi riwayat kosong
        print("Belum ada riwayat.")
    else:
        # Loop dan tampilkan riwayat dengan penomoran
        for i, h in enumerate(calculation_history, 1):
            print(f"{i}. {h}")

def main_menu():
    """Menu utama aplikasi yang mengintegrasikan seluruh fitur kalkulator"""
    while True: # Loop utama program
        print("\n" + "╔" + "═"*38 + "╗")
        print("║" + "    SISTEM KALKULATOR MULTI-FUNGSI    " + "║")
        print("╠" + "═"*38 + "╣")
        print("║  1. Kalkulator Aritmatika            ║")
        print("║  2. Kalkulator Suhu                  ║")
        print("║  3. Kalkulator Konversi Bilangan     ║")
        print("║  4. Riwayat Perhitungan              ║")
        print("║  5. Export Hasil ke File             ║")
        print("║  6. Kalkulator IP Address (Bonus)    ║")
        print("║  0. Keluar                           ║")
        print("╚" + "═"*38 + "╝")
        
        # Input pilihan menu dari user (Fuzzy matching)
        raw = input("Pilih: ").strip().lower()
        
        # Logika pengalihan menu berdasarkan keyword atau angka
        if '1' in raw or 'aritmatika' in raw:
            arithmetic_menu(add_to_history) # Masuk ke modul Aritmatika
        elif '2' in raw or 'suhu' in raw:
            temperature_menu(add_to_history) # Masuk ke modul Suhu
        elif '3' in raw or 'bilangan' in raw or 'konversi' in raw:
            base_converter_menu(add_to_history) # Masuk ke modul Bilangan
        elif '4' in raw or 'riwayat' in raw:
            show_history() # Tampilkan riwayat di layar
        elif '5' in raw or 'export' in raw:
            export_history() # Simpan riwayat ke file .txt
        elif '6' in raw or 'ip' in raw:
            ip_calculator_menu(add_to_history) # Masuk ke modul IP (Bonus)
        elif '0' in raw or 'keluar' in raw:
            print("Terima kasih menggunakan sistem ini!") # Penutup program
            break # Keluar dari loop agar program berhenti
        else:
            print("Pilihan tidak valid.") # Jika menu tidak dikenali

# Bagian pengeksekusian program utama
if __name__ == "__main__":
    try:
        main_menu() # Panggil menu utama
    except KeyboardInterrupt: # Tangani jika user menekan Ctrl+C secara paksa
        print("\n\nProgram dihentikan paksa.")