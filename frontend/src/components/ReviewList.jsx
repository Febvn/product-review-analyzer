/**
 * Review List Component
 * Displays a grid of all analyzed reviews
 */
import React from 'react';
import styled from 'styled-components';
import {
  History,
  Filter,
  RefreshCw,
  ChevronDown,
  Inbox
} from 'lucide-react';
import ReviewCard from './ReviewCard';

const ReviewList = ({
  reviews,          // Array data ulasan
  loading,          // Status loading saat refresh/fetch
  onRefresh,        // Fungsi untuk refresh data manual
  selectedFilter,   // Filter sentimen yang dipilih saat ini
  onFilterChange,   // Handler saat filter berubah
  onDeleteReview,   // Handler hapus review
  onEditReview      // Handler edit review
}) => {
  // Opsi filter yang tersedia untuk dropdown
  const filterOptions = [
    { value: '', label: 'All Reviews' },
    { value: 'positive', label: 'Positive' },
    { value: 'negative', label: 'Negative' },
    { value: 'neutral', label: 'Neutral' }
  ];

  return (
    <StyledWrapper>
      <div className="list_container">
        {/* Dekorasi border background */}
        <div className="list_border" />

        {/* Header List: Judul, Jumlah Review, dan Tombol Filter/Refresh */}
        <div className="list_header">
          <div className="header_title">
            <History size={20} />
            <h2>Analysis History</h2>
            <span className="review_count">{reviews.length} reviews</span>
          </div>

          <div className="header_actions">
            {/* Dropdown Filter Sentimen */}
            <div className="filter_wrapper">
              <Filter size={14} />
              <select
                value={selectedFilter}
                onChange={(e) => onFilterChange(e.target.value)}
                className="filter_select"
              >
                {filterOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <ChevronDown size={14} className="dropdown_arrow" />
            </div>

            {/* Tombol Refresh Manual */}
            <button
              className={`refresh_button ${loading ? 'loading' : ''}`}
              onClick={onRefresh}
              disabled={loading}
            >
              <RefreshCw size={16} />
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>

        <hr className="line" />

        {/* Kondisional Rendering untuk Grid Review */}
        {loading && reviews.length === 0 ? (
          // Tampilan Loading Awal (jika belum ada data)
          <div className="loading_state">
            <div className="spinner" />
            <p>Loading reviews...</p>
          </div>
        ) : reviews.length === 0 ? (
          // Tampilan Kosong (Empty State) jika tidak ada review
          <div className="empty_state">
            <Inbox size={48} />
            <h3>No reviews yet</h3>
            <p>Analyze your first review to see it here</p>
          </div>
        ) : (
          // Grid Review (jika ada data)
          <div className="reviews_grid">
            {reviews.map((review, index) => (
              <div
                key={review.id}
                className="review_item"
                // Animasi bertahap (staggered animation) untuk setiap item
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <ReviewCard
                  review={review}
                  onDelete={onDeleteReview}
                  onEdit={onEditReview}
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  width: 100%;

  .list_container {
    --white: hsl(0, 0%, 100%);
    --black: hsl(240, 15%, 9%);
    --paragraph: hsl(0, 0%, 83%);
    --line: hsl(240, 9%, 17%);
    --primary: hsl(189, 92%, 58%);

    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1rem;
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

  .list_border {
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

  .list_border::before {
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

  .list_header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .header_title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--white);
  }

  .header_title h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
  }

  .review_count {
    padding: 0.25rem 0.6rem;
    background: hsla(189, 92%, 58%, 0.15);
    border-radius: 9999px;
    font-size: 0.75rem;
    color: var(--primary);
  }

  .header_actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .filter_wrapper {
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: hsla(240, 15%, 15%, 0.5);
    border: 1px solid var(--line);
    border-radius: 0.5rem;
    color: var(--paragraph);
  }

  .filter_select {
    appearance: none;
    background: transparent;
    border: none;
    color: var(--white);
    font-size: 0.85rem;
    cursor: pointer;
    padding-right: 1rem;
  }

  .filter_select:focus {
    outline: none;
  }

  .filter_select option {
    background: var(--black);
    color: var(--white);
  }

  .dropdown_arrow {
    position: absolute;
    right: 0.75rem;
    pointer-events: none;
    color: var(--paragraph);
  }

  .refresh_button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: hsla(189, 92%, 58%, 0.15);
    border: 1px solid hsla(189, 92%, 58%, 0.3);
    border-radius: 0.5rem;
    color: var(--primary);
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .refresh_button:hover:not(:disabled) {
    background: hsla(189, 92%, 58%, 0.25);
  }

  .refresh_button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .refresh_button.loading svg {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .line {
    width: 100%;
    height: 1px;
    background-color: var(--line);
    border: none;
  }

  .loading_state,
  .empty_state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 3rem;
    text-align: center;
    color: var(--paragraph);
  }

  .loading_state .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid hsla(189, 92%, 58%, 0.2);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .empty_state svg {
    color: hsla(0, 0%, 100%, 0.2);
  }

  .empty_state h3 {
    font-size: 1.1rem;
    color: var(--white);
    margin: 0;
  }

  .empty_state p {
    font-size: 0.85rem;
    margin: 0;
  }

  .reviews_grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
    margin-top: 0.5rem;
  }

  .review_item {
    animation: fadeInUp 0.5s ease forwards;
    animation-fill-mode: both;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (max-width: 768px) {
    .list_container {
      padding: 1rem;
    }

    .list_header {
      flex-direction: column;
      align-items: flex-start;
    }

    .header_actions {
      width: 100%;
      justify-content: space-between;
    }

    .reviews_grid {
      grid-template-columns: 1fr;
    }
  }
`;

export default ReviewList;
