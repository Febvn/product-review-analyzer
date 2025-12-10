/**
 * API Service for Review Analyzer
 */
import axios from 'axios';

// API Base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000, // 5 minutes timeout for first-time AI model download
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => {
        console.log(`[API] Response:`, response.status);
        return response;
    },
    (error) => {
        console.error('[API] Response error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

/**
 * Analyze a new product review
 * @param {Object} reviewData - The review data
 * @param {string} reviewData.review_text - The review text to analyze
 * @param {string} [reviewData.product_name] - Optional product name
 * @returns {Promise<Object>} Analysis result
 */
export const analyzeReview = async (reviewData) => {
    try {
        const response = await api.post('/api/analyze-review', reviewData);
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to analyze review';
        throw new Error(errorMessage);
    }
};

/**
 * Get all reviews with optional filtering
 * @param {Object} [params] - Query parameters
 * @param {number} [params.skip=0] - Number of records to skip
 * @param {number} [params.limit=50] - Number of records to return
 * @param {string} [params.sentiment] - Filter by sentiment
 * @returns {Promise<Object>} List of reviews
 */
export const getReviews = async (params = {}) => {
    try {
        const response = await api.get('/api/reviews', { params });
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to fetch reviews';
        throw new Error(errorMessage);
    }
};

/**
 * Get a specific review by ID
 * @param {number} reviewId - The review ID
 * @returns {Promise<Object>} Review data
 */
export const getReview = async (reviewId) => {
    try {
        const response = await api.get(`/api/reviews/${reviewId}`);
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to fetch review';
        throw new Error(errorMessage);
    }
};

/**
 * Delete a review by ID
 * @param {number} reviewId - The review ID
 * @returns {Promise<Object>} Deletion result
 */
export const deleteReview = async (reviewId) => {
    try {
        const response = await api.delete(`/api/reviews/${reviewId}`);
        return response.data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to delete review';
        throw new Error(errorMessage);
    }
};

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch (error) {
        throw new Error('API is not available');
    }
};

export default api;
