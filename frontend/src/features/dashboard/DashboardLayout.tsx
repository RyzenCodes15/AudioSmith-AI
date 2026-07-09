import React from 'react';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-base)' }}>
      {/* Sidebar */}
      <aside style={{ 
        width: '260px', 
        background: 'var(--bg-surface)', 
        borderRight: '1px solid var(--border-subtle)',
        padding: '24px'
      }}>
        <div style={{ fontWeight: '700', fontSize: '1.25rem', marginBottom: '40px' }}>
          AudioSmith
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <a href="#" style={{ padding: '12px 16px', background: 'rgba(255,126,95,0.1)', color: 'var(--accent-primary)', borderRadius: '8px', fontWeight: '500' }}>Dashboard</a>
          <a href="#" style={{ padding: '12px 16px', color: 'var(--text-secondary)', fontWeight: '500' }}>History</a>
          <a href="#" style={{ padding: '12px 16px', color: 'var(--text-secondary)', fontWeight: '500' }}>Settings</a>
        </nav>
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, padding: '40px' }}>
        <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '40px' }}>
          <h1 style={{ fontSize: '1.5rem' }}>Dashboard</h1>
          <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--border-medium)' }} />
        </header>
        {children}
      </main>
    </div>
  );
}
