"""
MODUL IP ADDRESS (SOAL BONUS)
File ini berisi logika untuk kalkulasi jaringan IP:
- Konversi IP Address ke format Biner
- Perhitungan Subnet Mask berdasarkan prefix length (CIDR)
- Perhitungan jumlah total host dan host yang dapat digunakan
"""


from soal3_bilangan import decimal_to_base # Mengimpor fungsi konversi desimal ke basis lain

# --- MODUL IP ADDRESS (BONUS) ---

def ip_to_bin(ip):
    """Mengonversi alamat IP string (e.g. 192.168.1.1) ke format biner"""
    parts = ip.split('.') # Memecah IP menjadi 4 bagian berdasarkan tanda titik
    if len(parts) != 4: raise ValueError("IP tidak valid") # IP harus punya 4 segmen
    bin_parts = []
    for p in parts:
        val = int(p) # Mengubah segmen teks jadi angka
        if not (0 <= val <= 255): raise ValueError("Part IP harus 0-255") # Validasi rentang angka IP
        b, _ = decimal_to_base(val, 2) # Mengonversi angka ke biner pakai modul Soal 3
        bin_parts.append(b.zfill(8))   # Pastikan biner selalu 8 digit (nambah nol di depan kalau kurang)
    return ".".join(bin_parts) # Gabungkan kembali bagian biner dengan titik

def prefix_to_mask(prefix):
    """Menghitung Subnet Mask dari panjang prefix (e.g. 24 -> 255.255.255.0)"""
    if not (0 <= prefix <= 32): raise ValueError("Prefix harus 0-32") # Prefix maksimal 32 (untuk IPv4)
    mask_bin = "1" * prefix + "0" * (32 - prefix) # Buat barisan 1 sebanyak prefix dan sisanya 0
    # Pecah 32 bit menjadi 4 segmen 8-bit, lalu ubah tiap segmen biner ke desimal
    parts = [str(int(mask_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    return ".".join(parts) # Gabungkan jadi string IP mask

def ip_to_int(ip):
    """Mengonversi IP string ke integer 32-bit untuk perhitungan bitwise"""
    parts = [int(p) for p in ip.split('.')] # Ubah tiap bagian IP jadi integer
    # Geser bit tiap bagian ke posisinya masing-masing dalam 32-bit
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def int_to_ip(n):
    """Mengonversi kembali integer 32-bit ke format IP string"""
    # Ambil 8-bit dari tiap posisi dengan shift dan mask 0xFF (255)
    return f"{(n >> 24) & 0xFF}.{(n >> 16) & 0xFF}.{(n >> 8) & 0xFF}.{n & 0xFF}"

def ip_calculator_menu(add_to_history):
    """Antarmuka pengguna untuk kalkulator IP Address (Bonus)"""
    print("\n=== KALKULATOR IP ADDRESS (BONUS) ===")
    try:
        # Mengambil input alamat IP dan prefix
        ip_str = input("Masukkan IP Address (e.g. 192.168.1.1): ")
        prefix = int(input("Masukkan Prefix (e.g. 24): "))
        
        # Menghitung mask dan biner
        mask_str = prefix_to_mask(prefix)
        ip_bin = ip_to_bin(ip_str)
        mask_bin = ip_to_bin(mask_str)
        
        # Kalkulasi Network & Broadcast menggunakan operasi bitwise integer
        ip_val = ip_to_int(ip_str) # Nilai IP dlm integer
        mask_val = ip_to_int(mask_str) # Nilai Mask dlm integer
        
        # Alamat Network didapat dari IP di-AND-kan dengan Mask
        net_val = ip_val & mask_val
        # Alamat Broadcast didapat dari IP di-OR-kan dengan Invers Mask
        broad_val = net_val | (~mask_val & 0xFFFFFFFF)
        
        # Menghitung jumlah host (2 pangkat jumlah bit sisa)
        num_hosts = 2**(32 - prefix)
        # Usable host adalah total host dikurangi 2 (Network dan Broadcast)
        usable_hosts = num_hosts - 2 if num_hosts > 2 else num_hosts
        
        # Tampilkan Hasil Kalkulasi
        print(f"\nSubnet Mask:      {mask_str}")
        print(f"Network Address:  {int_to_ip(net_val)}")
        print(f"Broadcast Address: {int_to_ip(broad_val)}")
        print(f"IP Biner:         {ip_bin}")
        print(f"Mask Biner:       {mask_bin}")
        print(f"Total Host:       {num_hosts}")
        if prefix <= 30: # Jika prefix > 30 biasanya tidak ada usable host standar
            print(f"Usable Host:      {usable_hosts}")
        
        # Simpan hasil ke riwayat utama
        add_to_history(f"IP Calc {ip_str}/{prefix}", f"Net: {int_to_ip(net_val)}")
    except Exception as e:
        print(f"Error: {e}")

# Memungkinkan file dijalankan secara terpisah (standalone)
if __name__ == "__main__":
    def standalone_history(desc, res):
        """Riwayat sementara untuk testing modul IP saja"""
        print(f"[Riwayat Standalone] {desc} = {res}")
    
    ip_calculator_menu(standalone_history) # Masuk ke menu IP