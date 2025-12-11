# Panduan Deployment ke Vercel

Proyek ini telah dikonfigurasi untuk dapat di-deploy ke Vercel (Frontend + Backend).

## Langkah-langkah Deployment

1.  **Push ke GitHub**
    Pastikan semua perubahan kode sudah di-commit dan di-push ke repository GitHub Anda.

2.  **Import Proyek di Vercel**
    - Buka dashboard Vercel -> "Add New..." -> "Project".
    - Pilih repository GitHub Anda.
    - Vercel akan mendeteksi konfigurasi `vercel.json`.

3.  **Konfigurasi Environment Variables**
    Di halaman konfigurasi "Import Project" (atau di Settings setelah deploy), tambahkan Environment Variables berikut:

    **Backend:**
    - `DATABASE_URL`: Connection string PostgreSQL Anda.
      - Contoh: `postgres://user:password@host:port/database`
      - Anda bisa menggunakan provider seperti **Vercel Postgres**, **Neon**, **Supabase**, atau **ElephantSQL**.
      - Jika menggunakan **Vercel Postgres**, Vercel akan otomatis mengisi `POSTGRES_URL` dsb, pastikan kode Anda membaca variabel yang benar atau buat alias `DATABASE_URL`.
    - `GEMINI_API_KEY`: API Key untuk Google Gemini.
    - `HUGGINGFACE_API_KEY`: API Key wuntuk Hugging Face (Opsional).

    **Frontend:**
    - `VITE_API_URL`: Set value ke `/` (hanya karakter slash).
      - Ini penting agar frontend menghubungi backend di domain yang sama (via rewrite rule).

4.  **Deploy**
    Klik "Deploy". Vercel akan:
    - Menginstall dependencies Python.
    - Membuild frontend Vite.
    - Men-deploy Serverless Function untuk backend.

## Catatan Penting
- **Database**: Backend dikonfigurasi untuk menggunakan PostgreSQL jika `DATABASE_URL` tidak diawali dengan `sqlite`. Fitur `init_db` akan otomatis membuat tabel saat aplikasi berjalan pertama kali.
- **Cold Starts**: Karena menggunakan Serverless Function (Python), request pertama mungkin sedikit lambat (Cold Start).
