import '../styles/globals.css'
import {createTheme} from "@mui/material/styles";
import {ThemeProvider} from "@mui/material";

function MyApp({ Component, pageProps }) {

  const theme = createTheme({
    palette: {
      primary: {
        main: '#747ab7'
      }
    },
  });

  return (
      <ThemeProvider theme={theme}>
        <Component {...pageProps} />
      </ThemeProvider>
  )
}

export default MyApp
