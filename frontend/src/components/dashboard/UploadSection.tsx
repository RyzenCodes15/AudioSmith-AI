import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2 } from 'lucide-react';
import { FileUpload } from '../ui/FileUpload';
import { ApiClient } from '@/lib/api/client';
import styles from './UploadSection.module.css';

export function UploadSection({ onUploadComplete }: { onUploadComplete: () => void }) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  
  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setUploadSuccess(false);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await ApiClient.post('/uploads/upload', formData);
      setUploadSuccess(true);
      onUploadComplete();
      
      // Reset success state after a delay
      setTimeout(() => setUploadSuccess(false), 3000);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Upload Audio</h2>
      <p className={styles.subheading}>
        Upload a noisy audio file to begin the enhancement process.
      </p>
      
      <div className={styles.uploadArea}>
        <AnimatePresence mode="wait">
          {uploadSuccess ? (
            <motion.div
              key="success"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className={styles.successState}
            >
              <CheckCircle2 size={64} className={styles.successIcon} />
              <h3>Upload Successful!</h3>
              <p>Your audio is pending enhancement.</p>
            </motion.div>
          ) : (
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <FileUpload
                onUpload={handleUpload}
                isUploading={isUploading}
              />
              {isUploading && (
                <div className={styles.progressContainer}>
                  <div className={styles.progressBar}>
                    <motion.div 
                      className={styles.progressFill}
                      initial={{ width: "0%" }}
                      animate={{ width: "100%" }}
                      transition={{ duration: 15, ease: "easeOut" }} // Fake progress for UX
                    />
                  </div>
                  <span className={styles.progressText}>Uploading and processing metadata...</span>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
