[![LcfherShell](https://github.com/LcfherShell/local_svg/blob/main/lcfhershell.svg)](https://github.com/LcfherShell)
<img src="https://repository-images.githubusercontent.com/847198464/b36c0223-b3fa-4846-8f82-21e1b48d7021" alt="SuperNano" style="max-width: 100%; height: auto;" />

Berikut adalah dokumentasi untuk script `SuperNano`, sebuah text editor berbasis console yang kuat khusus platform Windows 8, 10, 11.

---

# Dokumentasi SuperNano

## Deskripsi
`SuperNano` adalah sebuah text editor berbasis console yang dikembangkan menggunakan Python dan pustaka `urwid[curses]`. Aplikasi ini dirancang untuk memberikan pengguna kemampuan untuk mengedit teks, mengelola file, dan melakukan inspeksi modul Python langsung dari antarmuka berbasis console. `SuperNano` mendukung beberapa fitur seperti undo-redo, clipboard (copy-paste), pencarian file, dan inspeksi modul Python.

## Fitur Utama
- **Text Editing**: Editor teks dengan dukungan multiline, undo-redo, copy-paste, dan penyimpanan file.
- **File Management**: Memungkinkan navigasi direktori, membuka dan menyimpan file, serta membuat dan menghapus file.
- **Module Inspection**: Fitur untuk melakukan inspeksi modul Python, C, NodeJS, dan PHP, menampilkan informasi tentang variabel global, kelas, dan fungsi yang ada di dalam modul.


## Kelas dan Metode

### 1. `SuperNano`
`SuperNano` adalah kelas utama yang mengatur seluruh aplikasi, termasuk inisialisasi, pembuatan menu, dan manajemen UI.

#### Atribut:
- **current_path**: Menyimpan path direktori saat ini.
- **current_file_name**: Menyimpan nama file yang sedang dibuka.
- **undo_stack**, **redo_stack**: Stack yang digunakan untuk menyimpan state teks guna mendukung fitur undo-redo.
- **overlay**: Widget yang digunakan untuk menampilkan popup.
- **modulepython**: Objek dari `ModuleInspector` yang digunakan untuk inspeksi modul Python, C, NodeJS, dan PHP.
- **loop**: Objek `urwid.MainLoop` yang menangani event loop aplikasi.
- **loading_alarm**, **system_alarm**: Alarm untuk mengatur timing penggantian layout dan memonitor sistem.

#### Metode:
- **`__init__(self, start_path=".")`**: Inisialisasi kelas, menyiapkan path awal, widget, dan memulai event loop.
- **`load_main_menu(self)`**: Menyiapkan dan menampilkan menu utama setelah periode loading.
- **`switch_to_secondary_layout(self)`**: Mengubah layout aplikasi ke menu utama.
- **`setup_main_menu(self)`**: Mengatur widget untuk menu utama, termasuk daftar file, editor teks, dan tombol-tombol fungsional.
- **`create_modules_menus(self, listmodulename)`**: Membuat tombol untuk setiap modul yang ada di `sys.path`.
- **`inspect_module(self, button, module_name)`**: Menampilkan hasil inspeksi modul dalam footer.
- **`setup_popup(self, options, title, descrip="")`**: Menyiapkan konten dan layout untuk menu popup.
- **`show_popup(self, title, descrip, menus)`**: Menampilkan popup menu dengan judul, deskripsi, dan opsi yang diberikan.
- **`close_popup(self, button)`**: Menutup popup dan mengembalikan tampilan ke layout utama.
- **`get_file_list(self)`**: Mengambil daftar file dan direktori di path saat ini.
- **`handle_input(self, key)`**: Menangani input keyboard untuk berbagai tindakan seperti keluar, menyimpan, menghapus, undo, redo, copy-paste, dan refresh UI.
- **`get_current_edit(self)`**: Mengembalikan widget edit yang sedang difokuskan (text editor atau search edit).
- **`set_focus_on_click(self, widget, new_edit_text, index)`**: Mengatur fokus pada widget edit berdasarkan klik dan indeks.
- **`copy_text_to_clipboard(self)`**: Menyalin teks dari widget edit yang sedang aktif ke clipboard.
- **`paste_text_from_clipboard(self)`**: Menempelkan teks dari clipboard ke widget edit yang sedang aktif.

### 2. `ModuleInspector`
Kelas ini bertanggung jawab untuk memuat dan menginspeksi modul-modul Python, C, NodeJS, dan PHP. Informasi yang dapat diambil meliputi variabel global, kelas, dan fungsi dalam modul.

#### Atribut:
- **modules**: Menyimpan daftar nama modul yang ditemukan di `sys.path`.

#### Metode:
- **`get_moduleV2(self, paths)`**: Mengembalikan daftar modul yang ditemukan di path yang diberikan.
- **`inspect_module(self, module_name)`**: Menginspeksi modul dengan nama yang diberikan dan mengembalikan detail modul tersebut.

## Penggunaan
1. **Menjalankan Aplikasi**: Jalankan script `SuperNano` dengan Python 3.6 ke atas di terminal Anda.
2. **Navigasi File**: Gunakan panah atas dan bawah untuk memilih file di direktori. Tekan Enter untuk membuka file.
3. **Edit Teks**: Setelah file terbuka, teks dapat diedit langsung di editor. Gunakan `Ctrl+S` untuk menyimpan perubahan.
4. **Undo-Redo**: Gunakan `Ctrl+Z` untuk undo dan `Ctrl+Y` untuk redo.
5. **Copy-Paste**: Gunakan `Ctrl+C` untuk copy dan `Ctrl+V` untuk paste.
6. **Inspeksi Modul**: Pilih modul dari daftar yang tersedia di UI untuk menampilkan informasi tentang modul tersebut.
7. **Keluar dari Aplikasi**: Tekan `Ctrl+Q` atau `ESC` untuk keluar dari aplikasi.


## Syarat
- Python V3.8^
- Nodejs
- Clang [tidak wajib]
- Composer PHP [tidak wajib]
- Module pip (Python) : requirements.txt
- Module NPM (Node) : acorn, php-parser


## Cara Penggunaan
Jalankan script ini melalui command line dengan memberikan argumen berupa path file atau direktori yang ingin diedit. Contoh:
```
python supernano.py /path/to/directory_or_file
```

## Lisensi
Aplikasi ini dibuat oleh Ramsyan Tungga Kiansantang dan dilisensikan di bawah [Lisensi GPL v3](https://www.gnu.org/licenses/gpl-3.0.html). Untuk kontribusi atau pelaporan bug, silakan kunjungi repositori Github yang telah disediakan.

## Versi
- **Versi**: V2.2.1
- **Tanggal Rilis**: 30 Agustus 2024

---

## Kesimpulan
`SuperNano` adalah editor teks berbasis konsol yang dirancang untuk memudahkan pengelolaan file dan direktori secara langsung dari command line. Aplikasi ini menawarkan alat yang kuat untuk pengguna yang bekerja di lingkungan berbasis teks.

Jika ada pertanyaan atau butuh bantuan lebih lanjut terkait implementasi, jangan ragu untuk menghubungi pengembang atau melihat dokumentasi tambahan yang mungkin tersedia.
