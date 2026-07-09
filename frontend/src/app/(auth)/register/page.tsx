'use client';

import { RegisterForm } from '@/components/auth/RegisterForm';
import { Logo } from '@/components/common/Logo';
import { motion } from 'framer-motion';
import styles from '@/components/auth/AuthForm.module.css';

export default function RegisterPage() {
  return (
    <div className={styles.pageContainer}>
      <div className={styles.backgroundOrb}></div>
      <div className={styles.backgroundOrb2}></div>
      
      <motion.div 
        className={`glass-panel ${styles.card}`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <div className={styles.logoWrapper}>
          <Logo />
        </div>
        
        <div className={styles.header}>
          <h1 className={styles.title}>Create Account</h1>
          <p className={styles.subtitle}>Join AudioSmith AI for premium speech enhancement.</p>
        </div>
        
        <RegisterForm />
      </motion.div>
    </div>
  );
}
