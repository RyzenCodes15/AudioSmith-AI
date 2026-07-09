'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ApiClient } from '@/lib/api/client';
import { useAuth } from '@/lib/auth/AuthContext';
import Link from 'next/link';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import styles from './AuthForm.module.css';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      const response = await ApiClient.post<{access_token: string; refresh_token: string}>('/auth/login', {
        email,
        password,
      });
      await login(response.access_token, response.refresh_token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid credentials. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.formContainer}>
      {error && <div className={styles.errorBanner}>{error}</div>}
      
      <div className={styles.inputGroup}>
        <label className={styles.label} htmlFor="email">Email address</label>
        <div className={styles.inputWrapper}>
          <input 
            id="email"
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={styles.input}
            placeholder="name@company.com"
            required
            disabled={isLoading}
          />
        </div>
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label} htmlFor="password">Password</label>
        <div className={styles.inputWrapper}>
          <input 
            id="password"
            type={showPassword ? "text" : "password"} 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.input}
            placeholder="••••••••"
            required
            disabled={isLoading}
          />
          <button 
            type="button"
            className={styles.inputIconBtn}
            onClick={() => setShowPassword(!showPassword)}
            tabIndex={-1}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      <div className={styles.optionsRow}>
        <label className={styles.checkboxLabel}>
          <input 
            type="checkbox" 
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            disabled={isLoading}
          />
          Remember me for 30 days
        </label>
      </div>

      <button 
        type="submit" 
        disabled={isLoading}
        className={styles.submitBtn}
      >
        {isLoading ? (
          <>
            <div className={styles.spinner}></div>
            Signing in...
          </>
        ) : (
          <>
            <LogIn size={20} />
            Sign In
          </>
        )}
      </button>

      <p className={styles.footerText}>
        Don't have an account? <Link href="/register" className={styles.footerLink}>Create account</Link>
      </p>
    </form>
  );
}
