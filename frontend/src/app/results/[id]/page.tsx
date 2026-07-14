'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { Logo } from '@/components/common/Logo';
import { ApiClient } from '@/lib/api/client';
import { motion } from 'framer-motion';
import { ArrowLeft, CheckCircle, Headphones, Waves, Download, Activity, Trash2, Loader2, XCircle } from 'lucide-react';
import { WaveformPlayer } from '@/components/ui/WaveformPlayer';
import styles from './page.module.css';

interface AudioMetadata {
  id: string;
  filename: string;
  file_size_bytes: number;
  duration_seconds: number;
  sample_rate: number;
  format: string;
  status: string;
  uploaded_at: string;
  enhanced_file_id?: string;
}

export default function ResultsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  
  const [data, setData] = useState<AudioMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  const [enhancedUrl, setEnhancedUrl] = useState<string | null>(null);

  // Cleanup object URLs on unmount to prevent memory leaks
  useEffect(() => {
    return () => {
      if (originalUrl) URL.revokeObjectURL(originalUrl);
      if (enhancedUrl) URL.revokeObjectURL(enhancedUrl);
    };
  }, [originalUrl, enhancedUrl]);

  useEffect(() => {
    let isSubscribed = true;
    let timeoutId: NodeJS.Timeout;

    const fetchResult = async () => {
      try {
        const metadata = await ApiClient.get<AudioMetadata>(`/uploads/${id}`);
        if (!isSubscribed) return;
        
        setData(metadata);

        if (metadata.status === 'pending' || metadata.status === 'processing') {
          // Poll every 2 seconds
          timeoutId = setTimeout(() => fetchResult(), 2000);
          setLoading(false);
          return;
        }

        if (metadata.status === 'failed') {
          setLoading(false);
          return;
        }
        
        // Fetch audio files concurrently if completed
        if (metadata.status === 'completed' && !originalUrl) {
          try {
            const [origBlob, enhBlob] = await Promise.all([
              ApiClient.getBlob(`/uploads/${metadata.id}/download`),
              metadata.enhanced_file_id 
                ? ApiClient.getBlob(`/uploads/${metadata.enhanced_file_id}/download`)
                : Promise.reject('No enhanced file ID')
            ]);
            
            if (isSubscribed) {
              setOriginalUrl(URL.createObjectURL(origBlob));
              setEnhancedUrl(URL.createObjectURL(enhBlob));
            }
          } catch (blobErr) {
            console.error('Failed to fetch audio blobs:', blobErr);
            if (isSubscribed) setError('Failed to load audio files. They may have been deleted.');
          }
        }
      } catch (err) {
        const e = err as Error;
        if (isSubscribed) setError(e.message || 'Failed to fetch results.');
      } finally {
        if (isSubscribed) setLoading(false);
      }
    };
    
    fetchResult();

    return () => {
      isSubscribed = false;
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [id, originalUrl]);

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this result?')) {
      try {
        await ApiClient.delete(`/uploads/${id}`);
        router.push('/dashboard');
      } catch (e) {
        alert('Failed to delete.');
      }
    }
  };

  const formatSize = (bytes: number) => {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const formatDuration = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  if (loading && !data) {
    return (
      <ProtectedRoute>
        <div className={styles.resultsWrapper}>
          <div className={styles.loading}>
            <Loader2 className={styles.spinner} size={48} />
            <p>Loading results...</p>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  if (error || !data) {
    return (
      <ProtectedRoute>
        <div className={styles.resultsWrapper}>
          <div className="container" style={{ padding: '3rem 0' }}>
            <div className={styles.error}>{error || 'Result not found.'}</div>
            <div style={{ textAlign: 'center', marginTop: '2rem' }}>
              <button onClick={() => router.push('/dashboard')} className={styles.backBtn}>
                <ArrowLeft size={18} /> Back to Dashboard
              </button>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className={styles.resultsWrapper}>
        <header className={styles.header}>
          <div className={`container ${styles.headerContent}`}>
            <Logo />
            <button onClick={() => router.push('/dashboard')} className={styles.backBtn}>
              <ArrowLeft size={18} />
              <span>Back to Dashboard</span>
            </button>
          </div>
        </header>

        <main className={styles.mainContent}>
          <div className="container">
            {/* Status Section */}
            {data.status === 'completed' && (
              <motion.div 
                className={styles.successSection}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4 }}
              >
                <div className={styles.iconWrapper}>
                  <CheckCircle size={64} />
                </div>
                <h1 className={styles.title}>Enhancement Complete!</h1>
                <p className={styles.subtitle}>
                  Your audio file <strong>{data.filename}</strong> has been successfully processed by the AI.
                </p>
                
                <div className={styles.actionButtons}>
                  <button onClick={() => router.push('/dashboard')} className={styles.primaryBtn}>
                    Process Another File
                  </button>
                  <button onClick={handleDelete} className={styles.deleteBtn}>
                    <Trash2 size={16} /> Delete Result
                  </button>
                </div>
              </motion.div>
            )}

            {(data.status === 'pending' || data.status === 'processing') && (
              <motion.div 
                className={styles.processingSection}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div className={styles.iconWrapperProcessing}>
                  <Activity size={64} className={styles.pulseIcon} />
                </div>
                <h1 className={styles.title}>AI is working its magic...</h1>
                <p className={styles.subtitle}>
                  Current Status: <strong>{data.status.toUpperCase()}</strong>
                </p>
                <p className={styles.helperText}>This usually takes just a moment. Please wait...</p>
              </motion.div>
            )}

            {data.status === 'failed' && (
              <motion.div 
                className={styles.failedSection}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div className={styles.iconWrapperFailed}>
                  <XCircle size={64} />
                </div>
                <h1 className={styles.title}>Processing Failed</h1>
                <p className={styles.subtitle}>
                  We encountered an error while processing <strong>{data.filename}</strong>.
                </p>
                <div className={styles.actionButtons}>
                  <button onClick={() => router.push('/dashboard')} className={styles.primaryBtn}>
                    Try Another File
                  </button>
                  <button onClick={handleDelete} className={styles.deleteBtn}>
                    <Trash2 size={16} /> Delete Result
                  </button>
                </div>
              </motion.div>
            )}

            {/* Audio Visualization Section */}
            {data.status === 'completed' && (
              <motion.div 
                className={styles.audioSection}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
              >
                <div className={styles.audioCard}>
                  <div className={styles.cardHeader}>
                    <Waves size={24} color="var(--text-secondary)" />
                    <h2 className={styles.cardTitle}>Original Audio</h2>
                    {originalUrl && (
                      <a href={originalUrl} download={data.filename} className={styles.downloadBtn}>
                        <Download size={18} /> Download Original
                      </a>
                    )}
                  </div>
                  {originalUrl ? (
                    <WaveformPlayer 
                      audioUrl={originalUrl} 
                      waveColor="#9ca3af" 
                      progressColor="#4b5563"
                    />
                  ) : (
                    <div className={styles.loadingAudio}>Loading original audio...</div>
                  )}
                  <div className={styles.stats}>
                    <span>{formatSize(data.file_size_bytes)}</span>
                    <span>{data.format.toUpperCase()}</span>
                    <span>{data.sample_rate} Hz</span>
                    <span>{formatDuration(data.duration_seconds)}</span>
                  </div>
                </div>

                <div className={styles.audioCard}>
                  <div className={styles.cardHeader}>
                    <Headphones size={24} color="var(--primary)" />
                    <h2 className={styles.cardTitle}>Enhanced Audio</h2>
                    {enhancedUrl && (
                      <a href={enhancedUrl} download={`enhanced_${data.filename.replace(/\.[^/.]+$/, "")}.wav`} className={styles.downloadBtnPrimary}>
                        <Download size={18} /> Download Enhanced
                      </a>
                    )}
                  </div>
                  {enhancedUrl ? (
                    <WaveformPlayer 
                      audioUrl={enhancedUrl} 
                      waveColor="#3b82f6" 
                      progressColor="#1d4ed8"
                    />
                  ) : data.enhanced_file_id ? (
                    <div className={styles.loadingAudio}>Loading enhanced audio...</div>
                  ) : null}
                  <div className={styles.stats}>
                    {data.enhanced_file_id ? (
                      <>
                        <span>WAV</span>
                        <span>48000 Hz</span>
                        <span>{formatDuration(data.duration_seconds)}</span>
                      </>
                    ) : (
                      <span>Processing failed or incomplete</span>
                    )}
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
