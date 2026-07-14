import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileAudio, Clock, Activity, HardDrive, Trash2, Download, ExternalLink } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { ApiClient } from '@/lib/api/client';
import { useToast } from '@/lib/ToastContext';
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
  const { showToast } = useToast();
  const [uploads, setUploads] = useState<AudioUpload[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [isDeleting, setIsDeleting] = useState(false);

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
            // We can choose not to auto-redirect from history, but let's keep it if processing
            if (newlyCompleted) {
              // Only redirect if this is the only thing we are looking at (maybe too aggressive)
              // Let's remove auto-redirect from the history to prevent stealing focus when bulk managing
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

  const toggleSelection = (id: string) => {
    setSelectedIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAll = () => {
    if (selectedIds.size === uploads.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(uploads.map(u => u.id)));
    }
  };

  const deleteSelected = async () => {
    if (selectedIds.size === 0) return;
    if (!confirm(`Are you sure you want to delete ${selectedIds.size} files?`)) return;

    setIsDeleting(true);
    try {
      await Promise.all(
        Array.from(selectedIds).map(id => ApiClient.delete(`/uploads/${id}`))
      );
      
      setUploads(prev => prev.filter(u => !selectedIds.has(u.id)));
      showToast(`Successfully deleted ${selectedIds.size} files`, 'success');
      setSelectedIds(new Set());
    } catch (e) {
      showToast('Failed to delete some files. They may already be removed.', 'error');
      // Refresh to get actual state
      const data = await ApiClient.get<AudioUpload[]>('/uploads').catch(() => []);
      setUploads(data);
      setSelectedIds(new Set());
    } finally {
      setIsDeleting(false);
    }
  };

  const deleteSingle = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this file?')) return;
    try {
      await ApiClient.delete(`/uploads/${id}`);
      setUploads(prev => prev.filter(u => u.id !== id));
      showToast('File deleted successfully', 'success');
      setSelectedIds(prev => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    } catch (err) {
      showToast('Failed to delete file', 'error');
    }
  };

  const downloadSingle = async (e: React.MouseEvent, id: string, filename: string) => {
    e.stopPropagation();
    try {
      const blob = await ApiClient.getBlob(`/uploads/${id}/download`);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      showToast('Failed to download file', 'error');
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
      <div className={styles.header}>
        <h2 className={styles.heading}>Processing History</h2>
        
        <AnimatePresence>
          {selectedIds.size > 0 && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={styles.actionBar}
            >
              <span className={styles.selectedCount}>{selectedIds.size} selected</span>
              <button 
                className={styles.bulkDeleteBtn} 
                onClick={deleteSelected}
                disabled={isDeleting}
              >
                <Trash2 size={16} /> 
                {isDeleting ? 'Deleting...' : 'Delete Selected'}
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th className={styles.checkboxCol}>
                <input 
                  type="checkbox" 
                  checked={uploads.length > 0 && selectedIds.size === uploads.length}
                  onChange={toggleAll}
                  className={styles.checkbox}
                />
              </th>
              <th>Filename</th>
              <th>Status</th>
              <th>Duration</th>
              <th>Size</th>
              <th>Date</th>
              <th className={styles.actionsCol}>Actions</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence>
              {uploads.map((upload, index) => (
                <motion.tr 
                  key={upload.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ delay: index * 0.02 }}
                  onClick={() => router.push(`/results/${upload.id}`)}
                  className={`${styles.clickableRow} ${selectedIds.has(upload.id) ? styles.selectedRow : ''}`}
                >
                  <td className={styles.checkboxCol} onClick={(e) => e.stopPropagation()}>
                    <input 
                      type="checkbox" 
                      checked={selectedIds.has(upload.id)}
                      onChange={() => toggleSelection(upload.id)}
                      className={styles.checkbox}
                    />
                  </td>
                  <td>
                    <div className={styles.filenameCell}>
                      <FileAudio size={16} />
                      <span className={styles.truncate}>{upload.filename}</span>
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
                  <td className={styles.actionsCol} onClick={(e) => e.stopPropagation()}>
                    <div className={styles.rowActions}>
                      <button 
                        onClick={() => router.push(`/results/${upload.id}`)}
                        className={styles.iconBtn}
                        title="Open Result"
                      >
                        <ExternalLink size={16} />
                      </button>
                      {upload.status === 'completed' && (
                        <button 
                          onClick={(e) => downloadSingle(e, upload.id, upload.filename)}
                          className={styles.iconBtn}
                          title="Download Original"
                        >
                          <Download size={16} />
                        </button>
                      )}
                      <button 
                        onClick={(e) => deleteSingle(e, upload.id)}
                        className={`${styles.iconBtn} ${styles.iconBtnDanger}`}
                        title="Delete"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>
    </div>
  );
}
