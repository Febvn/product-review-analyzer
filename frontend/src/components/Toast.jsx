/**
 * Toast Notification Component
 * Displays success/error messages
 */
import React, { useEffect } from 'react';
import styled from 'styled-components';
import { CheckCircle, XCircle, AlertTriangle, X, Info } from 'lucide-react';

const Toast = ({ message, type = 'info', onClose, duration = 5000 }) => {
  /**
   * Effect hook untuk menghilangkan toast secara otomatis setelah durasi tertentu.
   * Membersihkan timeout saat komponen unmount untuk mencegah memory leak.
   */
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  /**
   * Helper untuk memilih icon berdasarkan tipe toast (success, error, warning, info).
   */
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle size={20} />;
      case 'error':
        return <XCircle size={20} />;
      case 'warning':
        return <AlertTriangle size={20} />;
      default:
        return <Info size={20} />;
    }
  };

  return (
    // StyledWrapper menerima prop $type untuk mengatur warna tema toast
    <StyledWrapper $type={type}>
      <div className="toast">
        <span className="toast_icon">{getIcon()}</span>
        <p className="toast_message">{message}</p>
        <button className="toast_close" onClick={onClose}>
          <X size={16} />
        </button>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 1000;
  animation: slideIn 0.3s ease forwards;

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .toast {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    min-width: 300px;
    max-width: 450px;
    
    background: hsla(240, 15%, 12%, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid ${props =>
    props.$type === 'success' ? 'hsla(142, 76%, 46%, 0.3)' :
      props.$type === 'error' ? 'hsla(0, 72%, 51%, 0.3)' :
        props.$type === 'warning' ? 'hsla(45, 93%, 55%, 0.3)' :
          'hsla(189, 92%, 58%, 0.3)'
  };
    border-radius: 0.75rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3),
                0 0 20px ${props =>
    props.$type === 'success' ? 'hsla(142, 76%, 46%, 0.15)' :
      props.$type === 'error' ? 'hsla(0, 72%, 51%, 0.15)' :
        props.$type === 'warning' ? 'hsla(45, 93%, 55%, 0.15)' :
          'hsla(189, 92%, 58%, 0.15)'
  };
  }

  .toast_icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: ${props =>
    props.$type === 'success' ? 'hsl(142, 76%, 46%)' :
      props.$type === 'error' ? 'hsl(0, 72%, 51%)' :
        props.$type === 'warning' ? 'hsl(45, 93%, 55%)' :
          'hsl(189, 92%, 58%)'
  };
  }

  .toast_message {
    flex: 1;
    font-size: 0.9rem;
    color: hsl(0, 0%, 100%);
    margin: 0;
    line-height: 1.4;
  }

  .toast_close {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.25rem;
    background: transparent;
    border: none;
    border-radius: 0.25rem;
    color: hsl(0, 0%, 60%);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .toast_close:hover {
    background: hsla(0, 0%, 100%, 0.1);
    color: hsl(0, 0%, 100%);
  }

  @media (max-width: 480px) {
    top: 1rem;
    right: 1rem;
    left: 1rem;

    .toast {
      min-width: auto;
      max-width: none;
    }
  }
`;

export default Toast;
