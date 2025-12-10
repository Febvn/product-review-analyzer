 # Penganalisis Ulasan Produk

Aplikasi penganalisis ulasan produk berbasis AI dengan frontend React + Vite dan backend FastAPI.

Repositori ini terdiri dari dua bagian utama:

- `frontend/` — aplikasi single-page React (Vite). Menggunakan API backend untuk mengirim ulasan dan menampilkan hasil analisis.
- `backend/` — aplikasi FastAPI yang melakukan analisis sentimen (Hugging Face) dan ekstraksi poin penting (Google Gemini) serta menyimpan hasil ke database.

---

## Ringkasan cepat

- Frontend: `frontend/` (Vite, React, styled-components)
- Backend API: `backend/` (FastAPI, SQLAlchemy, Postgres)
- Port pengembangan yang digunakan secara default:
  - Frontend: `http://localhost:5173`
  - Backend API: `http://localhost:8000` (dokumen di `http://localhost:8000/docs`)

---

## Fitur

- Analisis sentimen (positif / negatif / netral)
- Ekstraksi poin-poin penting
- Menyimpan hasil analisis di PostgreSQL
- Daftar riwayat ulasan, penyaringan, penghapusan
- Antarmuka modern dengan styled-components

---

## Isi README ini

1. Prasyarat
2. Pengembangan lokal (backend & frontend)
3. Variabel lingkungan
4. Endpoint API
5. Catatan deployment (Vercel untuk frontend + opsi untuk backend)
6. Pemecahan masalah

---

## 1) Prasyarat

- Node.js 18+ dan npm
- Python 3.10+
- PostgreSQL (atau layanan kompatibel PostgreSQL)
- (Opsional) Kunci API: Google Gemini dan (opsional) Hugging Face

---

## 2) Pengembangan Lokal

Ikuti langkah-langkah berikut untuk menjalankan backend dan frontend secara lokal.

### Backend (FastAPI)

1. Buka terminal dan masuk ke folder backend:

```powershell
cd backend
```

2. Buat dan aktifkan virtual environment:

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Jika Activate.ps1 diblokir, jalankan: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Pasang dependensi Python:

```powershell
pip install -r requirements.txt
```

4. Salin dan sunting file environment:

```powershell
copy .env.example .env
# Kemudian edit .env untuk mengatur DATABASE_URL, GEMINI_API_KEY, dll.
```

Contoh `DATABASE_URL` (Postgres):

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/review_analyzer
```

5. Buat database (Postgres):

```sql
# Menggunakan psql
CREATE DATABASE review_analyzer;
```

6. Jalankan server (development dengan autoreload):

```powershell
python run.py
```

API akan tersedia di `http://localhost:8000` dan dokumentasi API di `http://localhost:8000/docs`.

Catatan:
- Konfigurasi dibaca dari `backend/app/config.py` menggunakan variabel lingkungan (dan `.env`).
- Aplikasi FastAPI mendaftarkan route utama di `backend/app/routes.py`.

### Frontend (React + Vite)

1. Buka terminal baru dan masuk ke folder frontend:

```powershell
cd frontend
```

2. Pasang dependensi:

```powershell
npm install
```

3. Konfigurasikan frontend untuk memanggil API dengan menyalin atau mengedit nilai `.env`. Demo menggunakan `VITE_API_URL`:

Buat (atau edit) `.env` di `frontend/` dengan:

```
VITE_API_URL=http://localhost:8000
```

4. Jalankan dev server:

```powershell
npm run dev
```

Buka `http://localhost:5173` di browser Anda.

---

## 3) Variabel Lingkungan (ringkasan)

Backend (`backend/.env`)
- `DATABASE_URL` — URL DB untuk SQLAlchemy (Postgres). Contoh: `postgresql://user:pass@host:5432/dbname`
- `GEMINI_API_KEY` — Kunci API Google Gemini (untuk ekstraksi poin penting)
- `HUGGINGFACE_API_KEY` — Kunci Hugging Face opsional (jika digunakan)
- `HOST` — host server (default `0.0.0.0`)
- `PORT` — port server (default `8000`)

Frontend (`frontend/.env`)
- `VITE_API_URL` — URL dasar untuk backend API (mis. `https://api.example.com` atau `http://localhost:8000`)

File `app/config.py` di backend sudah berisi CORS origin default yang termasuk origin dev Vite lokal.

---

## 4) Endpoint API

Endpoint utama yang diimplementasikan di `backend/app/routes.py`:

