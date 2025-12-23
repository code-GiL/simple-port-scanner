# simple-port-scanner (Bahasa Indonesia)

Sebuah alat pemindai port TCP (*port scanner*) sederhana berbasis Python yang menggunakan teknik *Multi-threading* untuk kecepatan pemindaian.

## LEGAL DISCLAIMER

**Alat ini dibuat KHUSUS UNTUK TUJUAN EDUKASI dan AUDIT KEAMANAN YANG SAH.**

Melakukan pemindaian port (*port scanning*) tanpa izin tertulis dari pemilik sistem adalah tindakan ilegal dan dapat dikategorikan sebagai kejahatan siber (Cybercrime).

**Bagi Pengguna di Indonesia:**
Tindakan akses ilegal dapat menjerat Anda pada **UU ITE (Undang-Undang Informasi dan Transaksi Elektronik)**, khususnya Pasal 30 tentang Akses Ilegal.

* **DILARANG** menggunakan alat ini pada jaringan/server yang bukan milik Anda.
* **DILARANG** menggunakan alat ini untuk tujuan merusak atau merugikan orang lain.

Pembuat kode tidak bertanggung jawab atas segala kerusakan atau konsekuensi hukum yang timbul akibat penyalahgunaan alat ini.

## Fitur
* **Cepat:** Menggunakan 100 *threads* simultan.
* **Aman (Safety First):** Memberikan peringatan otomatis jika pengguna mencoba memindai IP Publik.
* **Deteksi Layanan:** Mencoba mengenali layanan yang berjalan pada port terbuka (misal: Port 80 -> http).

## Instalasi
1. Clone repositori ini:
   ```bash
   git clone [https://github.com/code-GiL/simple-port-scanner.git](https://github.com/code-GiL/simple-port-scanner.git)
   cd educational-port-scanner
2. Tidak perlu instalasi library tambahan (pip install) karena alat ini hanya menggunakan Python Standard Library.

## Cara Penggunaan
Jalankan script menggunakan Python via terminal/CMD.
1. Scan Standar (Port 1-1024):
   python port_scanner.py -t 192.168.1.1
2. Scan Rentang Port Tertentu (Misal port 1 sampai 5000):
   python port_scanner.py -t 192.168.1.1 -p 1-5000

## Cara Kerja Teknis
Alat ini melakukan teknik "TCP Connect Scan":
1. Mengirim paket SYN ke target.
2. Menunggu balasan.
   - Jika menerima SYN-ACK, koneksi berhasil -> Port TERBUKA. 
   - Jika menerima RST (Reset) atau Timeout -> Port TERTUTUP/FILTERED.
3. Menutup koneksi segera setelah berhasil (untuk meminimalkan beban pada target).

# Lisensi
MIT License