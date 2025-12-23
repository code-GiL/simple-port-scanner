import socket
import argparse
import sys
import threading
from datetime import datetime
from queue import Queue

# --- KONFIGURASI ---
# Lock untuk mencegah teks berantakan saat diprint oleh banyak thread
print_lock = threading.Lock()
# Antrian (Queue) untuk menyimpan nomor port yang akan discan
q = Queue()

def get_args():
    """Mengambil argumen dari terminal (CLI)."""
    parser = argparse.ArgumentParser(description="Educational TCP Port Scanner (Bahasa Indonesia)")
    parser.add_argument("-t", "--target", dest="target", required=True, help="Alamat IP Target (Wajib diisi)")
    parser.add_argument("-p", "--ports", dest="ports", default="1-1024", help="Rentang Port (Contoh: 1-100, Default: 1-1024)")
    options = parser.parse_args()
    return options

def is_private_ip(ip):
    """Cek apakah IP tersebut adalah IP Privat/Lokal (bukan IP Publik)."""
    # IP Privat: 192.168.x.x, 10.x.x.x, 172.16.x.x - 172.31.x.x, 127.0.0.1
    return ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.") or ip.startswith("127.")

def port_scan(target, port):
    """Fungsi inti untuk mencoba koneksi ke port spesifik."""
    try:
        # Membuat socket TCP (IPv4)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # Batas waktu tunggu koneksi 1 detik
        
        # connect_ex mengembalikan 0 jika koneksi BERHASIL
        result = s.connect_ex((target, port))
        
        if result == 0:
            with print_lock:
                # Mencoba menebak nama layanan (misal: port 80 = http)
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "tidak diketahui"
                print(f"[+] Port {port:<5} TERBUKA (OPEN) --> {service}")
        s.close()
    except:
        pass

def threader(target_ip):
    """Worker thread yang mengambil tugas dari antrian."""
    while True:
        worker = q.get()
        port_scan(target_ip, worker)
        q.task_done()

def main():
    args = get_args()
    target = args.target
    
    # Resolusi Hostname ke IP (misal: scanme.nmap.org -> 45.33.32.156)
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] Error: Tidak dapat mengenali hostname '{target}'.")
        sys.exit()

    # --- PENGAMANAN (SAFETY CHECK) ---
    if not is_private_ip(target_ip):
        print("\n=== ⚠️ PERINGATAN KEAMANAN ⚠️ ===")
        print(f"    Anda akan memindai IP PUBLIK: {target_ip}")
        print("    Pastikan Anda memiliki izin tertulis dari pemilik server.")
        print("    Melakukan scanning tanpa izin adalah tindakan ilegal.")
        confirm = input("    Apakah Anda ingin melanjutkan? (y/n): ")
        if confirm.lower() != 'y':
            print("Dibatalkan.")
            sys.exit()

    # Parsing rentang port
    try:
        start_port, end_port = map(int, args.ports.split('-'))
    except ValueError:
        print("[-] Error: Format port harus awal-akhir (contoh: 1-100)")
        sys.exit()

    print("-" * 30)
    print(f"Target IP       : {target_ip}")
    print(f"Rentang Port    : {start_port} s/d {end_port}")
    print(f"Waktu Mulai     : {str(datetime.now())}")
    print("-" * 30)

    # Membuat 100 threads agar scanning cepat
    for _ in range(100):
        t = threading.Thread(target=threader, args=(target_ip,))
        t.daemon = True
        t.start()

    # Memasukkan daftar port ke dalam antrian
    for worker in range(start_port, end_port + 1):
        q.put(worker)

    # Menunggu antrian kosong (selesai)
    q.join()
    
    print("-" * 60)
    print("Pemindaian Selesai.")

if __name__ == "__main__":
    main()