/**
 * Review Form Component
 * Form for submitting reviews for analysis
 */
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Send, Package, FileText, Sparkles, Eraser } from 'lucide-react';

const ReviewForm = ({ onSubmit, isLoading, initialValues }) => {
  // State untuk menyimpan teks review dan nama produk
  const [reviewText, setReviewText] = useState('');
  const [productName, setProductName] = useState('');

  // State untuk menyimpan pesan error validasi
  const [errors, setErrors] = useState({});

  /**
   * Effect untuk mengisi form jika ada data awal (misal saat edit).
   * Dijalankan setiap kali `initialValues` berubah.
   */
  useEffect(() => {
    if (initialValues) {
      setReviewText(initialValues.review_text || '');
      setProductName(initialValues.product_name || '');
    } else {
      setReviewText('');
      setProductName('');
    }
  }, [initialValues]);

  /**
   * Fungsi validasi form sebelum submit.
   * Mengecek apakah review kosong atau terlalu pendek/panjang.
   */
  const validateForm = () => {
    const newErrors = {};

    if (!reviewText.trim()) {
      newErrors.reviewText = 'Please enter your review';
    } else if (reviewText.trim().length < 10) {
      newErrors.reviewText = 'Review must be at least 10 characters';
    } else if (reviewText.trim().length > 5000) {
      newErrors.reviewText = 'Review must be less than 5000 characters';
    }

    setErrors(newErrors);
    // Mengembalikan true jika tidak ada error
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handler saat form disubmit.
   * Mencegah reload halaman default dan memanggil fungsi `onSubmit` dari parent.
   */
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    // Kirim data ke parent component
    onSubmit({
      review_text: reviewText.trim(),
      product_name: productName.trim() || null
    });
  };

  /**
   * Mereset form ke kondisi awal (kosong).
   */
  const handleClear = () => {
    setReviewText('');
    setProductName('');
    setErrors({});
  };

  // Menghitung jumlah karakter saat ini untuk ditampilkan
  const characterCount = reviewText.length;
  const maxCharacters = 5000;

  return (
    <StyledWrapper>
      <form onSubmit={handleSubmit} className="form">
        <div className="form__border" />

        <div className="form_header">
          <div className="icon_container">
            <Sparkles size={24} />
          </div>
          <h2 className="form_title">Analyze Review</h2>
          <p className="form_subtitle">Enter a product review to analyze sentiment and extract key points</p>
        </div>

        <hr className="line" />

        {/* Input Nama Produk (Opsional) */}
        <div className="input_group">
          <label className="input_label">
            <Package size={14} />
            Product Name <span className="optional">(optional)</span>
          </label>
          <input
            type="text"
            className="input_field"
            placeholder="e.g., iPhone 15 Pro, Sony WH-1000XM5..."
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            disabled={isLoading}
            maxLength={255}
          />
        </div>

        {/* Input Teks Review (Wajib) */}
        <div className="input_group">
          <label className="input_label">
            <FileText size={14} />
            Review Text <span className="required">*</span>
          </label>
          <textarea
            className={`textarea_field ${errors.reviewText ? 'error' : ''}`}
            placeholder="Paste or type your product review here..."
            value={reviewText}
            onChange={(e) => {
              setReviewText(e.target.value);
              // Hapus error saat user mulai mengetik ulang
              if (errors.reviewText) {
                setErrors({ ...errors, reviewText: null });
              }
            }}
            disabled={isLoading}
            rows={6}
          />
          <div className="textarea_footer">
            {errors.reviewText && (
              <span className="error_text">{errors.reviewText}</span>
            )}
            <span className={`char_count ${characterCount > maxCharacters ? 'error' : ''}`}>
              {characterCount} / {maxCharacters}
            </span>
          </div>
        </div>

        {/* Tombol Aksi (Clear & Analyze) */}
        <div className="button_group">
          <button
            type="button"
            className="button_secondary"
            onClick={handleClear}
            disabled={isLoading || (!reviewText && !productName)}
          >
            <Eraser size={16} />
            Clear
          </button>
          <button
            type="submit"
            className="button_primary"
            disabled={isLoading || !reviewText.trim()}
          >
            {isLoading ? (
              <span className="button_loading">
                <span className="spinner" />
                Analyzing...
              </span>
            ) : (
              <>
                <Send size={16} />
                Analyze Review
              </>
            )}
          </button>
        </div>
      </form>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  width: 100%;
  width: 100%;

  .form {
    --white: hsl(0, 0%, 100%);
    --black: hsl(240, 15%, 9%);
    --paragraph: hsl(0, 0%, 83%);
    --line: hsl(240, 9%, 17%);
    --primary: hsl(189, 92%, 58%);
    --primary-dark: hsl(189, 99%, 26%);
    --error: hsl(0, 72%, 51%);

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
      radial-gradient(at 0% 64%, hsl(189, 99%, 26%) 0px, transparent 85%),
      radial-gradient(at 41% 94%, hsl(189, 97%, 36%) 0px, transparent 85%),
      radial-gradient(at 100% 99%, hsl(188, 94%, 13%) 0px, transparent 85%);

    border-radius: 1rem;
    box-shadow: 0px -16px 24px 0px rgba(255, 255, 255, 0.25) inset;
  }

  .form__border {
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

  .form__border::before {
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
      hsl(189, 100%, 50%) 40%,
      hsl(189, 100%, 50%) 60%,
      hsla(0, 0%, 40%, 0) 100%
    );
    animation: rotate 8s linear infinite;
  }

  @keyframes rotate {
    to {
      transform: rotate(360deg);
    }
  }

  .form_header {
    text-align: center;
  }

  .icon_container {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    margin-bottom: 0.75rem;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    border-radius: 50%;
    color: var(--black);
    box-shadow: 0 0 20px hsla(189, 92%, 58%, 0.4);
  }

  .form_title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 0.5rem;
  }

  .form_subtitle {
    font-size: 0.85rem;
    color: var(--paragraph);
    max-width: 300px;
    margin: 0 auto;
  }

  .line {
    width: 100%;
    height: 1px;
    background-color: var(--line);
    border: none;
  }

  .input_group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .input_label {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--white);
  }

  .optional {
    color: var(--paragraph);
    font-weight: 400;
    font-size: 0.75rem;
  }

  .required {
    color: var(--primary);
  }

  .input_field,
  .textarea_field {
    width: 100%;
    padding: 0.75rem 1rem;
    background: hsla(240, 15%, 15%, 0.5);
    border: 1px solid var(--line);
    border-radius: 0.5rem;
    color: var(--white);
    font-family: inherit;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }

  .input_field:focus,
  .textarea_field:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px hsla(189, 92%, 58%, 0.15);
  }

  .input_field::placeholder,
  .textarea_field::placeholder {
    color: hsla(0, 0%, 100%, 0.3);
  }

  .input_field:disabled,
  .textarea_field:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .textarea_field {
    min-height: 150px;
    resize: vertical;
    line-height: 1.5;
  }

  .textarea_field.error {
    border-color: var(--error);
  }

  .textarea_footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
  }

  .error_text {
    font-size: 0.75rem;
    color: var(--error);
  }

  .char_count {
    font-size: 0.75rem;
    color: var(--paragraph);
    margin-left: auto;
  }

  .char_count.error {
    color: var(--error);
  }

  .button_group {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }

  .button_primary,
  .button_secondary {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    border-radius: 9999px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
  }

  .button_primary {
    flex: 1;
    background-image: linear-gradient(
      0deg,
      hsl(189, 92%, 58%),
      hsl(189, 99%, 26%) 100%
    );
    color: var(--white);
    box-shadow: inset 0 -2px 25px -4px var(--white);
  }

  .button_primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: inset 0 -2px 25px -4px var(--white),
                0 5px 20px hsla(189, 92%, 58%, 0.3);
  }

  .button_primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  .button_secondary {
    background: hsla(240, 15%, 20%, 0.5);
    color: var(--paragraph);
    border: 1px solid var(--line);
  }

  .button_secondary:hover:not(:disabled) {
    background: hsla(240, 15%, 25%, 0.5);
    color: var(--white);
  }

  .button_secondary:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .button_loading {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid hsla(0, 0%, 100%, 0.3);
    border-top-color: var(--white);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  @media (max-width: 480px) {
    .form {
      padding: 1.25rem;
    }

    .form_title {
      font-size: 1.25rem;
    }

    .button_group {
      flex-direction: column-reverse;
    }

    .button_secondary {
      flex: none;
    }
  }
`;

export default ReviewForm;
