'use client';

import React, { useState } from 'react';

export function AudioUploader() {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div 
      className="glass-panel"
      style={{
        padding: '60px',
        textAlign: 'center',
        border: isDragging ? '2px dashed var(--accent-primary)' : '2px dashed var(--border-medium)',
        background: isDragging ? 'rgba(255,126,95,0.05)' : 'var(--bg-surface)',
        transition: 'all var(--transition-fast)'
      }}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => { e.preventDefault(); setIsDragging(false); /* Handle drop */ }}
    >
      <div style={{ 
        width: '64px', 
        height: '64px', 
        borderRadius: '50%', 
        background: 'rgba(255,126,95,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '0 auto 24px auto'
      }}>
        <span style={{ fontSize: '24px' }}>🎵</span>
      </div>
      <h3 style={{ marginBottom: '8px' }}>Upload Noisy Audio</h3>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
        Drag and drop your WAV or MP3 file here, or click to browse
      </p>
      <button style={{
        padding: '12px 24px',
        background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
        color: 'white',
        borderRadius: 'var(--radius-full)',
        fontWeight: '600'
      }}>
        Select File
      </button>
    </div>
  );
}
