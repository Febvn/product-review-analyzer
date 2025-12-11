# 🌟 Product Review Analyzer AI

## 👨‍💻 Kontributor

Nama  :Febrian Valentino Nugroho
NIM   :123140034
Kelas :RA

Teknologi: React, FastAPI, PostgreSQL, Google Gemini AI.

<div align="center">

![Product Review Analyzer](https://img.shields.io/badge/Product%20Review-Analyzer-00d4ff?style=for-the-badge&logo=sparkles)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql)

**Aplikasi Analisis Sentimen dan Ekstraksi Poin Penting Berbasis AI**

</div>

---

## 📋 Daftar Isi

1. [Tentang Proyek](#-tentang-proyek)
2. [Fitur Utama](#-fitur-utama)
3. [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
4. [Struktur Proyek](#-struktur-proyek)
5. [Asset Dokumentasi](#️-asset-dokumentasi)
6. [Prasyarat Sistem](#-prasyarat-sistem)
7. [Panduan Instalasi & Menjalankan](#-panduan-instalasi--menjalankan)
8. [Dokumentasi API](#-dokumentasi-api)
9. [Troubleshooting](#-troubleshooting)

---

## 📖 Tentang Proyek

**Product Review Analyzer** adalah aplikasi web modern yang dirancang untuk membantu pengguna memahami ulasan produk secara mendalam menggunakan kecerdasan buatan (AI). Aplikasi ini tidak hanya menentukan sentiment (positif/negatif/netral) dari sebuah ulasan, tetapi juga mengekstrak poin-poin kunci (key points) yang menjadi sorotan dalam ulasan tersebut.

Aplikasi ini dibangun dengan arsitektur **Fullstack** yang memisahkan antara Frontend (React) dan Backend (FastAPI), serta menggunakan database PostgreSQL untuk menyimpan riwayat analisis.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🎭 **Analisis Sentimen** | Mengidentifikasi apakah ulasan bersifat Positif, Negatif, atau Netral menggunakan model Deep Learning (Hugging Face Transformers). |
| 🔑 **Ekstraksi Poin Penting** | Menggunakan Google Gemini AI untuk merangkum poin-poin utama dari ulasan panjang menjadi daftar poin yang mudah dibaca. |
| 📊 **Riwayat Analisis** | Menyimpan semua hasil analisis ke dalam database sehingga dapat diakses kembali kapan saja. |
| 🔍 **Filtering & Sortir** | Fitur untuk menyaring riwayat ulasan berdasarkan sentimen (hanya positif/negatif). |
| 🗑️ **Manajemen Data** | Kemampuan untuk menghapus ulasan yang sudah tidak diperlukan. |
| 🎨 **UI Modern** | Antarmuka pengguna yang responsif dan estetis menggunakan gaya **Glassmorphism**, animasi halus, dan tema gelap (Dark Theme). |

---

## 🛠 Teknologi yang Digunakan

### Frontend (Sisi Klien)
- **React.js**: Library UI utama untuk membangun antarmuka interaktif.
- **Vite**: Build tool super cepat untuk pengembangan React.
- **Styled Components**: Library CSS-in-JS untuk styling komponen yang modular dan dinamis.
- **Lucide React**: Koleksi ikon yang ringan dan modern.
- **Axios**: Library untuk melakukan HTTP request ke backend.

### Backend (Sisi Server)
- **FastAPI**: Framework Python modern yang sangat cepat untuk membangun API.
- **SQLAlchemy**: ORM (Object Relational Mapping) untuk interaksi dengan database SQL.
- **PostgreSQL**: Database relasional yang robust untuk penyimpanan data.
- **Hugging Face Transformers**: Library AI untuk Natural Language Processing (Analisis Sentimen).
- **Google Gemini API**: Layanan Generative AI untuk ekstraksi teks cerdas.
- **Uvicorn**: Server ASGI untuk menjalankan aplikasi FastAPI.

---

## 📂 Struktur Proyek

Berikut adalah penjelasan detail mengenai struktur file dan folder dalam proyek ini:

```
TUGAS3/
├── backend/                  # Folder BackEnd (API & Database)
│   ├── app/
│   │   ├── services/         # Layanan Integrasi AI
│   │   │   ├── sentiment.py  # Logika analisis sentimen (Hugging Face)
│   │   │   └── gemini.py     # Logika ekstraksi poin (Google Gemini)
│   │   ├── config.py         # Konfigurasi environment (DB URL, API Keys)
│   │   ├── database.py       # Koneksi database SQLAlchemy
│   │   ├── main.py           # Entry point aplikasi FastAPI
│   │   ├── models.py         # Definisi Tabel Database (Schema DB)
│   │   ├── routes.py         # Definisi Endpoint API (URL paths)
│   │   └── schemas.py        # Validasi data request/response (Pydantic)
│   ├── requirements.txt      # Daftar library Python yang dibutuhkan
│   ├── run.py                # Script untuk menjalankan server
│   └── .env                  # File variabel lingkungan (RAHASIA)
│
├── frontend/                 # Folder FrontEnd (React UI)
│   ├── src/
│   │   ├── api/              # Konfigurasi Axios
│   │   ├── components/       # Komponen UI Reusable (Lihat detail di bawah)
│   │   │   ├── AnalysisResult.jsx  # Menampilkan hasil analisis & skor
│   │   │   ├── Loader.jsx          # Animasi loading kubus 3D
│   │   │   ├── ReviewCard.jsx      # Kartu untuk item riwayat review
│   │   │   ├── ReviewForm.jsx      # Form input review
│   │   │   ├── ReviewList.jsx      # Grid daftar riwayat review
│   │   │   ├── SocialButton.jsx    # Tombol sosial media dekoratif
│   │   │   └── Toast.jsx           # Notifikasi popup
│   │   ├── App.jsx           # Komponen utama layout
│   │   └── main.jsx          # Entry point React
│   ├── index.html            # File HTML utama
│   └── package.json          # Daftar library JS yang dibutuhkan
│
└── README.md                 # Dokumentasi Proyek
```

---

## 🖼️ Screenshot Aplikasi

Berikut adalah tampilan aplikasi **Product Review Analyzer**:

### Desktop View

#### Landing Page
![Landing Page](screenshots/landing%20page.png)
*Halaman utama aplikasi dengan hero section, deskripsi fitur, dan form analisis review. UI menggunakan tema dark dengan efek glassmorphism dan gradien ungu-biru yang modern.*

#### Form Analisis Review
![Analyze Review Form](screenshots/Analyze%20review%20Form.png)
*Detail form analisis review dengan textarea untuk input review, input nama produk, dan tombol "Analyze Review" dengan desain glassmorphism yang premium.*

#### Analysis History
![Analysis History](screenshots/Analysis%20History.png)
*Section "Analysis History" menampilkan grid cards berisi riwayat review yang telah dianalisis. Setiap card menunjukkan sentiment badge (positive/negative/neutral), product name, review text, key points, confidence score, dan action buttons (Copy, Edit, Delete).*

### Mobile View (Responsive)

<div align="center">
  <img src="screenshots/mobile%20landing.PNG" width="300" alt="Mobile Landing Page">
  <img src="screenshots/analyze%20review%20mobile.PNG" width="300" alt="Mobile Review Form">
  <img src="screenshots/Footer%20mobile.PNG" width="300" alt="Mobile Footer">
</div>

*Aplikasi fully responsive dengan layout yang dioptimalkan untuk perangkat mobile/smartphone.*

### Asset Fungsional

| Nama File | Ukuran | Deskripsi |
|-----------|--------|-----------|
| **favicon.png** | 4.4 KB | Icon aplikasi yang muncul di tab browser. Berupa logo atau simbol representatif dari Product Review Analyzer. File ini di-link di `index.html` sebagai favicon untuk branding aplikasi. |
| **loading.jpg** | 34 KB | Gambar loading/placeholder yang ditampilkan saat proses analisis sedang berjalan. Memberikan feedback visual kepada user bahwa sistem sedang memproses request mereka. |

### Catatan
- Semua screenshot menggunakan **tema dark mode** dengan **glassmorphism effect** untuk konsistensi visual.
- Asset gambar di-import dan digunakan oleh komponen React (misalnya di `App.jsx` atau komponen lainnya).
- Screenshot disimpan di folder `screenshots/` untuk dokumentasi.

---

## 💻 Prasyarat Sistem

Sebelum memulai, pastikan komputer Anda telah terinstal:

1.  **Node.js** (Versi 18 atau lebih baru) - [Download](https://nodejs.org/)
2.  **Python** (Versi 3.10 atau lebih baru) - [Download](https://www.python.org/)
3.  **PostgreSQL** (Database Server) - [Download](https://www.postgresql.org/)
4.  **Git** (Untuk clone repository) - [Download](https://git-scm.com/)

Anda juga memerlukan **API Key** (gratis):
-   **Google Gemini API Key**: Dapatkan di [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## 🚀 Panduan Instalasi & Menjalankan

Ikuti langkah-langkah ini secara berurutan untuk menjalankan aplikasi di komputer lokal Anda.

### Langkah 1: Clone Repository
```bash
git clone <url-repository-anda>
cd TUGAS3
```

### Langkah 2: Setup Backend (Python)

1.  Buka terminal/command prompt, masuk ke folder `backend`:
    ```bash
    cd backend
    ```

2.  Buat Virtual Environment (agar library tidak tercampur dengan sistem):
    ```bash
    # Windows
    python -m venv venv
    
    # Mac/Linux
    python3 -m venv venv
    ```

3.  Aktifkan Virtual Environment:
    ```bash
    # Windows
    venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

4.  Install dependencies (library) yang dibutuhkan:
    ```bash
    pip install -r requirements.txt
    ```

5.  Buat file konfigurasi `.env`:
    -   Salin file `.env.example` menjadi `.env`.
    -   Buka file `.env` dengan text editor (Notepad/VS Code).
    -   Isi konfigurasi berikut:
    ```env
    # URL Database PostgreSQL Anda
    # Format: postgresql://username:password@localhost:5432/nama_database
    DATABASE_URL=postgresql://postgres:password123@localhost:5432/review_analyzer
    
    # API Key Google Gemini Anda
    GEMINI_API_KEY=masukan_api_key_gemini_disini
    ```

6.  Siapkan Database:
    -   Pastikan PostgreSQL server sudah berjalan.
    -   Buat database baru bernama `review_analyzer` (bisa lewat pgAdmin atau SQL Shell).

7.  Jalankan Server Backend:
    ```bash
    python run.py
    ```
    *Server akan berjalan di http://localhost:8000*

### Langkah 3: Setup Frontend (React)

1.  Buka terminal **BARU** (jangan tutup terminal backend), masuk ke folder `frontend`:
    ```bash
    cd frontend
    ```

2.  Install dependencies (library JavaScript):
    ```bash
    npm install
    ```

3.  Jalankan Server Frontend:
    ```bash
    npm run dev
    ```
    *Server akan berjalan di http://localhost:5173*

4.  Buka browser dan akses `http://localhost:5173`. Aplikasi siap digunakan! 🎉

---

## 📡 Dokumentasi API

Aplikasi ini menyediakan REST API yang bisa diuji langsung via Swagger UI di `http://localhost:8000/docs`.

### **1. Menganalisis Review**
-   **Endpoint**: `POST /api/analyze-review`
-   **Deskripsi**: Menganalisis teks review baru.
-   **Body**:
    ```json
    {
      "review_text": "Produk ini sangat bagus, baterainya awet dan layarnya jernih.",
      "product_name": "Smartphone X"
    }
    ```

### **2. Mendapatkan Semua Review**
-   **Endpoint**: `GET /api/reviews`
-   **Deskripsi**: Mengambil daftar riwayat review.
-   **Query Params**: `skip` (offset), `limit` (jumlah data), `sentiment` (filter sentimen).

### **3. Menghapus Review**
-   **Endpoint**: `DELETE /api/reviews/{id}`
-   **Deskripsi**: Menghapus data review berdasarkan ID.

---

## ❓ Troubleshooting

**Masalah**: Error "Connection refused" pada Backend.
**Solusi**: Pastikan PostgreSQL server sudah menyala dan URL database di `.env` sudah benar (username & password).

**Masalah**: Frontend tidak bisa mengambil data (Network Error).
**Solusi**: Pastikan server Backend sedang berjalan di port 8000. Cek console browser (F12) untuk detail error.

**Masalah**: Analisis gagal atau "Partial Analysis".
**Solusi**: Cek koneksi internet. Pastikan `GEMINI_API_KEY` di `.env` valid dan kuota API belum habis.

---


