import Head from 'next/head';
import { notifications } from '@mantine/notifications';
import styles from '@/styles/Home.module.css';
import {
  ActionIcon,
  Button,
  createStyles,
  Input,
  MultiSelect,
  useMantineColorScheme,
} from '@mantine/core';
import {
  CaretCircleUp,
  MagnifyingGlass,
  Moon,
  Sun,
  Warning,
} from '@phosphor-icons/react';
import { Loading } from '@/components/Loading';
import { Inter, Roboto_Mono } from 'next/font/google';
import { Section } from '@/components/Section';
import { useEffect, useState, useMemo, useRef, useCallback } from 'react';
import logo from '@/assets/logo.png';
import Image from 'next/image';
import { eventSource, fetchAPI } from '@/utils/fetchAPI';

const font = Roboto_Mono({ subsets: ['latin'], weight: ['300', '500'] });
const font2 = Inter({ subsets: ['latin'], weight: 'variable' });

const useStyles = createStyles((theme) => ({
  label: {
    fontFamily: font.style.fontFamily,
    marginBottom: '0.5em',
  },
  input: {
    fontFamily: font.style.fontFamily,
  },
  dropdown: {
    fontFamily: font.style.fontFamily,
    borderRadius: '1rem',
    padding: '2rem',
  },
  item: {
    fontFamily: font.style.fontFamily,
    borderRadius: '1rem',
    fontSize: '.875rem',
    padding: '0.5rem 1rem',
  },
  defaultValueLabel: {
    fontFamily: font.style.fontFamily,
  },
  nothingFound: {
    fontFamily: font.style.fontFamily,
  },
}));

