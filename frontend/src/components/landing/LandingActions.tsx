'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/AuthContext';
import styles from '@/app/page.module.css';

export function NavActions() {
  const { user } = useAuth();

  if (user) {
    return (
      <>
        <Link href="/dashboard" className={styles.signupBtn}>Dashboard</Link>
      </>
    );
  }

  return (
    <>
      <Link href="/login" className={styles.loginBtn}>Log In</Link>
      <Link href="/register" className={styles.signupBtn}>Get Started</Link>
    </>
  );
}

export function HeroActions() {
  const { user } = useAuth();

  if (user) {
    return (
      <div className={styles.ctaGroup}>
        <Link href="/dashboard" className={styles.primaryBtn}>Go to Dashboard</Link>
      </div>
    );
  }

  return (
    <div className={styles.ctaGroup}>
      <Link href="/register" className={styles.primaryBtn}>Try for Free</Link>
      <Link href="#demo" className={styles.secondaryBtn}>Watch Demo</Link>
    </div>
  );
}
