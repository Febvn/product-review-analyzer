
import sys
import os
sys.path.append(os.getcwd())

from app.services.sentiment_service import SentimentAnalyzer

def test_neutral_indo_variations():
    analyzer = SentimentAnalyzer()
    
    variations = [
        # Variation 1: Balanced / Standard
        "Produk ini biasa saja secara keseluruhan. Kualitasnya standar dan fungsinya berjalan normal, tidak ada yang istimewa. Harganya cukup masuk akal untuk barang seperti ini, meskipun performanya hanya rata-rata saja. Saya tidak terlalu kecewa tapi juga tidak terlalu terkesan, jadi menurut saya ini pembelian yang lumayan saja.",
        
        # Variation 2: More coloquial "meh"
        "Barang sudah sampai. Kondisinya biasa saja tidak ada yang spesial. Dipakai juga standar saja rasanya. Dibilang bagus banget juga enggak, dibilang rusak juga enggak. Ya pokoknya rata-rata lah buat harga segitu. Lumayan aja.",
        
        # Variation 3: Short logical
        "Kualitas produk standar. Pengiriman lumayan. Tidak ada masalah berarti tapi juga bukan produk premium.",
        
        # Variation 4: Explicit mixed
        "Ada kelebihannya tapi ada kekurangannya juga. Barangnya oke tapi pengirimannya agak lama. Kualitas bahannya biasa aja, sesuai harga."
    ]

    print("Testing Indonesian Variations for Neutrality...")
    
    for i, text in enumerate(variations):
        try:
            sentiment, score = analyzer.analyze(text)
            print(f"\n[Variation {i+1}]\nText: {text}\nResult: {sentiment} (Score: {score:.4f})")
        except Exception as e:
            print(f"Error testing Var {i+1}: {e}")

if __name__ == "__main__":
    test_neutral_indo_variations()
