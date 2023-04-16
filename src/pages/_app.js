import '@/styles/globals.css'
import {MantineProvider} from "@mantine/core";


export default function App({Component, pageProps}) {
    return (<>
        <MantineProvider
            withGlobalStyles
            withNormalizeCSS
            theme={{
                colorScheme: 'light',
            }}
        >
            <main>
                <Component {...pageProps} />
            </main>
        </MantineProvider>
    </>)
}
