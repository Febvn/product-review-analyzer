"""
Service Ekstraksi Poin Penting menggunakan Google Gemini AI
File ini bertanggung jawab untuk mengekstrak poin-poin kunci dari review panjang.
Jika API Gemini tidak tersedia, akan menggunakan fallback method berbasis NLP sederhana.
"""
import logging
import re
import google.generativeai as genai
from typing import List, Optional
from app.config import settings

# Setup logger untuk tracking dan debugging
logger = logging.getLogger(__name__)


class KeyPointsExtractor:
    """
    Kelas untuk Ekstraksi Poin Penting menggunakan Google Gemini AI.
    
    Fitur:
    - Menggunakan Gemini Pro untuk ekstraksi cerdas (jika API key tersedia)
    - Fallback otomatis ke metode NLP sederhana jika API gagal
    - Mendukung bahasa Indonesia dan Inggris
    """
    
    def __init__(self):
        """
        Inisialisasi ekstraksi poin penting dengan Gemini API key.
        API key diambil dari environment variable melalui settings.
        """
        self.api_key = settings.GEMINI_API_KEY
        self.use_ai = False  # Flag untuk menandakan apakah AI tersedia
        
        # Cek apakah API key valid (tidak dimulai dengan placeholder "your_")
        if self.api_key and not self.api_key.startswith("your_"):
            try:
                # Konfigurasi Gemini API dengan API key
                genai.configure(api_key=self.api_key)
                # Inisialisasi model Gemini Pro (model gratis untuk text generation)
                self.model = genai.GenerativeModel('gemini-pro')
                self.use_ai = True
                logger.info("Gemini AI berhasil diinisialisasi untuk ekstraksi poin penting")
            except Exception as e:
                logger.error(f"Gagal menginisialisasi Gemini AI: {str(e)}")
                self.use_ai = False
        else:
            logger.warning("API Key Gemini tidak ditemukan atau tidak valid. Menggunakan mode fallback ringan.")
            self.use_ai = False
        
    def extract_key_points(self, review_text: str, product_name: Optional[str] = None) -> List[str]:
        """
        Ekstrak poin-poin kunci dari review produk.
        
        Args:
            review_text: Teks review yang akan dianalisis
            product_name: (Optional) Nama produk untuk konteks tambahan
            
        Returns:
            List berisi 3-5 poin penting dari review
            
        Contoh:
            >>> points = extract_key_points("Laptop ini sangat cepat dan layarnya jernih...")
            >>> print(points)
            ['Performa sangat cepat', 'Kualitas layar jernih', 'Harga terjangkau']
        """
        # Validasi: Pastikan teks tidak kosong
        if not review_text or not review_text.strip():
            raise ValueError("Teks review tidak boleh kosong")
        
        # Prioritas 1: Coba gunakan AI terlebih dahulu
        if self.use_ai:
            try:
                return self._extract_with_gemini(review_text, product_name)
            except Exception as e:
                logger.error(f"Ekstraksi Gemini gagal: {str(e)}. Beralih ke metode lokal.")
                # Jika AI gagal, lanjutkan ke fallback method di bawah
        
        # Prioritas 2: Gunakan metode fallback (NLP sederhana)
        return self._extract_fallback(review_text, product_name)

    def _extract_with_gemini(self, text: str, product_name: str = None) -> List[str]:
        """
        Ekstrak poin penting menggunakan Gemini API (AI-powered).
        
        Args:
            text: Teks review
            product_name: Nama produk (opsional untuk konteks)
            
        Returns:
            List poin-poin penting yang dihasilkan AI
        """
        # Tambahkan konteks nama produk jika tersedia
        product_context = f" untuk '{product_name}'" if product_name else ""
        
        # Prompt engineering: Instruksi yang jelas untuk AI
        prompt = f"""
        Analisis review produk berikut{product_context} dan ekstrak 3-5 poin penting dalam bentuk bullet.
        Fokus pada fitur produk, kualitas, dan sentimen pengguna.
        Kembalikan HANYA poin-poin dalam bentuk list, satu per baris, tanpa asterisk atau numbering.
        Jika review tidak jelas atau tidak bermakna, kembalikan "No clear key points found".
        
        Review: "{text}"
        """
        
        # Kirim prompt ke Gemini dan dapatkan respons
        response = self.model.generate_content(prompt)
        content = response.text.strip()
        
        # Proses respons AI menjadi list
        # Hilangkan simbol markdown seperti *, -, atau #
        points = [
            line.strip().replace('*', '').replace('-', '').strip() 
            for line in content.split('\n') 
            if line.strip()
        ]
        
        # Filter: Buang poin kosong dan hasil "No clear key points"
        points = [p for p in points if len(p) > 3 and "No clear key points" not in p]
        
        # Jika tidak ada poin yang valid, kembalikan placeholder
        if not points:
            return ["No clear key points found"]
            
        # Batasi maksimal 5 poin
        return points[:5]
    
    def _extract_fallback(self, text: str, product_name: Optional[str] = None) -> List[str]:
        """
        Ekstrak poin penting menggunakan metode NLP sederhana (Fallback).
        
        Metode ini bekerja dengan:
        1. Memecah teks menjadi kalimat-kalimat
        2. Memberi skor kalimat berdasarkan keyword penting
        3. Mengambil kalimat dengan skor tertinggi
        
        Args:
            text: Teks review
            product_name: Nama produk (opsional)
            
        Returns:
            List poin-poin penting hasil ekstraksi manual
        """
        # Bersihkan teks dari spasi berlebih
        text = text.strip()
        
        # Pecah teks menjadi kalimat berdasarkan tanda baca
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
        
        # Handle kasus review sangat pendek (1 kalimat)
        if len(sentences) == 1 and len(sentences[0]) < 100:
             return [sentences[0]]

        key_points = []
        
        # ========================================
        # KEYWORD DICTIONARIES untuk Scoring
        # ========================================
        
        # Keyword positif (Indonesia & Inggris)
        positive_keywords = [
            'great', 'excellent', 'amazing', 'love', 'best', 'good', 'nice', 
            'recommend', 'happy', 'perfect', 'fantastic', 'awesome', 'wonderful',
            'satisfied', 'worth', 'quality', 'fast', 'quick', 'easy',
            # Indonesian
            'bagus', 'mantap', 'suka', 'puas', 'keren', 'recommended', 'banget',
            'cepat', 'mudah', 'worth it', 'oke', 'ok', 'top', 'jos', 'mantul'
        ]
        
        # Keyword negatif (Indonesia & Inggris)
        negative_keywords = [
            'bad', 'poor', 'terrible', 'hate', 'worst', 'disappointed', 
            'broken', 'slow', 'expensive', 'waste', 'horrible', 'awful',
            'regret', 'useless', 'cheap', 'fake', 'defective', 'damaged',
            # Indonesian
            'jelek', 'kecewa', 'rusak', 'mahal', 'lambat', 'bohong', 'palsu',
            'tidak bagus', 'buruk', 'parah', 'zonk', 'nyesel', 'kapok', 'gak'
        ]
        
        # Keyword fitur produk (Indonesia & Inggris)
        feature_keywords = [
            'battery', 'screen', 'camera', 'design', 'quality', 'price', 
            'delivery', 'shipping', 'fast', 'size', 'color', 'package',
            'packaging', 'performance', 'speed', 'material', 'build',
            # Indonesian
            'baterai', 'layar', 'kamera', 'desain', 'kualitas', 'harga',
            'pengiriman', 'ongkir', 'ukuran', 'warna', 'kemasan', 'packing',
            'bahan', 'model', 'fitur'
        ]
        
        # ========================================
        # SCORING ALGORITHM
        # ========================================
        scored_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = 0
            
            # Tambah skor jika mengandung keyword sentimen (positif/negatif)
            for kw in positive_keywords + negative_keywords:
                if kw in sentence_lower:
                    score += 2  # Keyword sentimen lebih penting
            
            # Tambah skor jika mengandung keyword fitur produk
            for kw in feature_keywords:
                if kw in sentence_lower:
                    score += 1
            
            # Bonus skor jika menyebut nama produk
            if product_name and product_name.lower() in sentence_lower:
                score += 1
            
            # Penalti untuk kalimat terlalu pendek (kecuali skornya tinggi)
            if len(sentence) < 20: 
                score -= 1
            
            scored_sentences.append((sentence, score))
        
        # Urutkan kalimat berdasarkan skor (tertinggi dulu)
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Ambil kalimat dengan skor tertinggi
        for sentence, score in scored_sentences:
            # Hanya ambil kalimat dengan skor positif dan tidak terlalu panjang
            if score > 0 and len(sentence) < 300:
                # Kapitalisasi huruf pertama agar terlihat rapi
                point = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence
                # Hindari duplikasi
                if point not in key_points:
                    key_points.append(point)
                # Batasi maksimal 5 poin
                if len(key_points) >= 5:
                    break
        
        # Jika tidak ada keyword yang cocok tapi ada kalimat, ambil kalimat terpanjang
        # Asumsi: Kalimat panjang biasanya mengandung informasi lebih banyak
        if not key_points and sentences:
             # Urutkan berdasarkan panjang
            sentences_by_len = sorted(sentences, key=len, reverse=True)
            for sentence in sentences_by_len[:3]:  # Ambil 3 terpanjang
                 if len(sentence) < 300:
                    point = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence
                    key_points.append(point)

        # Fallback final: Jika masih kosong, kembalikan pesan default
        if not key_points:
            key_points = ["Review text analysis completed"]
        
        logger.info(f"Berhasil mengekstrak {len(key_points)} poin penting (Mode Fallback)")
        return key_points


# ============================================
# Singleton Pattern untuk efisiensi memory
# ============================================
# Instance global yang di-share oleh semua request
_extractor: Optional[KeyPointsExtractor] = None


def get_key_points_extractor() -> KeyPointsExtractor:
    """
    Mendapatkan atau membuat instance KeyPointsExtractor (Singleton).
    Fungsi ini memastikan hanya ada satu instance extractor di memory.
    """
    global _extractor
    if _extractor is None:
        _extractor = KeyPointsExtractor()
    return _extractor


def extract_key_points(review_text: str, product_name: Optional[str] = None) -> List[str]:
    """
    Fungsi helper untuk mengekstrak poin penting.
    Ini adalah shortcut agar kode lebih mudah dibaca.
    
    Args:
        review_text: Teks review yang akan dianalisis
        product_name: (Optional) Nama produk
        
    Returns:
        List poin-poin penting
        
    Contoh:
        >>> points = extract_key_points("Produk bagus, pengiriman cepat", "Laptop X")
        >>> print(points)
        ['Produk bagus', 'pengiriman cepat']
    """
    extractor = get_key_points_extractor()
    return extractor.extract_key_points(review_text, product_name)