- `POST /api/analyze-review` — menganalisis ulasan (body: `review_text`, opsional `product_name`). Mengembalikan hasil analisis yang tersimpan.
- `GET /api/reviews` — daftar ulasan dengan query opsional: `skip`, `limit`, `sentiment`.
- `GET /api/reviews/{id}` — mendapatkan ulasan berdasarkan id.
- `DELETE /api/reviews/{id}` — menghapus ulasan berdasarkan id.
- `GET /health` — pemeriksaan kesehatan sederhana.

Gunakan dokumentasi interaktif di `http://localhost:8000/docs` untuk mengeksplor skema dan payload contoh.

---

## 5) Catatan Deployment

Frontend:
- Ini adalah build Vite; `frontend/package.json` sudah berisi script `build` dan `preview`.
- Deployment paling mudah: Vercel (direkomendasikan). Saat menghubungkan repo, atur build command `npm run build` dan output directory `dist`.
- Set `VITE_API_URL` di environment Vercel agar mengarah ke URL backend produksi Anda.

Opsi backend (direkomendasikan):
- Render / Railway / Fly / Heroku — pilih yang mendukung proses server persisten dan Postgres.
- Jika ingin serverless, Anda bisa mengubah backend menjadi fungsi serverless, tapi perhatikan repo saat ini mengharapkan proses FastAPI persisten dan database Postgres.

Langkah singkat untuk Render / Railway (tingkat tinggi):
1. Buat layanan PostgreSQL dan catat connection URL-nya.
2. Deploy layanan backend (Python); set variabel lingkungan `DATABASE_URL`, `GEMINI_API_KEY`, dll.
3. Pastikan proses web menjalankan `python run.py` atau gunakan perintah Uvicorn:`uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

Catatan tentang Vercel + backend: Vercel cocok untuk frontend statis. Anda bisa menempatkan backend di host lain dan mengatur `VITE_API_URL` sesuai.

---

## 6) Pemecahan Masalah & Tips

- Jika CORS memblokir permintaan, pastikan origin `frontend` ada di `backend/app/config.py` pada `ALLOWED_ORIGINS` atau atur environment yang sesuai.
- Jika model lambat pada pemanggilan pertama, proses mungkin sedang mengunduh model (Hugging Face) atau inisialisasi panggilan remote — beri waktu lebih lama atau jalankan di mesin dengan koneksi bagus.
- Error koneksi database: verifikasi `DATABASE_URL` dan pastikan server Postgres dapat dijangkau.
- Untuk men-debug log backend, jalankan `python run.py` dan amati log yang tercetak oleh aplikasi.

---

## Catatan Pengembangan (lokasi file penting)

- Entri backend: `backend/run.py`, `backend/app/main.py` (lifespan dan inisialisasi startup)
- Route API: `backend/app/routes.py`
- Layanan integrasi AI: `backend/app/services/sentiment_service.py`` dan `backend/app/services/gemini_service.py`
- Entri frontend: `frontend/src/main.jsx` dan `frontend/index.html`
- Klien API frontend: `frontend/src/api/reviewApi.js` (atur `VITE_API_URL`)

---

## Kontribusi

Kontribusi sangat welcome. Buka issue atau PR. Sertakan langkah reproduksi dan tes bila memungkinkan.

---

## Lisensi

Proyek ini disediakan untuk tujuan edukasi.

---

Jika Anda mau, saya juga bisa:

- Menambahkan `vercel.json` dan README singkat untuk deploy frontend saja ke Vercel.
- Menambahkan `Procfile` atau `Dockerfile` untuk backend agar deployment ke Render/Heroku lebih mudah.
- Menambahkan contoh nilai `.env` ke `frontend/.env.example` dan `backend/.env.example` jika Anda mau.

Katakan mana yang Anda inginkan selanjutnya dan saya akan mengimplementasikannya.
# 🌟 Penganalisis Ulasan Produk

<div align="center">

