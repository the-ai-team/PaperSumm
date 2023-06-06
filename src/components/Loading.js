import styles from '@/styles/Loading.module.css';
import { useEffect, useState } from 'react';

export function Loading({ show }) {
  const [loadingText, setLoadingText] = useState('Loading...');

  const loadingTexts = [
    'Extracting insights',
    'Synthesizing knowledge',
    "Unveiling paper's essence",
    'Crafting brilliance',
    'Distilling scholarly wisdom',
    'Unleashing research power',
    'Awaiting key findings',
    'Unlocking hidden gems',
    'Converting complexity',
    'Summarizing with precision',
  ];

  const appreciationTexts = [
    'Patience fuels knowledge!',
    'Thanks for understanding.',
    'Grateful for unraveling mysteries.',
    'Savoring research details!',
    'Fueling research passion.',
    'Value your time and trust.',
    'Trusting us on the journey.',
    'Commitment to excellence.',
    'Deciphering research tapestry.',
    'Grateful for research trust.',
  ];

  // make a timer changes the text every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * loadingTexts.length);
      const randomList = Math.floor(Math.random());
      if (randomList === 0) setLoadingText(appreciationTexts[randomIndex]);
      else setLoadingText(loadingTexts[randomIndex]);
    }, 5000);
    return () => clearInterval(interval);
  });

  useEffect(() => {
    setLoadingText('Loading...');
  }, [show]);

  return (
    <div className={styles.loading} data-visible={show}>
      <div className={styles.outer}>
        <div className={styles.inner}></div>
      </div>
      <div className={styles.text}>{loadingText}</div>
    </div>
  );
}
