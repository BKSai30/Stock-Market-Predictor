import React from 'react';
import ReactDOM from 'react-dom/client';
import './main.js';  // Import our custom JavaScript

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div>Loading...</div>
  </React.StrictMode>
);

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (window.initializeApp) {
        window.initializeApp();
    }
});
