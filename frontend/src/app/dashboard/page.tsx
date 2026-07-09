'use client';

import React from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/lib/auth/AuthContext';
import { Logo } from '@/components/common/Logo';
import { LogOut, UploadCloud, History, Settings } from 'lucide-react';
import { motion, Variants } from 'framer-motion';
import styles from './Dashboard.module.css';

export default function DashboardPage() {
  const { user, logout } = useAuth();

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } }
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
              <p className={styles.welcomeText}>
                Ready to enhance your audio? Select an option below to get started.
              </p>
            </motion.div>

            <motion.div 
              className={styles.cardsGrid}
              variants={containerVariants}
              initial="hidden"
              animate="show"
            >
              <motion.div className={styles.actionCard} variants={itemVariants}>
                <div className={styles.cardIcon}>
                  <UploadCloud size={32} />
                </div>
                <h3 className={styles.cardTitle}>New Enhancement</h3>
                <p className={styles.cardDesc}>Upload a noisy audio file to isolate speech using our AI model.</p>
              </motion.div>

              <motion.div className={styles.actionCard} variants={itemVariants}>
                <div className={styles.cardIcon}>
                  <History size={32} />
                </div>
                <h3 className={styles.cardTitle}>Processing History</h3>
                <p className={styles.cardDesc}>View and download your previously enhanced audio files.</p>
              </motion.div>

              <motion.div className={styles.actionCard} variants={itemVariants}>
                <div className={styles.cardIcon}>
                  <Settings size={32} />
                </div>
                <h3 className={styles.cardTitle}>Account Settings</h3>
                <p className={styles.cardDesc}>Manage your profile, API keys, and subscription preferences.</p>
              </motion.div>
            </motion.div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
