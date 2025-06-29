# Dokumen Kebutuhan Produk (PRD): Tanam Rawat

## 1. Tinjauan Produk

**Visi Produk:** Menjadi asisten perawatan tanaman cerdas yang paling akurat dan relevan bagi pehobi tanaman di Indonesia, dengan fokus pada flora dan ekosistem lokal.

**Target Pengguna:**
- **Pengguna Utama:** Pehobi tanaman hias pemula hingga menengah di Indonesia yang aktif mencari informasi perawatan di media sosial.
- **Pengguna Sekunder:** Petani tanaman hias skala kecil dan penjual tanaman yang membutuhkan alat bantu untuk identifikasi dan diagnosis.

**Tujuan Bisnis:**
- Mencapai 10.000 pengguna aktif dalam 6 bulan pertama setelah peluncuran.
- Mengkonversi 5% pengguna gratis menjadi pelanggan "Tanam Rawat Pro" dalam 1 tahun.
- Menjadi platform komunitas terpusat untuk pehobi tanaman di Indonesia.

**Metrik Kesuksesan:**
- **Akurasi Identifikasi:** Tingkat keberhasilan identifikasi tanaman lokal di atas 90%.
- **Tingkat Keterlibatan (Engagement):** Rata-rata pengguna membuka aplikasi 3 kali seminggu.
- **Retensi Pengguna:** Tingkat retensi 30 hari sebesar 40%.
- **Aktivitas Komunitas:** Jumlah posting dan komentar harian di forum.

## 2. Persona Pengguna

### Persona 1: "Rina, Karyawan Kantoran & Pehobi Baru"
- **Demografi:** 28 tahun, tinggal di apartemen perkotaan, melek teknologi.
- **Tujuan:** Ingin berhasil merawat tanaman hias dalam ruangan (indoor plants) untuk dekorasi dan penghilang stres, tetapi sering gagal karena kurang pengetahuan.
- **Masalah (Pain Points):**
    - Tidak tahu nama tanaman yang baru dibeli.
    - Bingung kapan dan seberapa banyak harus menyiram.
    - Tanaman sering mati karena hama atau penyakit yang tidak diketahui.
    - Informasi dari internet seringkali bersifat umum dan tidak sesuai untuk iklim Indonesia.
- **Perjalanan Pengguna:** Rina mengunduh aplikasi, menggunakan fitur identifikasi untuk mengenali monstera barunya, mendapatkan jadwal penyiraman otomatis, dan bertanya di forum cara mengatasi daun yang menguning.

### Persona 2: "Pak Budi, Pensiunan & Kolektor Anggrek"
- **Demografi:** 60 tahun, tinggal di rumah dengan halaman, memiliki pengalaman merawat tanaman, aktif di grup Facebook.
- **Tujuan:** Ingin memastikan koleksi anggrek langkanya tetap sehat dan terhindar dari penyakit spesifik.
- **Masalah (Pain Points):**
    - Sulit menemukan informasi terpercaya tentang penyakit spesifik anggrek lokal.
    - Ingin berdiskusi dengan sesama kolektor yang memiliki minat serupa.
    - Kewalahan melacak jadwal pemupukan untuk puluhan tanamannya.
- **Perjalanan Pengguna:** Pak Budi menggunakan fitur diagnosis penyakit untuk mengidentifikasi bercak pada daun anggreknya, menemukan solusi di ensiklopedia hama, dan berbagi pengalamannya di forum komunitas anggrek.

## 3. Kebutuhan Fitur (MVP)

| Fitur | Deskripsi | User Stories | Prioritas | Kriteria Penerimaan | Ketergantungan |
|---|---|---|---|---|---|
| **Identifikasi Tanaman (AI)** | Pengguna mengambil foto tanaman, AI mengidentifikasi nama tanaman dari database lokal. | Sebagai Rina, saya ingin bisa memfoto tanaman saya dan langsung tahu namanya agar saya bisa mencari cara perawatan yang benar. | **Wajib** | - Aplikasi dapat mengidentifikasi 20 jenis tanaman hias paling populer di Indonesia dengan akurasi >90%.<br>- Hasil identifikasi muncul dalam waktu <5 detik. | - Database gambar tanaman lokal.<br>- Model AI yang sudah dilatih. |
| **Database Perawatan Lokal** | Informasi detail perawatan (air, cahaya, media tanam) untuk setiap tanaman yang teridentifikasi. | Sebagai Rina, setelah tahu nama tanaman saya, saya ingin mendapatkan panduan perawatan spesifik yang sesuai untuk iklim tropis. | **Wajib** | - Setiap tanaman dalam database memiliki panduan perawatan lengkap.<br>- Informasi media tanam dan pupuk mudah ditemukan di pasar Indonesia. | - Fitur Identifikasi Tanaman. |
| **Jadwal Perawatan Cerdas** | Sistem pengingat otomatis untuk menyiram dan memupuk berdasarkan jenis tanaman. | Sebagai Rina, saya ingin aplikasi mengingatkan saya kapan harus menyiram tanaman agar saya tidak lupa atau kelebihan air. | **Wajib** | - Pengguna dapat menambahkan tanaman ke "Koleksi Saya".<br>- Jadwal penyiraman otomatis dibuat setelah tanaman ditambahkan.<br>- Notifikasi pengingat muncul di perangkat pengguna. | - Database Perawatan Lokal. |
| **Ensiklopedia Hama & Penyakit** | Direktori visual hama dan penyakit umum di Indonesia, beserta cara penanganannya. | Sebagai Pak Budi, saya ingin bisa mencari gambar hama yang menyerang anggrek saya dan menemukan cara membasminya. | **Sebaiknya Ada** | - Ensiklopedia berisi minimal 10 hama/penyakit paling umum.<br>- Setiap entri memiliki foto, deskripsi, dan solusi (organik/kimia). | - Konten dari ahli hortikultura. |
| **Forum Komunitas** | Ruang diskusi di dalam aplikasi tempat pengguna bisa bertanya, berbagi, dan berinteraksi. | Sebagai Pak Budi, saya ingin bergabung dengan grup pecinta anggrek untuk berbagi tips dan memamerkan koleksi saya. | **Sebaiknya Ada** | - Pengguna dapat membuat postingan (teks & gambar).<br>- Pengguna dapat berkomentar pada postingan.<br>- Terdapat kategori atau grup berdasarkan jenis tanaman. | - Sistem otentikasi pengguna. |

