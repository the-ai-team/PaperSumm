import styles from '@/styles/Loading.module.css'

export function Loading() {
    return (
        <div className={styles.loading}>
            <div className={styles.outer}>
                <div className={styles.inner}>
                </div>
            </div>
            <div className={styles.text}>Loading...</div>
        </div>
    )
}