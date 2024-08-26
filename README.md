Berikut adalah dokumentasi untuk script `SuperNano`, sebuah editor berbasis konsol yang ditulis menggunakan Python dengan modul `py_cui`. Editor ini menyediakan antarmuka untuk mengelola file dan direktori serta menyediakan fitur pengeditan teks dasar. 

---

# Dokumentasi SuperNano

## Deskripsi
`SuperNano` adalah editor teks berbasis konsol yang memungkinkan pengguna untuk membuka, mengedit, menyimpan, dan menghapus file secara langsung dari antarmuka berbasis teks. Aplikasi ini juga menyediakan fitur edit file, navigasi direktori dan pencarian file.

### Fitur Utama:
- **Navigasi Direktori**: Menampilkan isi dari direktori dan memungkinkan navigasi antar direktori.
- **Pengeditan Teks**: Memungkinkan pengeditan file teks dengan fitur undo.
- **Penyimpanan File**: Menyimpan perubahan ke file yang dibuka.
- **Penghapusan File**: Menghapus file yang dipilih.
- **Pencarian File**: Mencari file atau direktori berdasarkan nama.

## Struktur Kode
Script ini dibagi menjadi beberapa bagian penting:
1. **Imports**: Bagian ini mengimpor modul yang diperlukan untuk menjalankan aplikasi. Selain modul standar Python, script ini juga mengimpor beberapa modul khusus yang berfungsi untuk manajemen sistem, manajemen file, penanganan kesalahan, dan pengaturan waktu.

2. **Konfigurasi Logging**: Mengatur logging untuk mencatat event atau kesalahan yang terjadi selama aplikasi berjalan.

3. **Fungsi `setTitle`**: Fungsi ini digunakan untuk mengatur judul dari window konsol sesuai dengan path file atau direktori yang sedang dibuka.

4. **Class `SuperNano`**: Class ini merupakan inti dari aplikasi yang mengatur berbagai fitur yang ada seperti membuka file, menyimpan file, menghapus file, navigasi direktori, dan lain-lain.

5. **Fungsi `parse_args`**: Fungsi ini digunakan untuk memparsing argumen baris perintah yang menentukan file atau direktori target untuk diedit.

6. **Fungsi `main`**: Fungsi utama yang menginisialisasi objek `PyCUI`, mengatur judul aplikasi, dan memulai antarmuka pengguna.

7. **Safe Execution**: Menggunakan `SafeProcessExecutor` untuk menjalankan aplikasi dengan aman menggunakan thread.

## Detail Implementasi

### Class `SuperNano`
Class ini menangani seluruh fungsionalitas aplikasi dan diinisialisasi dengan parameter `root` (objek `PyCUI`) dan `path` (path file atau direktori). Beberapa metode penting dalam class ini adalah:

- **`__init__`**: Inisialisasi antarmuka dan menentukan apakah `path` adalah file atau direktori.
- **`open_new_directory`**: Membuka dan menampilkan isi dari direktori baru.
- **`open_file_dir`**: Membuka file atau navigasi ke direktori yang dipilih.
- **`save_opened_file`**: Menyimpan file yang sedang dibuka.
- **`delete_selected_file`**: Menghapus file yang dipilih.
- **`search_files`**: Mencari file di dalam direktori berdasarkan input pencarian.

### Fungsi `setTitle`
Fungsi ini mengatur judul window konsol dengan nama file atau direktori yang sedang dibuka, dan menyesuaikan panjangnya agar tidak melebihi batas karakter tertentu.

### Fungsi `parse_args`
Fungsi ini digunakan untuk memproses argumen yang diberikan melalui command line. Argumen tersebut akan menentukan file atau direktori mana yang akan dibuka oleh `SuperNano`.

### Safe Execution
Penggunaan `SafeProcessExecutor` memastikan bahwa aplikasi berjalan dengan aman dan efisien, terutama saat menjalankan fungsi yang mungkin memakan waktu.

## Cara Penggunaan
Jalankan script ini melalui command line dengan memberikan argumen berupa path file atau direktori yang ingin diedit. Contoh:
```
python supernano.py /path/to/directory_or_file
```

## Lisensi
Aplikasi ini dibuat oleh Ramsyan Tungga Kiansantang dan dilisensikan di bawah [Lisensi GPL v3](https://www.gnu.org/licenses/gpl-3.0.html). Untuk kontribusi atau pelaporan bug, silakan kunjungi repositori Github yang telah disediakan.

## Versi
- **Versi**: V1.0.0
- **Tanggal Rilis**: 18 Juli 2024

---

## Kesimpulan
`SuperNano` adalah editor teks berbasis konsol yang dirancang untuk memudahkan pengelolaan file dan direktori secara langsung dari command line. Aplikasi ini menawarkan alat yang ringan untuk pengguna yang bekerja di lingkungan berbasis teks.

Jika ada pertanyaan atau butuh bantuan lebih lanjut terkait implementasi, jangan ragu untuk menghubungi pengembang atau melihat dokumentasi tambahan yang mungkin tersedia.
