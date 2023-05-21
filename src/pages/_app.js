import "@/styles/globals.css";
import { ColorSchemeProvider, MantineProvider } from "@mantine/core";
import { useEffect, useState } from "react";

export default function App({ Component, pageProps }) {
  const [colorScheme, setColorScheme] = useState("light");
  const toggleColorScheme = (value) =>
    setColorScheme(value || (colorScheme === "dark" ? "light" : "dark"));

  useEffect(() => {
    const localColorScheme = localStorage.getItem("colorScheme");
    setColorScheme(localColorScheme || "dark");
    document.documentElement.setAttribute(
      "data-theme",
      localColorScheme || "dark"
    );
  }, []);

  return (
    <>
      <ColorSchemeProvider
        colorScheme={colorScheme}
        toggleColorScheme={toggleColorScheme}
      >
        <MantineProvider
          withGlobalStyles
          withNormalizeCSS
          theme={{
            colorScheme,
          }}
        >
          <main>
            <Component {...pageProps} />
          </main>
        </MantineProvider>
      </ColorSchemeProvider>
    </>
  );
}
