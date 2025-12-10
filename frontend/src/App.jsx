/**
 * Product Review Analyzer
 * Main Application Component
 */
import React, { useState, useEffect, useCallback } from 'react';
import styled from 'styled-components';
import { Sparkles, MessageSquareText, Github, Zap } from 'lucide-react';
import {
  ReviewForm,
  AnalysisResult,
  ReviewList,
  Loader,
  Toast,
  SocialButton
} from './components';
import { analyzeReview, getReviews, healthCheck, deleteReview } from './api/reviewApi';

function App() {
  // State Management
  const [reviews, setReviews] = useState([]);
  const [currentResult, setCurrentResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isLoadingReviews, setIsLoadingReviews] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('');
  const [toast, setToast] = useState(null);
  const [view, setView] = useState('form'); // 'form', 'result', 'loading'
  const [apiStatus, setApiStatus] = useState('checking'); // 'checking', 'online', 'offline'

  // Show toast notification
  const showToast = (message, type = 'info') => {
    setToast({ message, type });
  };

  // Check API health
  const checkApiHealth = useCallback(async () => {
    try {
      await healthCheck();
      setApiStatus('online');
    } catch (error) {
      setApiStatus('offline');
    }
  }, []);

  // Fetch reviews from API
  const fetchReviews = useCallback(async () => {
    setIsLoadingReviews(true);
    try {
      const params = selectedFilter ? { sentiment: selectedFilter } : {};
      const response = await getReviews(params);
      setReviews(response.reviews || []);
    } catch (error) {
      console.error('Failed to fetch reviews:', error);
      showToast('Failed to load reviews. Please check if the API is running.', 'error');
    } finally {
      setIsLoadingReviews(false);
    }
  }, [selectedFilter]);

  // Check API and fetch reviews on mount
  useEffect(() => {
    checkApiHealth();
  }, [checkApiHealth]);

  useEffect(() => {
    if (apiStatus === 'online') {
      fetchReviews();
    }
  }, [apiStatus, fetchReviews]);

  // Handle review submission
  const handleSubmitReview = async (reviewData) => {
    setIsAnalyzing(true);
    setView('loading');

    try {
      const result = await analyzeReview(reviewData);
      setCurrentResult(result);
      setView('result');
      showToast('Review analyzed successfully!', 'success');

      // Refresh reviews list
      fetchReviews();
    } catch (error) {
      console.error('Analysis failed:', error);
      showToast(error.message || 'Failed to analyze review', 'error');
      setView('form');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Handle new analysis
  const handleNewAnalysis = () => {
    setCurrentResult(null);
    setView('form');
  };

  // Handle filter change
  const handleFilterChange = (filter) => {
    setSelectedFilter(filter);
  };

  // Handle review deletion
  const handleDeleteReview = async (id) => {
    try {
      await deleteReview(id);
      showToast('Review deleted successfully', 'success');
      // Remove from local state immediately for better UX
      setReviews(prevReviews => prevReviews.filter(review => review.id !== id));
    } catch (error) {
      console.error('Failed to delete review:', error);
      showToast('Failed to delete review', 'error');
    }
  };

  return (
    <StyledApp>
      {/* Toast Notification */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      {/* Header */}
      <header className="header">
        <div className="header_content">
          <div className="logo">
            <div className="logo_icon">
              <Sparkles size={24} />
            </div>
            <div className="logo_text">
              <h1>Review Analyzer</h1>
              <span className="tagline">AI-Powered Product Review Analysis</span>
            </div>
          </div>

          <div className="header_status">
            <span className={`api_status ${apiStatus}`}>
              <span className="status_dot" />
              {apiStatus === 'checking' && 'Checking API...'}
              {apiStatus === 'online' && 'API Online'}
              {apiStatus === 'offline' && 'API Offline'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero_content">
            <h2 className="hero_title">
              <span className="gradient_text">Understand</span> Your Product Reviews
            </h2>
            <p className="hero_subtitle">
              Use AI to analyze sentiment and extract key insights from customer feedback
            </p>

            <div className="features">
              <div className="feature">
                <MessageSquareText size={18} />
                <span>Sentiment Analysis</span>
              </div>
              <div className="feature">
                <Sparkles size={18} />
                <span>Key Points Extraction</span>
              </div>
              <div className="feature">
                <Zap size={18} />
                <span>Instant Results</span>
              </div>
            </div>
          </div>
        </section>

        {/* Analysis Section */}
        <section className="analysis_section">
          <div className="analysis_container">
            {view === 'form' && (
              <ReviewForm
                onSubmit={handleSubmitReview}
                isLoading={isAnalyzing}
              />
            )}

            {view === 'loading' && <Loader />}

            {view === 'result' && currentResult && (
              <AnalysisResult
                result={currentResult}
                onNewAnalysis={handleNewAnalysis}
              />
            )}
          </div>
        </section>

        {/* API Offline Warning */}
        {apiStatus === 'offline' && (
          <section className="offline_warning">
            <div className="warning_card">
              <h3>⚠️ Backend API is Offline</h3>
              <p>Please start the backend server to use the analyzer:</p>
              <div className="code_block">
                <code>cd backend</code>
                <code>pip install -r requirements.txt</code>
                <code>python run.py</code>
              </div>
              <button className="retry_button" onClick={checkApiHealth}>
                Retry Connection
              </button>
            </div>
          </section>
        )}

        {/* History Section */}
        {apiStatus === 'online' && (
          <section className="history_section">
            <ReviewList
              reviews={reviews}
              loading={isLoadingReviews}
              onRefresh={fetchReviews}
              selectedFilter={selectedFilter}
              onFilterChange={handleFilterChange}
              onDeleteReview={handleDeleteReview}
            />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer_content">
          <p className="copyright">
            © Febvn
          </p>
          <div className="tech_stack">
            <SocialButton />
          </div>
        </div>
      </footer>
    </StyledApp>
  );
}

const StyledApp = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;

  .header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: hsla(240, 15%, 9%, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid hsla(0, 0%, 100%, 0.1);
  }

  .header_content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 1.5rem;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .logo_icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    background: linear-gradient(135deg, hsl(189, 92%, 58%) 0%, hsl(189, 99%, 26%) 100%);
    border-radius: 0.5rem;
    color: hsl(240, 15%, 9%);
  }

  .logo_text h1 {
    font-size: 1.25rem;
    font-weight: 700;
    color: hsl(0, 0%, 100%);
    margin: 0;
  }

  .tagline {
    font-size: 0.7rem;
    color: hsl(0, 0%, 60%);
  }

  .header_status {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .api_status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.75rem;
    background: hsla(240, 15%, 15%, 0.5);
    border-radius: 9999px;
    font-size: 0.75rem;
    color: hsl(0, 0%, 70%);
  }

  .status_dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: hsl(45, 93%, 55%);
  }

  .api_status.online .status_dot {
    background: hsl(142, 76%, 46%);
    box-shadow: 0 0 8px hsl(142, 76%, 46%);
  }

  .api_status.offline .status_dot {
    background: hsl(0, 72%, 51%);
    box-shadow: 0 0 8px hsl(0, 72%, 51%);
  }

  .main {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  .hero {
    text-align: center;
    margin-bottom: 1rem;
  }

  .hero_title {
    font-size: 2.5rem;
    font-weight: 700;
    color: hsl(0, 0%, 100%);
    margin-bottom: 0.75rem;
  }

  .gradient_text {
    background: linear-gradient(135deg, hsl(189, 92%, 58%) 0%, hsl(189, 100%, 70%) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero_subtitle {
    font-size: 1.1rem;
    color: hsl(0, 0%, 70%);
    max-width: 500px;
    margin: 0 auto 1.5rem;
  }

  .features {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
  }

  .feature {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: hsla(240, 15%, 15%, 0.5);
    border: 1px solid hsla(0, 0%, 100%, 0.1);
    border-radius: 9999px;
    font-size: 0.85rem;
    color: hsl(0, 0%, 80%);
  }

  .feature svg {
    color: hsl(189, 92%, 58%);
  }

  .analysis_section {
    display: flex;
    justify-content: center;
  }

  .analysis_container {
    display: flex;
    justify-content: center;
    min-height: 400px;
  }

  .offline_warning {
    display: flex;
    justify-content: center;
  }

  .warning_card {
    padding: 2rem;
    max-width: 500px;
    background: hsla(45, 93%, 55%, 0.1);
    border: 1px solid hsla(45, 93%, 55%, 0.3);
    border-radius: 1rem;
    text-align: center;
  }

  .warning_card h3 {
    font-size: 1.25rem;
    color: hsl(45, 93%, 55%);
    margin-bottom: 0.75rem;
  }

  .warning_card p {
    font-size: 0.9rem;
    color: hsl(0, 0%, 70%);
    margin-bottom: 1rem;
  }

  .code_block {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;
    background: hsla(240, 15%, 9%, 0.8);
    border-radius: 0.5rem;
    margin-bottom: 1rem;
  }

  .code_block code {
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    color: hsl(189, 92%, 58%);
  }

  .retry_button {
    padding: 0.5rem 1.5rem;
    background: hsl(45, 93%, 55%);
    border: none;
    border-radius: 9999px;
    color: hsl(240, 15%, 9%);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .retry_button:hover {
    background: hsl(45, 93%, 65%);
    transform: translateY(-2px);
  }

  .history_section {
    margin-top: 1rem;
  }

  .footer {
    background: hsla(240, 15%, 9%, 0.8);
    border-top: 1px solid hsla(0, 0%, 100%, 0.1);
    padding: 1.5rem;
    margin-top: auto;
  }

  .footer_content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1200px;
    margin: 0 auto;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .copyright {
    font-size: 0.85rem;
    color: hsl(0, 0%, 50%);
    margin: 0;
  }

  .tech_stack {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: hsl(0, 0%, 50%);
  }

  .tech {
    padding: 0.25rem 0.5rem;
    background: hsla(189, 92%, 58%, 0.1);
    border-radius: 0.25rem;
    color: hsl(189, 92%, 58%);
  }

  @media (max-width: 768px) {
    .header_content {
      flex-direction: column;
      gap: 1rem;
    }

    .hero_title {
      font-size: 1.75rem;
    }

    .hero_subtitle {
      font-size: 0.95rem;
    }

    .features {
      gap: 0.75rem;
    }

    .feature {
      font-size: 0.75rem;
      padding: 0.4rem 0.75rem;
    }

    .footer_content {
      flex-direction: column;
      text-align: center;
    }
  }
`;

export default App;
