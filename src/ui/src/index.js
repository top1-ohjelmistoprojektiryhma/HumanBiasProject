
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './App.css';

/**
 * Main entry point of the application.
 * 
 * This script initializes the React application by rendering the App component
 * into the root DOM element.
 */

// Get the root container element from the HTML document
const container = document.getElementById('root');

// Create a root for React to render the application
const root = createRoot(container);

// Render the App component inside the root container
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);