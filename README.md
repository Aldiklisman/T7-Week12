# Dashboard Visualisasi Data - PySide6

Author:
- Nama : Mohammad Klisman Reynaldi
- NIM  : F1D022063
- Kelas: PemVisD

Deskripsi singkat: Aplikasi dashboard PySide6, Pandas, dan Matplotlib yang menampilkan data supermarket (tabel, filter, dan chart).

---

Aplikasi singkat:
- PySide6 + Pandas + Matplotlib
- Menampilkan tabel, filter `Product line`, chart bar dan pie, serta export PNG/CSV

---

Fitur utama:
- Menampilkan data mentah dalam `QTableView` dari file CSV
- Filter kategori berdasarkan kolom `Product line`
- Dua chart Matplotlib: bar chart (penjualan per branch) dan pie chart (proporsi product line)
- Tombol refresh dan export (chart ke PNG, tabel terfilter ke CSV)

Struktur project:
- `src/` - kode sumber aplikasi
- `data/` - dataset CSV
- `requirements.txt` - dependensi

Cara jalankan:
1. Buat virtual environment dan install dependensi:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Jalankan aplikasi:

```powershell
python src\main.py
```

Catatan singkat:
- Dataset contoh yang digunakan: `data/supermarket_sales_sample.csv` (asal: Kaggle)
- Aplikasi saat ini membaca CSV lokal. README mencantumkan langkah opsional untuk mengunduh dataset dari Kaggle.
- Jika ingin menggunakan SQLite, Anda bisa menyesuaikan `src/data_loader.py` untuk membaca dari file `.db` (contoh: `pd.read_sql_table(...)`).

---

Dataset (Kaggle) — ringkas dan bukti sumber
-------------------------------------------------
Dataset yang dipakai: "Supermarket Sales" (Kaggle)
URL dataset: https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales

File yang disertakan di repo ini: `data/supermarket_sales_sample.csv` (salinan subset/versi dataset Kaggle).

Penjelasan singkat kolom utama (untuk penilaian):
- `Invoice ID` — ID transaksi unik
- `Branch` — Cabang toko (kode singkat)
- `City` — Kota tempat cabang berada
- `Customer type` — Member atau Normal
- `Gender` — Gender pelanggan
- `Product line` — Kategori produk (mis. "Health and beauty", "Electronic accessories")
- `Unit price` — Harga per unit
- `Quantity` — Jumlah unit pada transaksi
- `Tax 5%` — Pajak 5% pada transaksi
- `Sales` / `Total` — Total nilai transaksi (kolom di dataset bisa bernama `Sales`; loader membuat `Total` jika perlu)
- `Date`, `Time` — Tanggal dan waktu transaksi
- `Payment` — Metode pembayaran (Cash/Credit card/Ewallet)
- `Rating` — Rating pelanggan (opsional, numeric)

- Dataset cocok untuk dashboard karena memungkinkan analisis per cabang, per kategori produk, dan tren ringkasan penjualan.

Cara mengunduh otomatis dari Kaggle (opsional)
- Persyaratan: install `kaggle` package dan siapkan `kaggle.json` (API token) di folder `%USERPROFILE%\.kaggle\kaggle.json`.
- Contoh perintah (PowerShell):

```powershell
pip install kaggle
# letakkan kaggle.json di C:\Users\<YourUser>\.kaggle\kaggle.json
kaggle datasets download -d faresashraf1001/supermarket-sales -p data --unzip
```

Atau jalankan skrip Python yang disertakan:

```powershell
python scripts\download_kaggle.py
```

Lihat halaman Kaggle dataset untuk detail lisensi dan atribusi.

## Screenshots

Screenshot yang ada di folder `screenshot/` (langsung ditampilkan di bawah):

![Tampilan Awal](screenshot/TampilanAwal.png)

_Gambar 1: Tampilan awal aplikasi saat pertama kali dibuka (tabel dan chart)._

![Tampilan Awal Minimize](screenshot/Tampilan%20Awal%20Minimize.png)

_Gambar 2: Tampilan aplikasi setelah jendela diminimize / ukuran berbeda._

![Tampilan Ekspor Chart dan Tabel](screenshot/Tampilan%20Ekspor%20Chart%20dan%20Tabel.png)

_Gambar 3: Dialog ekspor chart (menyimpan PNG) dan ekspor tabel (CSV)._

![Tampilan Ekspor Chart dan Tabel 2](screenshot/Tampilan%20Ekspor%20Chart%20dan%20Tabel2.png)

_Gambar 4: Contoh konfirmasi atau lokasi file hasil ekspor (opsional)._ 

![Tampilan Filter Product Line dan Pie Grouping](screenshot/Tampilan%20Filter%20Product%20Line%20dan%20Pie%20Grouping%20.png)

_Gambar 5: Filter `Product line` dan kontrol `Pie grouping` untuk memilih kolom kategori pie chart._

![Tampilan Mengurutkan Kolom Unit Price](screenshot/Tampilan%20Mengurutkan%20Kolom%20Unit%20Price%20.png)

_Gambar 6: Contoh pengurutan kolom (sort) pada kolom `Unit price` di tabel._

![Tampilan Refresh Setelah Merubah Unit Price](screenshot/Tampilan%20Refresh%20Setelah%20Merubah%20Unit%20Price%20Dari%2099.99%20menjadi%2099.88.png)

_Gambar 7: Hasil refresh setelah merubah nilai `Unit price` (menunjukkan update data dan chart setelah refresh)._

