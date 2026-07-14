import React, { useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';
import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
import { Play, Pause } from 'lucide-react';
import styles from './WaveformPlayer.module.css';

interface WaveformPlayerProps {
  audioUrl: string;
  waveColor?: string;
  progressColor?: string;
  showSpectrogram?: boolean;
}

export function WaveformPlayer({
  audioUrl,
  waveColor = '#3b82f6',
  progressColor = '#1d4ed8',
  showSpectrogram = true,
}: WaveformPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const spectrogramRef = useRef<HTMLDivElement>(null);
  const wavesurferRef = useRef<WaveSurfer | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;

    const plugins = [];
    if (showSpectrogram && spectrogramRef.current) {
      plugins.push(
        Spectrogram.create({
          container: spectrogramRef.current,
          labels: true,
          height: 100,
          splitChannels: false,
        })
      );
    }

    const wavesurfer = WaveSurfer.create({
      container: containerRef.current,
      waveColor,
      progressColor,
      cursorColor: '#ef4444',
      barWidth: 2,
      barGap: 1,
      barRadius: 2,
      height: 80,
      plugins,
    });

    wavesurferRef.current = wavesurfer;

    wavesurfer.load(audioUrl);

    wavesurfer.on('ready', () => {
      setIsReady(true);
    });

    wavesurfer.on('play', () => setIsPlaying(true));
    wavesurfer.on('pause', () => setIsPlaying(false));
    wavesurfer.on('finish', () => setIsPlaying(false));

    return () => {
      wavesurfer.destroy();
    };
  }, [audioUrl, waveColor, progressColor, showSpectrogram]);

  const togglePlay = () => {
    if (wavesurferRef.current) {
      wavesurferRef.current.playPause();
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.controls}>
        <button
          className={styles.playButton}
          onClick={togglePlay}
          disabled={!isReady}
        >
          {isPlaying ? <Pause size={20} /> : <Play size={20} />}
        </button>
      </div>
      <div className={styles.visuals}>
        <div ref={containerRef} className={styles.waveform} />
        {showSpectrogram && <div ref={spectrogramRef} className={styles.spectrogram} />}
      </div>
    </div>
  );
}