![Product Review Analyzer](https://img.shields.io/badge/Product%20Review-Analyzer-00d4ff?style=for-the-badge&logo=sparkles)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql)

**Penganalisis ulasan produk berbasis AI dengan deteksi sentimen dan ekstraksi poin penting**

</div>

---

## ✨ Fitur

| Feature | Deskripsi | Teknologi |
|---------|-----------|-----------|
| 🎭 **Analisis Sentimen** | Menganalisis sentimen ulasan (positif/negatif/netral) | Hugging Face Transformers |
| 🔑 **Ekstraksi Poin Penting** | Mengambil insight penting dari ulasan | Google Gemini AI |
| 💾 **Penyimpanan** | Menyimpan hasil analisis | PostgreSQL + SQLAlchemy |
| 🎨 **Antarmuka Modern** | Desain Glassmorphism + Gradient | React + Styled Components |
| ⚡ **Pemrosesan Instan** | Analisis AI secara cepat | FastAPI |
| 📊 **Riwayat Analisis** | Melihat semua analisis sebelumnya | REST API |

---

## 🏗️ Arsitektur

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (React + Vite)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ ReviewForm  │  │AnalysisResult│  │   ReviewList       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │     POST /api/analyze-review    GET /api/reviews       ││
│  └─────────────────────────────────────────────────────────┘│
│                    │                    │                    │
│         ┌─────────┴─────────┐          │                    │
│         ▼                   ▼          ▼                    │
│  ┌─────────────┐    ┌─────────────┐  ┌─────────────┐       │
│  │ HuggingFace │    │   Gemini    │  │ PostgreSQL  │       │
│  │ Sentiment   │    │ Key Points  │  │  Database   │       │
│  └─────────────┘    └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Cara Menjalankan (Singkat)

### Prasyarat

- **Node.js** 18+ dan npm
- **Python** 3.10+
- **PostgreSQL** 15+
- **Kunci API**:
  - Google Gemini API Key ([Dapatkan di sini](https://makersuite.google.com/app/apikey))
  - (Opsional) Hugging Face API Key

### 1️⃣ Clone & Setup

```bash
# Clone repository
git clone <repository-url>
cd TUGAS3
```

### 2️⃣ Pengaturan Database

```bash
# Masuk ke PostgreSQL
psql -U postgres
# Buat database
CREATE DATABASE review_analyzer;
\q
```

### 3️⃣ Pengaturan Backend

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Konfigurasi environment variables
copy .env.example .env
# Edit .env dengan pengaturanmu:
# DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/review_analyzer
# GEMINI_API_KEY=your_gemini_api_key

# Jalankan server
python run.py
```

API akan tersedia di: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 4️⃣ Pengaturan Frontend

```bash
# Buka terminal baru dan masuk ke folder frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend akan tersedia di: `http://localhost:5173`

---

## 📡 Endpoint API

### POST `/api/analyze-review`
Menganalisis ulasan produk baru.

**Request Body:**
```json
{
  "review_text": "This product is amazing! Great quality and fast shipping.",
  "product_name": "Wireless Headphones"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Review analyzed successfully",
  "data": {
    "id": 1,
    "review_text": "This product is amazing! Great quality and fast shipping.",
    "product_name": "Wireless Headphones",
    "sentiment": "positive",
    "sentiment_score": 0.98,
    "key_points": [
      "Great overall satisfaction"
    ],
    "created_at": "2024-12-08T17:00:00Z",
    "analysis_status": "completed"
  }
}
```

### GET `/api/reviews`
Mengambil semua ulasan yang dianalisis dengan opsi filter.

**Query Parameters:**
- `skip` (int): Jumlah record yang dilewati (default: 0)
- `limit` (int): Jumlah record yang dikembalikan (default: 50, max: 100)
- `sentiment` (string): Filter berdasarkan sentimen (positive, negative, neutral)

**Response:**
```json
{
  "success": true,
  "total": 25,
  "reviews": [
    {
      "id": 1,
      "review_text": "...",
      "sentiment": "positive",
      "sentiment_score": 0.98,
      "key_points": ["..."],
      "created_at": "2024-12-08T17:00:00Z",
      "analysis_status": "completed"
    }
  ]
}
```

### GET `/api/reviews/{id}`
Mengambil ulasan tertentu berdasarkan ID.

### DELETE `/api/reviews/{id}`
Menghapus ulasan tertentu.

---

## 🎨 Sistem Desain

Aplikasi menggunakan desain modern **Glassmorphism + Gradient**:

### Palet Warna

| Color | HSL | Penggunaan |
|-------|-----|-----------|
| 🔵 Primary | `hsl(189, 92%, 58%)` | Accent, tombol, link |
| 🟢 Positive | `hsl(142, 76%, 46%)` | Sentimen positif |
| 🔴 Negative | `hsl(0, 72%, 51%)` | Sentimen negatif |
| 🟡 Neutral | `hsl(45, 93%, 55%)` | Sentimen netral |
| ⚫ Background | `hsl(240, 15%, 9%)` | Latar belakang gelap |

### Komponen

- **Card Component**: Efek glassmorphism dengan border animasi
- **Loader**: Animasi kubus 3D yang berputar
- **Toast**: Notifikasi slide-in
- **Form**: Input interaktif dengan validasi

---

## 📁 Struktur Proyek

```
TUGAS3/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Manajemen konfigurasi
│   │   ├── database.py        # Setup SQLAlchemy
│   │   ├── main.py            # Aplikasi FastAPI
│   │   ├── models.py          # Model database
│   │   ├── routes.py          # Endpoint API
│   │   ├── schemas.py         # Skema Pydantic
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── sentiment_service.py  # Integrasi HuggingFace
│   │       └── gemini_service.py     # Integrasi Gemini
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── reviewApi.js   # Klien API
│   │   ├── components/
│   │   │   ├── index.js
│   │   │   ├── Loader.jsx
│   │   │   ├── ReviewCard.jsx
│   │   │   ├── ReviewForm.jsx
│   │   │   ├── AnalysisResult.jsx
│   │   │   ├── ReviewList.jsx
│   │   │   └── Toast.jsx
│   │   ├── App.jsx
+
      "Great overall satisfaction"
    ],
    "created_at": "2024-12-08T17:00:00Z",
    "analysis_status": "completed"
  }
}
```

### GET `/api/reviews`
Get all analyzed reviews with optional filtering.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 50, max: 100)
- `sentiment` (string): Filter by sentiment (positive, negative, neutral)

**Response:**
```json
{
  "success": true,
  "total": 25,
  "reviews": [
    {
      "id": 1,
      "review_text": "...",
      "sentiment": "positive",
      "sentiment_score": 0.98,
      "key_points": ["..."],
      "created_at": "2024-12-08T17:00:00Z",
      "analysis_status": "completed"
    }
  ]
}
```

### GET `/api/reviews/{id}`
Get a specific review by ID.

### DELETE `/api/reviews/{id}`
Delete a specific review.

---

## 🎨 Design System

The application uses a modern **Glassmorphism + Gradient** design system:

### Color Palette

| Color | HSL | Usage |
|-------|-----|-------|
| 🔵 Primary | `hsl(189, 92%, 58%)` | Accent, buttons, links |
| 🟢 Positive | `hsl(142, 76%, 46%)` | Positive sentiment |
| 🔴 Negative | `hsl(0, 72%, 51%)` | Negative sentiment |
| 🟡 Neutral | `hsl(45, 93%, 55%)` | Neutral sentiment |
| ⚫ Background | `hsl(240, 15%, 9%)` | Dark background |

### Components

- **Card Component**: Glassmorphism effect with animated borders
- **Loader**: 3D rotating cube animation
- **Toast**: Slide-in notifications
- **Form**: Interactive input with validation

---

## 📁 Project Structure

```
TUGAS3/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── main.py            # FastAPI application
│   │   ├── models.py          # Database models
│   │   ├── routes.py          # API endpoints
│   │   ├── schemas.py         # Pydantic schemas
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── sentiment_service.py  # HuggingFace integration
│   │       └── gemini_service.py     # Gemini integration
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── reviewApi.js   # API client
│   │   ├── components/
│   │   │   ├── index.js
│   │   │   ├── Loader.jsx
│   │   │   ├── ReviewCard.jsx
│   │   │   ├── ReviewForm.jsx
│   │   │   ├── AnalysisResult.jsx
│   │   │   ├── ReviewList.jsx
│   │   │   └── Toast.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── index.html
│
└── README.md
```

---

## 🔧 Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Hugging Face (optional - uses local model by default)
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Server
HOST=0.0.0.0
PORT=8000
```

### Frontend Environment Variables

```env
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Testing

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Analyze a review
curl -X POST http://localhost:8000/api/analyze-review \
  -H "Content-Type: application/json" \
  -d '{"review_text": "This product is fantastic!", "product_name": "Test Product"}'

# Get all reviews
curl http://localhost:8000/api/reviews
```

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Styled Components** - CSS-in-JS
- **Lucide React** - Icon library
- **Axios** - HTTP client

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Hugging Face Transformers** - Sentiment analysis
- **Google Gemini** - Key points extraction
- **Pydantic** - Data validation

---

## 🤝 Error Handling

The application implements comprehensive error handling:

### Frontend
- Loading states during API calls
- Toast notifications for success/error
- API offline detection with retry button
- Form validation with error messages

### Backend
- Global exception handler
- Partial analysis fallback (if one AI service fails)
- Detailed error messages in responses
- Request validation with Pydantic

---

## 📈 Performance

- **Lazy Model Loading**: AI models are loaded on first request
- **Connection Pooling**: SQLAlchemy connection pool for database
- **Async Processing**: FastAPI async endpoints
- **Optimized Bundling**: Vite for fast frontend builds

---

## 📝 License

This project is created for educational purposes.

---

<div align="center">

**Made with ❤️ using React, FastAPI, Hugging Face & Gemini**

</div>
