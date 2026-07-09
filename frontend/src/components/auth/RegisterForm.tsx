'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ApiClient } from '@/lib/api/client';
import { useAuth } from '@/lib/auth/AuthContext';
import Link from 'next/link';
import { Eye, EyeOff, UserPlus } from 'lucide-react';
import styles from './AuthForm.module.css';

export function RegisterForm() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // 1. Register
      await ApiClient.post('/auth/register', {
        full_name: fullName,
        email,
        password,
      });
      
      // 2. Auto-login after registration
      const response = await ApiClient.post<{access_token: string; refresh_token: string}>('/auth/login', {
        email,
        password,
      });
      
      await login(response.access_token, response.refresh_token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.formContainer}>
      {error && <div className={styles.errorBanner}>{error}</div>}
      
      <div className={styles.inputGroup}>
        <label className={styles.label} htmlFor="full_name">Full Name</label>
        <div className={styles.inputWrapper}>
          <input 
            id="full_name"
            type="text" 
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className={styles.input}
            placeholder="Jane Doe"
            required
            disabled={isLoading}
          />
        </div>
      </div>

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
            minLength={8}
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
        <p className={styles.helperText}>Must be at least 8 characters</p>
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label} htmlFor="confirm_password">Confirm Password</label>
        <div className={styles.inputWrapper}>
          <input 
            id="confirm_password"
            type={showPassword ? "text" : "password"} 
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={styles.input}
            placeholder="••••••••"
            minLength={8}
            required
            disabled={isLoading}
          />
        </div>
      </div>

      <button 
        type="submit" 
        disabled={isLoading}
        className={styles.submitBtn}
      >
        {isLoading ? (
          <>
            <div className={styles.spinner}></div>
            Creating account...
          </>
        ) : (
          <>
            <UserPlus size={20} />
            Create Account
          </>
        )}
      </button>

      <p className={styles.footerText}>
        Already have an account? <Link href="/login" className={styles.footerLink}>Sign in</Link>
      </p>
    </form>
  );
}
