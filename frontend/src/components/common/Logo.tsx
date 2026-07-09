import React from 'react';
import { AudioWaveform } from 'lucide-react';

interface LogoProps {
  className?: string;
  iconClassName?: string;
  textClassName?: string;
}

export function Logo({ className = '', iconClassName = '', textClassName = '' }: LogoProps) {
  return (
    <div className={`flex items-center gap-2 ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <div 
        className={iconClassName}
        style={{ 
          width: '2rem', 
          height: '2rem', 
          borderRadius: '0.5rem', 
          background: 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center' 
        }}
      >
        <AudioWaveform color="white" size={18} strokeWidth={2.5} />
      </div>
      <span 
        className={textClassName}
        style={{ 
          fontWeight: 700, 
          fontSize: '1.25rem', 
          letterSpacing: '-0.02em', 
          color: 'var(--text-primary)',
          fontFamily: "'Outfit', sans-serif"
        }}
      >
        AudioSmith <span style={{ color: 'var(--accent-primary)' }}>AI</span>
      </span>
    </div>
  );
}