export default function Home() {
  const { classes } = useStyles();

  const SummaryStateEnum = useMemo(() => {
    return {
      hidden: 'hidden',
      loading: 'loading',
      success: 'success',
      error: 'error',
    };
  }, []);

  const [summaryState, setSummaryState] = useState(SummaryStateEnum.hidden);
  const [link, setLink] = useState('');
  const [tag, setTag] = useState([]);
  const [inputValid, setInputValid] = useState(false);
  const [isSearchExpanded, toggleSearchExpanded] = useState(true);

  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  function toggleScheme() {
    toggleColorScheme();
    document.documentElement.setAttribute(
      'data-theme',
      colorScheme === 'dark' ? 'light' : 'dark'
    );
    localStorage.setItem(
      'colorScheme',
      colorScheme === 'dark' ? 'light' : 'dark'
    );
  }

  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const regex = new RegExp(
      '^(https?://)?(www.)?(arxiv.org/abs/)[a-zA-Z0-9]{4,9}.[a-zA-Z0-9]{4,9}$'
    );

    if (regex.test(link) && tag.length > 0) {
      setInputValid(true);
    } else {
      setInputValid(false);
    }
  }, [link, tag]);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 1800) {
        document.documentElement.style.setProperty('--window-padding', '2rem');
        document.documentElement.style.setProperty(
          '--container-border-radius',
          '40px'
        );
      }
    };
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const tags = [
    { value: 'experiments and results', label: 'Experiments and Results' },
    { value: 'proposed solution', label: 'Proposed Solution' },
    {
      value: 'building blocks and methodology',
      label: 'Building Blocks and Methodology',
    },
  ];

  useEffect(() => {
    let timeoutFunction;
    clearTimeout(timeoutFunction);

    if (summary) {
      setSummaryState(SummaryStateEnum.success);
    }

    if (error) {
      setSummaryState(SummaryStateEnum.error);
      toggleSearchExpanded(true);
      notifications.show({
        title: 'Error',
        message: error,
        color: 'red',
        icon: <Warning />,
        autoClose: 8000,
      });
      timeoutFunction = setTimeout(() => {
        setError('');
      }, 8000);
    }

    return () => {
      clearTimeout(timeoutFunction);
    };
  }, [SummaryStateEnum, summary, error]);

  useEffect(() => {
    switch (summaryState) {
      case SummaryStateEnum.success:
        toggleSearchExpanded(false);
        break;

      case SummaryStateEnum.error:
        toggleSearchExpanded(true);

      default:
        break;
    }
  }, [SummaryStateEnum, summaryState]);

  const summarize = () => {
    if (eventSource) {
      // console.log('closing event source');
      eventSource.close();
    }
    setSummary(null);
    setSummaryState(SummaryStateEnum.loading);
    setError('');

    if (!link || !tag) {
      console.log('link or tag is empty', link, tag);
      return;
    }

    fetchAPI({
      url: link,
      keyword: tag,
      updateSummary: (summary) => setSummary(summary),
      setError: (error) => setError(error),
    });
  };

  useEffect(() => {
    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, []);

  return (
    <>
      <Head>
        <title>PaperSumm</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main
        className={styles.main}
        data-summary-state={summaryState}
        style={{ fontFamily: font.style.fontFamily }}
      >
        <div
          className={styles.container}
          data-summary-state={summaryState}
          data-expanded={isSearchExpanded}
        >
          <div
            className={styles.expandable}
            data-summary-state={summaryState}
            aria-expanded={isSearchExpanded}
          >
            <div
              className={styles.logo_content}
              data-summary-state={summaryState}
            >
              <Image
                src={logo}
                data-summary-state={summaryState}
                placeholder="blur"
                alt="logo"
                className={styles.logo}
                onClick={() => {
                  setSummaryState(SummaryStateEnum.hidden);
                  toggleSearchExpanded(true);
                }}
              ></Image>
              <h2
                className={styles.title}
                data-summary-state={summaryState}
                style={{ fontFamily: font2.style.fontFamily }}
              >
                {summaryState === SummaryStateEnum.hidden ? (
                  <>
                    We <span>summ</span>arize <br /> your Arxiv{' '}
                    <span>Paper</span>
                  </>
                ) : (
                  <span
                    onClick={() => {
                      setSummaryState(SummaryStateEnum.hidden);
                      toggleSearchExpanded(true);
                    }}
                    className={styles.productName}
                  >
                    PaperSumm
                  </span>
                )}
              </h2>
              <ActionIcon
                size="lg"
                radius="xl"
                color={colorScheme === 'dark' ? 'gray' : 'blue'}
                variant={colorScheme === 'dark' ? 'filled' : 'light'}
                onClick={toggleScheme}
                className={styles.themeSwitcher}
                data-expanded={isSearchExpanded}
                data-summary-state={summaryState}
              >
                {colorScheme === 'dark' ? (
                  <Sun size={24} color="#1994fb" weight="light" />
                ) : (
                  <Moon size={24} color="#1994fb" weight="light" />
                )}
              </ActionIcon>
            </div>
            <div className={styles.inputs} data-summary-state={summaryState}>
              <Input.Wrapper
                label="Input arxiv URL to Research Paper"
                className={styles.input_box}
                classNames={{ label: classes.label }}
                size="md"
              >
                <Input
                  icon={
                    <MagnifyingGlass size={24} color="#1994fb" weight="light" />
                  }
                  placeholder="https://arxiv.org/abs/1512.03385"
                  radius="xl"
                  size="md"
                  value={link}
                  onChange={(event) => {
                    setLink(event.target.value);
                  }}
                  classNames={{ input: classes.input }}
                />
              </Input.Wrapper>
              <MultiSelect
                data={tags}
                label="Select a tag"
                searchable
                clearable
                radius="xl"
                size="md"
                value={tag}
                onChange={(value) => {
                  setTag(value);
                }}
                nothingFound="No tags found"
                classNames={{
                  label: classes.label,
                  dropdown: classes.dropdown,
                  item: classes.item,
                  defaultValueLabel: classes.defaultValueLabel,
                  nothingFound: classes.nothingFound,
                }}
              />
              <div className={styles.buttons} data-summary-state={summaryState}>
                <Button
                  radius="xl"
                  size="md"
                  className={styles.button}
                  onClick={summarize}
                  style={{ fontFamily: font.style.fontFamily }}
                  disabled={!inputValid}
                >
                  Summarize
                </Button>
              </div>
              <h5 className={styles.credits} data-summary-state={summaryState}>
                Product by the AI Team
              </h5>
            </div>
          </div>
          <ActionIcon
            size="lg"
            radius="xl"
            onClick={() => {
              toggleSearchExpanded(!isSearchExpanded);
              console.log(!isSearchExpanded);
            }}
            color={colorScheme === 'dark' ? 'gray' : 'blue'}
            variant={colorScheme === 'dark' ? 'filled' : 'light'}
            className={styles.expandIcon}
            data-expanded={isSearchExpanded}
            data-summary-state={summaryState}
          >
            <CaretCircleUp size={24} color="#1994fb" weight="light" />
          </ActionIcon>
          <div className={styles.output}>
            <Loading show={summaryState === SummaryStateEnum.loading} />
            <div className={styles.content} data-summary-state={summaryState}>
              <div
                className={styles.filler}
                data-summary-state={summaryState}
              ></div>
              <div className={styles.summary} data-summary-state={summaryState}>
                {summary?.valid
                  ? summary.value.map((section, index) => {
                      let diagrams = [];

                      // TODO: needs to remove this, from server side it must send a list of diagrams it self.
                      if (section.diagrams) {
                        diagrams = [
                          {
                            type: section.diagrams.type,
                            figures: section.diagrams.figure,
                            alt: section.title,
                            description: section.diagrams.description,
                            index,
                          },
                        ];
                      }

                      return (
                        <>
                          <Section
                            key={index}
                            title={section.title}
                            diagrams={diagrams}
                          >
                            {section.content}
                          </Section>
                        </>
                      );
                    })
                  : null}
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
