import '../styles/globals.css'
import {ThemeProvider} from "@mui/material";
import {CacheProvider} from "@emotion/react";
import createEmotionCache from "../utils/createEmotionCache";
import {theme} from "../styles/styles"

const clientSideEmotionCache = createEmotionCache();

function MyApp({ Component, emotionCache = clientSideEmotionCache, pageProps }) {

  return (
      <CacheProvider value={emotionCache}>
        <ThemeProvider theme={theme}>
          <Component {...pageProps} />
        </ThemeProvider>
      </CacheProvider>
  )
}

export default MyApp
