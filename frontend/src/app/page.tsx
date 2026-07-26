import React from 'react';
import { Logo } from '@/components/common/Logo';
import { NavActions, HeroActions } from '@/components/landing/LandingActions';
import styles from './page.module.css';

export default function Home() {
  return (
    <div className={styles.pageWrapper}>
      {/* Navigation */}
      <nav className={styles.nav}>
        <div className={`container ${styles.navContainer}`}>
          <Logo />
          <div className={styles.navLinks}>
            <a href="#features">Features</a>
            <a href="#how-it-works">How it works</a>
            <NavActions />
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={`container ${styles.heroContainer}`}>
          <div className={`${styles.heroContent} animate-fade-in`}>
            <div className={styles.pillBadge}>
              ✨ Next-Generation Speech Enhancement
            </div>
            <h1 className={styles.title}>
              Crystal Clear Voice,<br />
              <span className="gradient-text">Zero Background Noise.</span>
            </h1>
            <p className={styles.subtitle}>
              Upload your noisy audio and let our advanced deep learning model extract pristine human speech in seconds. Perfect for podcasts, interviews, and professional productions.
            </p>
            <HeroActions />
          </div>
          
          <div className={`${styles.heroVisual} animate-float`}>
            <div className={`glass-panel ${styles.demoCard}`}>
              <div className={styles.demoCardHeader}>
                <div className={styles.demoDots}>
                  <span></span><span></span><span></span>
                </div>
                <div className={styles.demoTitle}>interview_raw.wav</div>
              </div>
              <div className={styles.demoVisualizer}>
                <div className={styles.waveformOriginal}>
                  {/* CSS visualizer lines */}
                  {[45, 60, 35, 70, 25, 80, 50, 40, 65, 30, 55, 75, 45, 60, 35, 70, 25, 80, 50, 40, 65, 30, 55, 75].map((h, i) => (
                    <div key={i} className={styles.waveBar} style={{ height: `${h}%` }} />
                  ))}
                </div>
                <div className={styles.demoDivider}>
                  <span>AI Denoising</span>
                </div>
                <div className={styles.waveformEnhanced}>
                  {[20, 25, 15, 30, 10, 35, 20, 15, 25, 10, 20, 30, 20, 25, 15, 30, 10, 35, 20, 15, 25, 10, 20, 30].map((h, i) => (
                    <div key={i} className={styles.waveBarClean} style={{ height: `${h}%` }} />
                  ))}
                </div>
              </div>
            </div>
            
            {/* Decorative background elements */}
            <div className={styles.glowOrb}></div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className="container">
          <p>© {new Date().getFullYear()} AudioSmith AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
