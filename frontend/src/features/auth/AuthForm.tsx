import React from 'react';

export function AuthForm() {
  return (
    <div className="glass-panel" style={{ padding: '32px', maxWidth: '400px', margin: '0 auto' }}>
      <h2 style={{ marginBottom: '24px', textAlign: 'center' }}>Welcome Back</h2>
      <form style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.875rem' }}>Email</label>
          <input 
            type="email" 
            placeholder="you@example.com"
            style={{
              width: '100%',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid var(--border-medium)',
              outline: 'none'
            }} 
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.875rem' }}>Password</label>
          <input 
            type="password" 
            placeholder="••••••••"
            style={{
              width: '100%',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid var(--border-medium)',
              outline: 'none'
            }} 
          />
        </div>
        <button 
          type="submit"
          style={{
            marginTop: '16px',
            padding: '14px',
            background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))',
            color: 'white',
            fontWeight: '600',
            borderRadius: '8px',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Sign In
        </button>
      </form>
    </div>
  );
}
