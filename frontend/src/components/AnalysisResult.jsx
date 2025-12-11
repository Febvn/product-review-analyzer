/**
 * Analysis Result Component
 * Displays the detailed analysis result after processing
 */
import React from 'react';
import styled from 'styled-components';
import {
  ThumbsUp,
  ThumbsDown,
  Minus,
  Sparkles,
  Check,
  AlertTriangle,
  Copy,
  CheckCircle
} from 'lucide-react';
import { useState } from 'react';

const AnalysisResult = ({ result, onNewAnalysis }) => {
  // State untuk menangani status "Copied" pada tombol copy
  const [copied, setCopied] = useState(false);

  // Jika tidak ada hasil (null), jangan render apa-apa
  if (!result) return null;

  // Destructuring data dari prop `result` untuk memudahkan akses variabel
  const { data } = result;
  const {
    sentiment,          // Hasil sentimen: 'positive', 'negative', atau 'neutral'
    sentiment_score,    // Skor keyakinan (confidence score) dari model AI
    key_points,         // Array poin-poin penting yang diekstrak
    review_text,        // Teks review asli
    product_name,       // Nama produk (opsional)
    analysis_status,    // Status analisis
    error_message       // Pesan error jika ada
  } = data || {};

  /**
   * Konfigurasi tampilan berdasarkan sentimen.
   * Mengembalikan icon, warna, dan deskripsi yang sesuai
   * dengan hasil analisis sentimen.
   */
  const getSentimentConfig = () => {
    switch (sentiment) {
      case 'positive':
        return {
          icon: <ThumbsUp size={32} />,
          label: 'Positive',
          color: 'var(--positive)',
          bgColor: 'hsla(142, 76%, 46%, 0.15)',
          borderColor: 'hsla(142, 76%, 46%, 0.3)',
          description: 'This review expresses a positive sentiment about the product.'
        };
      case 'negative':
        return {
          icon: <ThumbsDown size={32} />,
          label: 'Negative',
          color: 'var(--negative)',
          bgColor: 'hsla(0, 72%, 51%, 0.15)',
          borderColor: 'hsla(0, 72%, 51%, 0.3)',
          description: 'This review expresses a negative sentiment about the product.'
        };
      default: // Neutral atau undefined
        return {
          icon: <Minus size={32} />,
          label: 'Neutral',
          color: 'var(--neutral)',
          bgColor: 'hsla(45, 93%, 55%, 0.15)',
          borderColor: 'hsla(45, 93%, 55%, 0.3)',
          description: 'This review expresses a neutral or mixed sentiment.'
        };
    }
  };

  const sentimentConfig = getSentimentConfig();

  /**
   * Fungsi untuk menyalin hasil analisis ke clipboard.
   * Memformat teks agar rapi saat dipaste.
   */
  const handleCopy = async () => {
    // Format teks yang akan disalin
    const textToCopy = `
Sentiment Analysis Result
=========================
Sentiment: ${sentimentConfig.label} (${((sentiment_score || 0) * 100).toFixed(0)}% confidence)

Key Points:
${(key_points || []).map((point, i) => `${i + 1}. ${point}`).join('\n')}

Original Review:
${review_text}
${product_name ? `\nProduct: ${product_name}` : ''}
    `.trim();

    try {
      // Menggunakan Clipboard API browser
      await navigator.clipboard.writeText(textToCopy);

      // Ubah status tombol menjadi "Copied!" selama 2 detik
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    // StyledWrapper menerima prop $sentiment untuk mengatur tema warna background
    <StyledWrapper $sentiment={sentiment}>
      <div className="result">
        {/* Elemen dekoratif border gradient */}
        <div className="result__border" />

        {/* Header Bagian Hasil Analisis */}
        <div className="result_header">
          <h2 className="result_title">
            <Sparkles size={20} />
            Analysis Complete
          </h2>
          <div className="header_actions">
            <button className="copy_button" onClick={handleCopy}>
              {copied ? <CheckCircle size={16} /> : <Copy size={16} />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
        </div>

        <hr className="line" />

        {/* Tampilan Error Jika Analisis Sebagian Gagal */}
        {error_message && (
          <div className="error_banner">
            <AlertTriangle size={18} />
            <div>
              <strong>Partial Analysis</strong>
              <p>{error_message}</p>
            </div>
          </div>
        )}

        {/* Kartu Sentimen Utama */}
        <div
          className="sentiment_card"
          style={{
            // Custom properties CSS (variables) untuk pewarnaan dinamis
            '--sentiment-color': sentimentConfig.color,
            '--sentiment-bg': sentimentConfig.bgColor,
            '--sentiment-border': sentimentConfig.borderColor
          }}
        >
          <div className="sentiment_icon">
            {sentimentConfig.icon}
          </div>
          <div className="sentiment_info">
            <h3 className="sentiment_label">{sentimentConfig.label}</h3>
            <p className="sentiment_description">{sentimentConfig.description}</p>
          </div>
          <div className="sentiment_score">
            {/* Menampilkan persentase skor keyakinan */}
            <span className="score_value">{((sentiment_score || 0) * 100).toFixed(0)}%</span>
            <span className="score_label">Confidence</span>
          </div>
        </div>

        {/* Bagian Poin Penting (Hanya tampil jika ada key_points) */}
        {key_points && key_points.length > 0 && (
          <div className="key_points_section">
            <h3 className="section_title">
              <Sparkles size={16} />
              Key Points Extracted
            </h3>
            <ul className="key_points_list">
              {key_points.map((point, index) => (
                <li key={index} className="key_point_item">
                  <span className="point_number">{index + 1}</span>
                  <span className="point_text">{point}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Menampilkan Review Asli */}
        <div className="original_review">
          <h4 className="review_label">Original Review</h4>
          {product_name && (
            <span className="product_tag">{product_name}</span>
          )}
          <p className="review_text">{review_text}</p>
        </div>

        {/* Tombol Aksi Bawah */}
        <div className="action_buttons">
          <button className="button_primary" onClick={onNewAnalysis}>
            <Sparkles size={16} />
            Analyze Another Review
          </button>
        </div>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  width: 100%;
  max-width: 600px;
  animation: slideUp 0.5s ease forwards;

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .result {
    --white: hsl(0, 0%, 100%);
    --black: hsl(240, 15%, 9%);
    --paragraph: hsl(0, 0%, 83%);
    --line: hsl(240, 9%, 17%);
    --primary: hsl(189, 92%, 58%);
    --positive: hsl(142, 76%, 46%);
    --negative: hsl(0, 72%, 51%);
    --neutral: hsl(45, 93%, 55%);

    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    padding: 1.5rem;
    
    background-color: hsla(240, 15%, 9%, 1);
    background-image: 
      radial-gradient(at 88% 40%, hsla(240, 15%, 9%, 1) 0px, transparent 85%),
      radial-gradient(at 49% 30%, hsla(240, 15%, 9%, 1) 0px, transparent 85%),
      radial-gradient(at 14% 26%, hsla(240, 15%, 9%, 1) 0px, transparent 85%),
      radial-gradient(at 0% 64%, ${props =>
    props.$sentiment === 'positive' ? 'hsl(142, 70%, 26%)' :
      props.$sentiment === 'negative' ? 'hsl(0, 70%, 26%)' :
        'hsl(189, 99%, 26%)'
  } 0px, transparent 85%),
      radial-gradient(at 41% 94%, ${props =>
    props.$sentiment === 'positive' ? 'hsl(142, 70%, 36%)' :
      props.$sentiment === 'negative' ? 'hsl(0, 70%, 36%)' :
        'hsl(189, 97%, 36%)'
  } 0px, transparent 85%),
      radial-gradient(at 100% 99%, ${props =>
    props.$sentiment === 'positive' ? 'hsl(142, 70%, 13%)' :
      props.$sentiment === 'negative' ? 'hsl(0, 70%, 13%)' :
        'hsl(188, 94%, 13%)'
  } 0px, transparent 85%);

    border-radius: 1rem;
    box-shadow: 0px -16px 24px 0px rgba(255, 255, 255, 0.25) inset;
  }

  .result__border {
    overflow: hidden;
    pointer-events: none;
    position: absolute;
    z-index: -10;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: calc(100% + 2px);
    height: calc(100% + 2px);
    background-image: linear-gradient(
      0deg,
      hsl(0, 0%, 100%) -50%,
      hsl(0, 0%, 40%) 100%
    );
    border-radius: 1rem;
  }

  .result__border::before {
    content: "";
    pointer-events: none;
    position: fixed;
    z-index: 200;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(0deg);
    transform-origin: left;
    width: 200%;
    height: 10rem;
    background-image: linear-gradient(
      0deg,
      hsla(0, 0%, 100%, 0) 0%,
      ${props =>
    props.$sentiment === 'positive' ? 'hsl(142, 100%, 50%)' :
      props.$sentiment === 'negative' ? 'hsl(0, 100%, 50%)' :
        'hsl(189, 100%, 50%)'
  } 40%,
      ${props =>
    props.$sentiment === 'positive' ? 'hsl(142, 100%, 50%)' :
      props.$sentiment === 'negative' ? 'hsl(0, 100%, 50%)' :
        'hsl(189, 100%, 50%)'
  } 60%,
      hsla(0, 0%, 40%, 0) 100%
    );
    animation: rotate 8s linear infinite;
  }

  @keyframes rotate {
    to {
      transform: rotate(360deg);
    }
  }

  .result_header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .result_title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--primary);
  }

  .header_actions {
    display: flex;
    gap: 0.5rem;
  }

  .copy_button {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.75rem;
    background: hsla(240, 15%, 20%, 0.5);
    border: 1px solid var(--line);
    border-radius: 0.5rem;
    color: var(--paragraph);
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .copy_button:hover {
    background: hsla(240, 15%, 25%, 0.5);
    color: var(--white);
  }

  .line {
    width: 100%;
    height: 1px;
    background-color: var(--line);
    border: none;
  }

  .error_banner {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem;
    background: hsla(45, 93%, 55%, 0.1);
    border: 1px solid hsla(45, 93%, 55%, 0.3);
    border-radius: 0.5rem;
    color: var(--neutral);
  }

  .error_banner strong {
    display: block;
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
  }

  .error_banner p {
    font-size: 0.75rem;
    color: var(--paragraph);
    margin: 0;
  }

  .sentiment_card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem;
    background: var(--sentiment-bg);
    border: 1px solid var(--sentiment-border);
    border-radius: 0.75rem;
  }

  .sentiment_icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3.5rem;
    height: 3.5rem;
    background: var(--sentiment-bg);
    border: 2px solid var(--sentiment-border);
    border-radius: 50%;
    color: var(--sentiment-color);
    flex-shrink: 0;
  }

  .sentiment_info {
    flex: 1;
  }

  .sentiment_label {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--sentiment-color);
    margin-bottom: 0.25rem;
  }

  .sentiment_description {
    font-size: 0.8rem;
    color: var(--paragraph);
    margin: 0;
    line-height: 1.4;
  }

  .sentiment_score {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5rem 0.75rem;
    background: hsla(0, 0%, 0%, 0.2);
    border-radius: 0.5rem;
  }

  .score_value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--sentiment-color);
  }

  .score_label {
    font-size: 0.65rem;
    color: var(--paragraph);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .key_points_section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .section_title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    color: var(--white);
  }

  .key_points_list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    list-style: none;
  }

  .key_point_item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem;
    background: hsla(240, 15%, 15%, 0.5);
    border-radius: 0.5rem;
    transition: background 0.3s ease;
  }

  .key_point_item:hover {
    background: hsla(240, 15%, 18%, 0.5);
  }

  .point_number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
    background: var(--primary);
    border-radius: 50%;
    color: var(--black);
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
  }

  .point_text {
    font-size: 0.85rem;
    color: var(--white);
    line-height: 1.5;
  }

  .original_review {
    padding: 1rem;
    background: hsla(240, 15%, 12%, 0.5);
    border-radius: 0.5rem;
    border: 1px solid var(--line);
  }

  .review_label {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--paragraph);
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .product_tag {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background: hsla(189, 92%, 58%, 0.15);
    border-radius: 9999px;
    font-size: 0.7rem;
    color: var(--primary);
    margin-bottom: 0.5rem;
  }

  .review_text {
    font-size: 0.85rem;
    color: var(--paragraph);
    line-height: 1.6;
    margin: 0;
    max-height: 150px;
    overflow-y: auto;
  }

  .action_buttons {
    display: flex;
    justify-content: center;
    margin-top: 0.5rem;
  }

  .button_primary {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background-image: linear-gradient(
      0deg,
      hsl(189, 92%, 58%),
      hsl(189, 99%, 26%) 100%
    );
    color: var(--white);
    border: none;
    border-radius: 9999px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: inset 0 -2px 25px -4px var(--white);
  }

  .button_primary:hover {
    transform: translateY(-2px);
    box-shadow: inset 0 -2px 25px -4px var(--white),
                0 5px 20px hsla(189, 92%, 58%, 0.3);
  }

  @media (max-width: 480px) {
    .result {
      padding: 1.25rem;
    }

    .sentiment_card {
      flex-wrap: wrap;
    }

    .sentiment_score {
      width: 100%;
      flex-direction: row;
      justify-content: center;
      gap: 0.5rem;
    }
  }
`;

export default AnalysisResult;
