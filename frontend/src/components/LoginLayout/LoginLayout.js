import {Container, CssBaseline} from "@mui/material";

function LoginLayout({ children }) {
    return (
        <Container maxWidth="xxl" sx={{display: "flex", background: "linear-gradient(120grad, #e66465, #9198e5);", height: "100vh", p: 0}}>
            <CssBaseline />
            <Container maxWidth="xs" sx={{display: "flex", alignItems: 'center'}}>
                {children}
            </Container>
        </Container>
    )
}

export default LoginLayout