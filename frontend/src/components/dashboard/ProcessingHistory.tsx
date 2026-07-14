import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FileAudio, Clock, Activity, HardDrive } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { ApiClient } from '@/lib/api/client';
import styles from './ProcessingHistory.module.css';

interface AudioUpload {
  id: string;
  filename: string;
  file_size_bytes: number;
  duration_seconds: number;
  status: string;
  uploaded_at: string;
}

export function ProcessingHistory({ refreshTrigger }: { refreshTrigger: number }) {
  const router = useRouter();
  const [uploads, setUploads] = useState<AudioUpload[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isSubscribed = true;
    let timeoutId: NodeJS.Timeout;

    const fetchHistory = async (isInitial = false) => {
      try {
        if (isInitial) setLoading(true);
        const data = await ApiClient.get<AudioUpload[]>('/uploads');
        
        if (!isSubscribed) return;
        
        setUploads(prev => {
          if (prev.length > 0 && !isInitial) {
            const newlyCompleted = data.find(d => 
              d.status === 'completed' && 
              prev.some(p => p.id === d.id && p.status !== 'completed')
            );
            if (newlyCompleted) {
              router.push(`/results/${newlyCompleted.id}`);
            }
          }
          return data;
        });

        const hasPending = data.some(d => d.status === 'pending' || d.status === 'processing');
        if (hasPending && isSubscribed) {
          timeoutId = setTimeout(() => fetchHistory(false), 3000);
        }
      } catch (err) {
        const error = err as Error;
        if (isSubscribed) setError(error.message || 'Failed to load history');
      } finally {
        if (isSubscribed && isInitial) setLoading(false);
      }
    };

    fetchHistory(true);

    return () => {
      isSubscribed = false;
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [refreshTrigger, router]);

  const formatSize = (bytes: number) => {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const formatDuration = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  if (loading && uploads.length === 0) {
    return <div className={styles.loading}>Loading history...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (uploads.length === 0) {
    return (
      <div className={styles.empty}>
        <FileAudio size={48} className={styles.emptyIcon} />
        <p>No audio files uploaded yet.</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Processing History</h2>
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Filename</th>
              <th>Status</th>
              <th>Duration</th>
              <th>Size</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {uploads.map((upload, index) => (
              <motion.tr 
                key={upload.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => router.push(`/results/${upload.id}`)}
                className={styles.clickableRow}
                style={{ cursor: 'pointer' }}
              >
                <td>
                  <div className={styles.filenameCell}>
                    <FileAudio size={16} />
                    <span>{upload.filename}</span>
                  </div>
                </td>
                <td>
                  <span className={`badge badge-${upload.status}`}>
                    {upload.status === 'pending' && <Activity size={12} style={{ marginRight: '4px' }} />}
                    {upload.status === 'processing' && <Activity size={12} style={{ marginRight: '4px' }} />}
                    {upload.status.charAt(0).toUpperCase() + upload.status.slice(1)}
                  </span>
                </td>
                <td>
                  <div className={styles.metaCell}>
                    <Clock size={14} />
                    <span>{formatDuration(upload.duration_seconds)}</span>
                  </div>
                </td>
                <td>
                  <div className={styles.metaCell}>
                    <HardDrive size={14} />
                    <span>{formatSize(upload.file_size_bytes)}</span>
                  </div>
                </td>
                <td>{new Date(upload.uploaded_at).toLocaleDateString()}</td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
