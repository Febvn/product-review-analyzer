# Panduan Mengaktifkan PostgreSQL


1.  **Download & Install PostgreSQL**
    - Unduh installer dari: https://www.postgresql.org/download/windows/
    - Install dan ingat password yang Anda set untuk user `postgres` (biasanya `postgres` atau `admin`).

2.  **Ubah Konfigurasi**
    - Buka file `backend/.env`.
    - Ubah baris `DATABASE_URL` menjadi:
      ```
      DATABASE_URL=postgresql://postgres:password_anda@localhost:5432/review_analyzer
      ```
      *(Ganti `password_anda` dengan password yang Anda buat saat install)*.

3.  **Restart Backend**
    - Matikan terminal backend (Ctrl+C).
    - Jalankan ulang: `python run.py`.
    - Backend akan otomatis membuat database `review_analyzer` (jika Anda menjalankan script `create_db.py` dahulu atau manual create) dan tabel-tabelnya.

Script helper `backend/create_db.py` sudah saya siapkan untuk membantu membuat database jika belum ada.
Run: `python backend/create_db.py` setelah install Postgres.
