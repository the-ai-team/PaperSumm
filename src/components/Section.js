import styles from "@/styles/Section.module.css";
import { useEffect, useState } from "react";
import randomColor from "randomcolor";
import { Rubik } from "next/font/google";
import { useMantineColorScheme } from "@mantine/core";

const font2 = Rubik({ subsets: ["latin"], weight: "variable" });

export function Section({ title, diagrams, children }) {
  const [bgDarkColor, setBgDarkColor] = useState("rgb(69,69,69)");
  const [bgLightColor, setBgLightColor] = useState("rgb(239,239,239)"); // [1
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  useEffect(() => {
    setBgDarkColor(
      randomColor({
        luminosity: "dark",
        format: "rgba",
      })
    );
    setBgLightColor(
      randomColor({
        luminosity: "light",
        format: "rgb",
      })
    );
  }, []);

  return (
    <section
      className={styles.section}
      style={{
        backgroundColor: colorScheme === "dark" ? bgDarkColor : bgLightColor,
      }}
    >
      <h2>{title}</h2>
      <p className={font2.className}>{children}</p>
      {diagrams
        ? diagrams.map((diagram, index) => {
            return (
              <div key={index} className={styles.diagrams}>
                {diagram.image.map((figure, index) => (
                  <>
                    <img key={index} src={figure} alt={diagram.alt} />
                  </>
                ))}
                <p>{diagram.description}</p>
              </div>
            );
          })
        : null}
    </section>
  );
}
