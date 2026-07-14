'use client';

import React, { useState } from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/lib/auth/AuthContext';
import { Logo } from '@/components/common/Logo';
import { LogOut } from 'lucide-react';
import { motion } from 'framer-motion';
import { UploadSection } from '@/components/dashboard/UploadSection';
import { ProcessingHistory } from '@/components/dashboard/ProcessingHistory';
import styles from './Dashboard.module.css';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadComplete = () => {
    // Trigger history refresh
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <ProtectedRoute>
      <div className={styles.dashboardWrapper}>
        <header className={styles.header}>
          <div className={`container ${styles.headerContent}`}>
            <Logo />
            
            <div className={styles.userSection}>
              <div className={styles.userInfo}>
                <span className={styles.userName}>{user?.full_name}</span>
                <span className={styles.userEmail}>{user?.email}</span>
              </div>
              <button onClick={logout} className={styles.logoutBtn}>
                <LogOut size={18} />
                <span>Log out</span>
              </button>
            </div>
          </div>
        </header>

        <main className={styles.mainContent}>
          <div className="container">
            <motion.div 
              className={styles.welcomeSection}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className={styles.welcomeTitle}>
                Welcome back, {user?.full_name?.split(' ')[0] || 'User'}!
              </h1>
            </motion.div>

            <div className="glass-panel" style={{ padding: '24px', marginBottom: '32px' }}>
              <UploadSection onUploadComplete={handleUploadComplete} />
            </div>
            
            <div className="glass-panel" style={{ padding: '24px' }}>
              <ProcessingHistory refreshTrigger={refreshTrigger} />
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
