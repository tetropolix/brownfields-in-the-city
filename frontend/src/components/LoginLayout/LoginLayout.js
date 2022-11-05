import {Container, CssBaseline, ThemeProvider} from "@mui/material";
import {createTheme} from "@mui/material/styles";


const theme = createTheme({
    palette: {
        primary: {
            main: '#747ab7'
        }
    },
});

function LoginLayout({ children }) {
    return (
        <ThemeProvider theme={theme}>
            <Container maxWidth="xxl" sx={{display: "flex", background: "linear-gradient(120grad, #e66465, #9198e5);", height: "100vh", p: 0}}>
                <CssBaseline />
                <Container maxWidth="xs" sx={{display: "flex", alignItems: 'center'}}>
                    {children}
                </Container>
            </Container>
        </ThemeProvider>
    )
}

export default LoginLayout