import styles from '@/styles/Section.module.css'
import {useEffect, useState} from "react";
import randomColor from "randomcolor";
import {Open_Sans, Rubik} from "next/font/google";

const font2 = Rubik({subsets: ['latin'], weight: "variable"})

export function Section({title, children }) {
    const [bgColor, setBgColor] = useState("#fff")

useEffect(() => {
    setBgColor(randomColor({
        luminosity: 'dark',
        format: 'rgba'
    }));
}, [])

    return (
    <section className={styles.section} style={{backgroundColor:bgColor}}>
        <h2>{title}</h2>
        <p className={font2.className}>{children}</p>
    </section>
    )
}