import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { UploadCloud, X, AlertCircle } from 'lucide-react';
import styles from './FileUpload.module.css';

interface FileUploadProps {
  onUpload: (file: File) => Promise<void>;
  maxSizeMB?: number;
  allowedExtensions?: string[];
  isUploading?: boolean;
}

export function FileUpload({
  onUpload,
  maxSizeMB = 50,
  allowedExtensions = ['.wav', '.mp3', '.flac'],
  isUploading = false,
}: FileUploadProps) {
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    async (acceptedFiles: File[], fileRejections: { errors: { code: string; message: string }[] }[]) => {
      setError(null);
      
      if (fileRejections.length > 0) {
        const rejection = fileRejections[0];
        if (rejection.errors[0]?.code === 'file-too-large') {
          setError(`File is too large. Maximum size is ${maxSizeMB}MB.`);
        } else if (rejection.errors[0]?.code === 'file-invalid-type') {
          setError(`Unsupported file type. Please upload ${allowedExtensions.join(', ')}.`);
        } else {
          setError(rejection.errors[0]?.message || 'Invalid file.');
        }
        return;
      }

      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        try {
          await onUpload(file);
        } catch (err) {
          const error = err as Error;
          setError(error.message || 'Upload failed. Please try again.');
        }
      }
    },
    [onUpload, maxSizeMB, allowedExtensions]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/wav': ['.wav'],
      'audio/mpeg': ['.mp3'],
      'audio/flac': ['.flac'],
    },
    maxSize: maxSizeMB * 1024 * 1024,
    multiple: false,
    disabled: isUploading,
  });

  return (
    <div className={styles.wrapper}>
      <div
        {...getRootProps()}
        className={`${styles.dropzone} ${isDragActive ? styles.active : ''} ${
          isUploading ? styles.disabled : ''
        }`}
      >
        <input {...getInputProps()} />
        <div className={styles.content}>
          <div className={styles.iconWrapper}>
            <UploadCloud size={48} className={styles.icon} />
          </div>
          <h3 className={styles.title}>
            {isDragActive ? 'Drop audio here' : 'Drag & drop audio'}
          </h3>
          <p className={styles.subtitle}>
            or click to browse from your computer
          </p>
          <div className={styles.limits}>
            <span>Supported: {allowedExtensions.join(', ')}</span>
            <span>Max size: {maxSizeMB}MB</span>
          </div>
        </div>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className={styles.error}
        >
          <AlertCircle size={16} />
          <span>{error}</span>
          <button onClick={() => setError(null)} className={styles.closeError}>
            <X size={16} />
          </button>
        </motion.div>
      )}
    </div>
  );
}
