import {Box, Button, Container, CssBaseline, TextField, Typography} from "@mui/material";

function Login() {

    return (
        <>
            <CssBaseline />
            <Container maxWidth={"xs"}>

                <Box sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        mt: 12,
                        p: 4,
                        border: '1px solid #C0C0C0',
                        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                        borderRadius: '12px'
                    }}
                >
                    <Typography component="h1" variant="h4" textAlign="center">
                        Prihlásenie
                    </Typography>

                    <Box component="form"  noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email"
                            name="email"
                            autoComplete="email"
                            autoFocus
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Heslo"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                           Prihlásiť sa
                        </Button>
                    </Box>
                </Box>



            </Container>
        </>
    )
}

export default Login