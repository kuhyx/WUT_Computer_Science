import App from './App';
import { ContextProvider } from './context/Context';
import React from 'react';
import ReactDOM from 'react-dom/client';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ContextProvider> 
    <App />
    </ContextProvider>
  </React.StrictMode>
);

