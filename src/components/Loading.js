import styles from '@/styles/Loading.module.css'

export function Loading({show, text}) {
    return (
        <div className={styles.loading} data-visible={show}>
            <div className={styles.outer}>
                <div className={styles.inner}>
                </div>
            </div>
            <div className={styles.text}>{text}</div>
        </div>
    )
}