
import sys
import os
sys.path.append(os.getcwd())

from app.services.sentiment_service import SentimentAnalyzer

def test_neutral_paragraph():
    analyzer = SentimentAnalyzer()
    
    # Candidate 1: Indonesian
    text_indo = (
        "Secara keseluruhan produk ini biasa saja. Kualitasnya standar dan berfungsi sebagaimana mestinya, "
        "meskipun tidak ada fitur yang benar-benar istimewa. Pengirimannya tepat waktu dan kemasannya cukup rapi. "
        "Untuk harga segini, barangnya lumayan dan performanya rata-rata saja, jadi saya rasa cukup adil untuk penggunaan sehari-hari."
    )
    
    # Candidate 2: English
    text_eng = (
        "The product is average in terms of quality. It works as expected but lacks any standout features "
        "that would make it exceptional. The shipping was on time and the packaging was decent. "
        "For the price point, it is an okay purchase mostly for daily use, providing acceptable performance without being amazing."
    )

    # Candidate 3: Mixed/Short (Control)
    text_short = "Barang sampai dengan aman. Kualitas standar aja."

    print("Testing Paragraphs for Neutrality...")
    
    try:
        sentiment, score = analyzer.analyze(text_indo)
        print(f"\n[Indonesian Paragraph]\nText: {text_indo}\nResult: {sentiment} (Score: {score:.4f})")
    except Exception as e:
        print(f"Error testing Indo: {e}")

    try:
        sentiment, score = analyzer.analyze(text_eng)
        print(f"\n[English Paragraph]\nText: {text_eng}\nResult: {sentiment} (Score: {score:.4f})")
    except Exception as e:
        print(f"Error testing Eng: {e}")

if __name__ == "__main__":
    test_neutral_paragraph()
