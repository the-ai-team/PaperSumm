import styles from '@/styles/Section.module.css';
import { useEffect, useState } from 'react';
import randomColor from 'randomcolor';
import { Rubik } from 'next/font/google';
import { useMantineColorScheme } from '@mantine/core';
import Image from 'next/image';

const font2 = Rubik({ subsets: ['latin'], weight: 'variable' });

export function Section({ title, diagrams, children }) {
  const [bgDarkColor, setBgDarkColor] = useState('rgb(69,69,69)');
  const [bgLightColor, setBgLightColor] = useState('rgb(239,239,239)');
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  useEffect(() => {
    setBgDarkColor(
      randomColor({
        luminosity: 'dark',
        format: 'rgba',
      })
    );
    setBgLightColor(
      randomColor({
        luminosity: 'light',
        format: 'rgb',
      })
    );
  }, []);

  if (!title && (!children || children.trim() === '')) {
    return null;
  }

  // console.log('diagrams', diagrams);

  return (
    <section
      className={styles.section}
      style={{
        backgroundColor: colorScheme === 'dark' ? bgDarkColor : bgLightColor,
      }}
    >
      <h2>{title}</h2>
      <p className={font2.className}>{children}</p>
      {diagrams
        ? diagrams.map((diagram, index) => {
            if (!diagram || diagram.type != 'img') {
              return null;
            }

            return (
              <div key={index} className={styles.diagrams}>
                {diagram?.figures
                  ? diagram.figures.map((figure, index) => (
                      <>
                        <img
                          key={index}
                          src={figure}
                          alt={diagram.alt}
                          className={styles.image}
                        />
                      </>
                    ))
                  : null}
                <p>{diagram.description}</p>
              </div>
            );
          })
        : null}
    </section>
  );
}
