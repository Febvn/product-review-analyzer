/**
 * Review Card Component
 * Displays individual review analysis results
 */
import React from 'react';
import styled from 'styled-components';
import {
  Check,
  ThumbsUp,
  ThumbsDown,
  Minus,
  Calendar,
  Package,
  Sparkles,
  AlertCircle,
  X,
  Copy,
  Edit2
} from 'lucide-react';

const ReviewCard = ({ review, onDelete, onEdit }) => {
  // Destructuring properties dari objek review
  const {
    id,
    review_text,
    product_name,
    sentiment,
    sentiment_score,
    key_points,
    created_at,
    analysis_status,
    error_message
  } = review;

  /**
   * Handler untuk menyalin teks review.
   * Menggunakan e.stopPropagation() untuk mencegah event bubbling
   * (agar tidak memicu onClick pada parent element jika ada).
   */
  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(review_text);
    // Tampilkan alert sederhana (bisa diganti Toast di implementasi real)
    alert("Review text copied!");
  };

  /**
   * Helper untuk mendapatkan icon yang sesuai dengan sentimen.
   */
  const getSentimentIcon = () => {
    switch (sentiment) {
      case 'positive':
        return <ThumbsUp size={16} />;
      case 'negative':
        return <ThumbsDown size={16} />;
      default:
        return <Minus size={16} />;
    }
  };

  /**
   * Helper untuk label teks sentimen.
   */
  const getSentimentLabel = () => {
    switch (sentiment) {
      case 'positive':
        return 'Positive';
      case 'negative':
        return 'Negative';
      default:
        return 'Neutral';
    }
  };

  /**
   * Helper formatting tanggal agar mudah dibaca.
   * Format: Dec 8, 2024, 05:00 PM
   */
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  /**
   * Memotong teks jika terlalu panjang agar card tidak terlalu tinggi.
   */
  const truncateText = (text, maxLength = 200) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    // StyledWrapper menerima prop sentimen untuk border gradient yang sesuai
    <StyledWrapper $sentiment={sentiment}>
      <div className="card">
        {/* Dekorasi Border */}
        <div className="card__border" />

        {/* Tombol Delete (Pojok Kanan Atas) */}
        <button
          className="delete_button_top"
          onClick={(e) => {
            e.stopPropagation(); // Mencegah klik tembus ke card
            // Konfirmasi sebelum menghapus
            if (window.confirm('Are you sure you want to delete this review?')) {
              onDelete(id);
            }
          }}
          title="Delete Review"
        >
          <X size={16} />
        </button>

        {/* Header: Judul (ID Review) dan Badge Produk */}
        <div className="card_title__container">
          <div className="card_header">
            <span className="card_title">Review #{id}</span>
            {product_name && (
              <span className="product_badge">
                <Package size={12} />
                {product_name}
              </span>
            )}
          </div>
          {/* Teks review yang dipotong */}
          <p className="card_paragraph">{truncateText(review_text)}</p>
        </div>

        <hr className="line" />

        {/* Badge Sentimen (Warna sesuai hasil analisis) */}
        {sentiment && (
          <div className="sentiment_section">
            <span className={`sentiment_badge sentiment_${sentiment}`}>
              {getSentimentIcon()}
              <span>{getSentimentLabel()}</span>
              {sentiment_score && (
                <span className="score">({(sentiment_score * 100).toFixed(0)}%)</span>
              )}
            </span>
          </div>
        )}

        {/* Bagian Key Points (Maksimal 5 poin ditampilkan) */}
        {key_points && key_points.length > 0 && (
          <>
            <div className="key_points_header">
              <Sparkles size={14} />
              <span>Key Points</span>
            </div>
            <ul className="card__list">
              {key_points.slice(0, 5).map((point, index) => (
                <li key={index} className="card__list_item">
                  <span className="check">
                    <Check className="check_svg" size={12} />
                  </span>
                  <span className="list_text">{point}</span>
                </li>
              ))}
            </ul>
          </>
        )}

        {/* Tampilan Pesan Error (jika ada) */}
        {error_message && (
          <div className="error_message">
            <AlertCircle size={14} />
            <span>{error_message}</span>
          </div>
        )}

        {/* Footer: Status, Tanggal, dan Tombol Aksi (Edit/Copy) */}
        <div className="card_footer">
          <div className="status_container">
            <span className={`status status_${analysis_status}`}>
              {analysis_status}
            </span>
            <span className="date">
              <Calendar size={12} />
              {formatDate(created_at)}
            </span>
          </div>

          <div className="actions_container">
            {/* Tombol Edit */}
            <button
              className="action_button edit_button"
              onClick={(e) => {
                e.stopPropagation();
                onEdit(review);
              }}
              title="Edit Review"
            >
              <Edit2 size={14} />
            </button>
            {/* Tombol Copy */}
            <button
              className="action_button copy_button"
              onClick={handleCopy}
              title="Copy Review Text"
            >
              <Copy size={14} />
            </button>
          </div>
        </div>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  .card {
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
    gap: 0.75rem;
    padding: 1.25rem;
    width: 100%;
    max-width: 400px;
    
    background-color: hsla(240, 15%, 9%, 1);
    /* background-image removed as requested */

    border-radius: 1rem;
    box-shadow: 0px -16px 24px 0px rgba(255, 255, 255, 0.15) inset;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  /* Hover effects removed */

  .card .card__border {
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

  .card .card__border::before {
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

  .card_header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .card .card_title__container .card_title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--white);
  }

  .product_badge {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.6rem;
    background: hsla(189, 92%, 58%, 0.15);
    border-radius: 9999px;
    font-size: 0.7rem;
    color: var(--primary);
    border: 1px solid hsla(189, 92%, 58%, 0.3);
  }

  .card .card_title__container .card_paragraph {
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: var(--paragraph);
    line-height: 1.5;
  }

  .card .line {
    width: 100%;
    height: 1px;
    background-color: var(--line);
    border: none;
  }

  .sentiment_section {
    display: flex;
    justify-content: flex-start;
  }

  .sentiment_badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: capitalize;
  }

  .sentiment_positive {
    background: hsla(142, 76%, 46%, 0.15);
    color: var(--positive);
    border: 1px solid hsla(142, 76%, 46%, 0.3);
  }

  .sentiment_negative {
    background: hsla(0, 72%, 51%, 0.15);
    color: var(--negative);
    border: 1px solid hsla(0, 72%, 51%, 0.3);
  }

  .sentiment_neutral {
    background: hsla(45, 93%, 55%, 0.15);
    color: var(--neutral);
    border: 1px solid hsla(45, 93%, 55%, 0.3);
  }

  .score {
    opacity: 0.8;
    font-weight: 400;
  }

  .key_points_header {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--primary);
    margin-top: 0.25rem;
  }

  .card .card__list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    margin-top: 0.25rem;
  }

  .card .card__list .card__list_item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .card .card__list .card__list_item .check {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
    width: 1rem;
    height: 1rem;
    margin-top: 0.1rem;
    background-color: var(--primary);
    border-radius: 50%;
  }

  .card .card__list .card__list_item .check .check_svg {
    color: var(--black);
  }

  .card .card__list .card__list_item .list_text {
    font-size: 0.75rem;
    color: var(--white);
    line-height: 1.4;
  }

  .error_message {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.5rem;
    background: hsla(0, 72%, 51%, 0.1);
    border-radius: 0.5rem;
    font-size: 0.7rem;
    color: var(--negative);
    border: 1px solid hsla(0, 72%, 51%, 0.2);
  }

  .card_footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 0.5rem;
    border-top: 1px solid var(--line);
  }

  .status_container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .status {
    padding: 0.2rem 0.5rem;
    border-radius: 9999px;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: capitalize;
  }

  .status_completed {
    background: hsla(142, 76%, 46%, 0.15);
    color: var(--positive);
  }

  .status_processing {
    background: hsla(45, 93%, 55%, 0.15);
    color: var(--neutral);
  }

  .status_failed {
    background: hsla(0, 72%, 51%, 0.15);
    color: var(--negative);
  }

  .status_partial {
    background: hsla(45, 93%, 55%, 0.15);
    color: var(--neutral);
  }

  .date {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.65rem;
    color: var(--paragraph);
  }

  .actions_container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .action_button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
  }

  /* Edit Button - Yellow */
  .edit_button {
    background: hsla(48, 100%, 50%, 0.1);
    border-color: hsla(48, 100%, 50%, 0.3);
    color: hsl(48, 100%, 50%);
  }

  .edit_button:hover {
    background: hsl(48, 100%, 50%);
    color: var(--black);
    transform: scale(1.05);
  }

  /* Copy Button - Green */
  .copy_button {
    background: hsla(142, 76%, 46%, 0.1);
    border-color: hsla(142, 76%, 46%, 0.3);
    color: hsl(142, 76%, 46%);
  }

  .copy_button:hover {
    background: hsl(142, 76%, 46%);
    color: white;
    transform: scale(1.05);
  }

  /* Delete Button - Red (Top Right) */
  .delete_button_top {
    position: absolute;
    top: 0.25rem;
    right: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: none;
    background: transparent;
    color: var(--paragraph);
    cursor: pointer;
    transition: all 0.2s ease;
    z-index: 999;
    pointer-events: auto;
  }

  .delete_button_top:hover {
    background: hsla(0, 72%, 51%, 0.15);
    color: var(--negative);
    transform: scale(1.1);
  }
`;

export default ReviewCard;