## 4. Alur Pengguna (User Flows)

### Alur 1: Onboarding & Identifikasi Tanaman Pertama
1. Pengguna mengunduh & membuka aplikasi.
2. Tampilan selamat datang singkat (3 layar).
3. Pengguna mendaftar menggunakan Akun Google/Email.
4. Halaman utama menampilkan tombol besar "Identifikasi Tanaman".
5. Pengguna mengambil/mengunggah foto.
6. Layar memuat, lalu menampilkan hasil identifikasi.
7. Pengguna melihat detail tanaman dan opsi "Tambahkan ke Koleksiku".
8. Setelah ditambahkan, jadwal perawatan otomatis dibuat.

### Alur 2: Diagnosis Penyakit
1. Dari halaman utama, pengguna masuk ke menu "Penyakit".
2. Pengguna melihat daftar hama/penyakit dengan gambar.
3. Pengguna memilih salah satu untuk melihat detail cara penanganan.
4. (Versi Pro) Pengguna mengambil foto bagian tanaman yang sakit, AI memberikan kemungkinan diagnosis.

## 5. Kebutuhan Non-Fungsional

### Performa
- **Waktu Muat:** Halaman utama < 2 detik.
- **Waktu Respons:** Interaksi UI < 200ms.
- **Identifikasi AI:** Proses identifikasi < 5 detik.

### Keamanan
- **Otentikasi:** Menggunakan OAuth 2.0 (Google Sign-In) untuk MVP.
- **Perlindungan Data:** Data pengguna (email, koleksi tanaman) harus disimpan dengan aman.

### Kompatibilitas
- **Perangkat:** Mobile (Android & iOS).
- **OS:** Android 8.0+, iOS 14+.

### Aksesibilitas
- **Kebutuhan Spesifik:** Ukuran font dapat disesuaikan, kontras warna memenuhi standar dasar.

## 6. Spesifikasi Teknis (Gambaran Umum)

### Frontend
- **Tumpukan Teknologi (Tech Stack):** React Native (untuk cross-platform Android/iOS).
- **Sistem Desain:** Menggunakan komponen UI dasar dari React Native, dengan tema warna hijau dan natural.

### Backend
- **Tumpukan Teknologi (Tech Stack):** Python dengan FastAPI (untuk kecepatan dan kemudahan pengembangan API, serta integrasi dengan model AI).
- **Kebutuhan API:** RESTful API.
- **Database:** PostgreSQL (untuk struktur data yang relasional seperti pengguna, tanaman, jadwal).
- **Penyimpanan Gambar:** Cloud Storage (misal: AWS S3, Google Cloud Storage).

### Infrastruktur & AI
- **Hosting:** Platform as a Service (PaaS) seperti Heroku atau Vercel untuk kemudahan deployment.
- **Model AI:** Akan mengembangkan model AI identifikasi tanaman sendiri secara internal, dengan fokus pada dataset flora lokal Indonesia. Untuk MVP awal, fungsionalitas identifikasi akan menggunakan respons dummy atau model dasar yang sangat terbatas, sambil menunggu pengembangan model internal.
- **CI/CD:** GitHub Actions untuk otomatisasi build dan deployment.

## 7. Rencana Rilis

### MVP (v1.0)
- **Fitur:** Identifikasi Tanaman (dengan 20 tanaman populer), Database Perawatan, Jadwal Perawatan Cerdas.
- **Target Waktu:** 3 bulan dari sekarang.
- **Kriteria Sukses MVP:** Aplikasi stabil, berhasil melakukan fungsi inti, dan mendapatkan 1.000 pengguna pertama dengan feedback positif.

### Rilis Berikutnya
- **v1.1:** Menambahkan Forum Komunitas dan Ensiklopedia Hama.
- **v1.2:** Memperluas database tanaman hingga 100 jenis.
- **v2.0:** Meluncurkan fitur "Tanam Rawat Pro" dengan diagnosis penyakit via AI dan konsultasi ahli.

## 8. Pertanyaan Terbuka & Asumsi

- **Pertanyaan 1:** Di mana kita akan mendapatkan dataset gambar tanaman lokal yang berkualitas untuk melatih model AI?
- **Asumsi 1:** Pengguna bersedia memberikan izin akses kamera dan notifikasi.
- **Asumsi 2:** Ada cukup banyak ahli hortikultura lokal yang bisa diajak bekerja sama untuk konten di masa depan.

## 9. Lampiran

### Wawasan dari Percakapan dengan AI
- *Akan diisi seiring berjalannya proyek.*

### Glosarium
- **MVP:** Minimum Viable Product - Versi produk paling dasar yang sudah bisa digunakan oleh pengguna.
- **Hiper-lokal:** Sangat spesifik untuk kondisi dan budaya lokal.
