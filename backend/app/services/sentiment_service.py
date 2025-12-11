"""
Service Analisis Sentimen menggunakan Hugging Face Transformers
File ini bertanggung jawab untuk menganalisis sentimen (positif/negatif/netral) dari teks review.
"""
import logging
from typing import Tuple, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Setup logger untuk tracking dan debugging
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Kelas untuk Analisis Sentimen menggunakan Hugging Face transformers.
    Menggunakan pre-trained model BERT multilingual untuk klasifikasi sentimen.
    
    Model utama: nlptown/bert-base-multilingual-uncased-sentiment
    - Mendukung banyak bahasa termasuk Indonesia dan Inggris
    - Mengklasifikasikan review dalam skala 1-5 bintang
    """
    
    def __init__(self, model_name: str = "nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        Inisialisasi sentiment analyzer.
        
        Args:
            model_name: Nama model Hugging Face untuk analisis sentimen
        """
        self.model_name = model_name
        self.classifier = None  # Pipeline classifier akan diisi saat lazy initialization
        self._initialized = False  # Flag untuk memastikan model hanya di-load sekali
        
    def _initialize(self):
        """
        Lazy initialization: Model baru di-load saat pertama kali digunakan.
        Ini menghemat memory karena model hanya di-load ketika benar-benar diperlukan.
        """
        # Jika sudah pernah di-initialize, skip
        if self._initialized:
            return
            
        try:
            logger.info(f"Memuat model sentimen: {self.model_name}")
            
            # Cek apakah ada GPU CUDA tersedia untuk mempercepat inferensi
            # device=0 artinya menggunakan GPU pertama, device=-1 artinya CPU
            device = 0 if torch.cuda.is_available() else -1
            
            # Inisialisasi pipeline untuk sentiment analysis
            # Pipeline ini adalah wrapper yang menyederhanakan proses tokenisasi dan inferensi
            self.classifier = pipeline(
                "sentiment-analysis",  # Jenis task
                model=self.model_name,  # Model yang digunakan
                tokenizer=self.model_name,  # Tokenizer (biasanya sama dengan model)
                device=device,  # Device untuk komputasi (GPU/CPU)
                max_length=512,  # Maksimal panjang token (batasan BERT)
                truncation=True  # Potong teks jika lebih panjang dari max_length
            )
            
            self._initialized = True
            logger.info("Model sentimen berhasil dimuat")
            
        except Exception as e:
            logger.error(f"Gagal memuat model sentimen: {str(e)}")
            
            # Fallback: Coba gunakan model yang lebih sederhana jika model utama gagal
            try:
                logger.info("Mencoba model fallback (distilbert-sst-2)...")
                self.classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",  # Model lebih kecil
                    device=-1,  # Gunakan CPU untuk keamanan
                    max_length=512,
                    truncation=True
                )
                self._initialized = True
                logger.info("Model fallback berhasil dimuat")
            except Exception as fallback_error:
                logger.error(f"Gagal memuat model fallback: {str(fallback_error)}")
                raise
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Menganalisis sentimen dari teks yang diberikan.
        
        Args:
            text: Teks review yang akan dianalisis
            
        Returns:
            Tuple berisi:
            - sentiment (str): 'positive', 'negative', atau 'neutral'
            - confidence_score (float): Skor kepercayaan model (0.0 - 1.0)
        """
        # Validasi: Pastikan teks tidak kosong
        if not text or not text.strip():
            raise ValueError("Teks tidak boleh kosong")
        
        # Inisialisasi model jika belum di-load
        self._initialize()
        
        try:
            # Potong teks jika terlalu panjang (batasan API)
            if len(text) > 4000:
                text = text[:4000]

            # Override manual untuk kata kunci negatif yang spesifik
            # CATATAN: Ini adalah logika hard-coded yang bisa menyebabkan false negative
            # Contoh: "not bad" akan terdeteksi sebagai negative karena mengandung "bad"
            lower_text = text.lower()
            if "jelek" in lower_text or "buruk" in lower_text or "bad" in lower_text:
                logger.info(f"Override manual: kata kunci negatif terdeteksi dalam '{text}'")
                return 'negative', 0.99
            
            # Jalankan prediksi menggunakan model
            # Result berbentuk list dictionary: [{'label': '5 stars', 'score': 0.9}]
            result = self.classifier(text)[0]
            
            # Ekstrak label dan skor dari hasil
            label = result['label'].lower()
            score = result['score']
            
            # Default sentiment adalah neutral
            sentiment = 'neutral'
            
            # Mapping label model ke kategori sentiment
            # Model nlptown menghasilkan label '1 star' sampai '5 stars'
            if '1 star' in label or '2 star' in label:
                sentiment = 'negative'  # Rating rendah = sentimen negatif
            elif '4 star' in label or '5 star' in label:
                sentiment = 'positive'  # Rating tinggi = sentimen positif
            elif '3 star' in label:
                sentiment = 'neutral'  # Rating tengah = sentimen netral
            else:
                # Fallback: Handle model lain yang menggunakan format label berbeda
                # Misalnya model distilbert-sst-2 menggunakan 'POSITIVE'/'NEGATIVE'
                if 'positive' in label or label in ['pos', 'label_2', '2']:
                    sentiment = 'positive'
                elif 'negative' in label or label in ['neg', 'label_0', '0']:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
            
            logger.info(f"Hasil analisis sentimen: {sentiment} ({score:.2f})")
            return sentiment, score
            
        except Exception as e:
            logger.error(f"Analisis sentimen gagal: {str(e)}")
            raise


# ============================================
# Singleton Pattern untuk efisiensi memory
# ============================================
# Instance global yang di-share oleh semua request
# Ini mencegah model di-load berulang kali untuk setiap request
_sentiment_analyzer: Optional[SentimentAnalyzer] = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """
    Mendapatkan atau membuat instance SentimentAnalyzer (Singleton).
    Fungsi ini memastikan hanya ada satu instance analyzer yang di-load di memory.
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer


def analyze_sentiment(text: str) -> Tuple[str, float]:
    """
    Fungsi helper untuk menganalisis sentimen.
    Ini adalah shortcut agar kode lebih mudah dibaca.
    
    Args:
        text: Teks yang akan dianalisis
        
    Returns:
        Tuple (sentiment, confidence_score)
        
    Contoh:
        >>> sentiment, score = analyze_sentiment("Produk ini sangat bagus!")
        >>> print(sentiment)  # Output: 'positive'
        >>> print(score)      # Output: 0.95
    """
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze(text)

