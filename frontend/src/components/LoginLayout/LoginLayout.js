import {Container, CssBaseline} from "@mui/material";
import {theme} from "./LoginLayout.styles"

function LoginLayout({ children }) {
    return (
        <Container sx={theme.bg}>
            <CssBaseline />
            <Container maxWidth="xs" sx={theme.formHolder}>
                {children}
            </Container>
        </Container>
    )
}

export default LoginLayout