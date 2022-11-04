import {Box, Button, Container, CssBaseline, Grid, TextField, ThemeProvider, Typography} from "@mui/material"
import { Link as MUILink } from '@mui/material';
import Link from "next/link";
import { createTheme } from '@mui/material/styles';

function Login() {
    const theme = createTheme({
        palette: {
            primary: {
                main: '#747ab7'
            }
        },
    });

    return (
        <>
            <ThemeProvider theme={theme}>
                <Container maxWidth="xxl" sx={{display: "flex", background: "linear-gradient(120grad, #e66465, #9198e5);", height: "100vh", p: 0}}>
                    <CssBaseline />
                    <Container maxWidth="xs">
                        <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                mt: 8,
                                p: 4,
                                border: '1px solid #C0C0C0',
                                boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                borderRadius: '12px',
                                backgroundColor: 'white'
                            }}
                        >
                            <Typography component="h1" variant="h4" fontWeight="700">
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


                                <Grid item xs>
                                    <Link href="/">
                                        <MUILink href="#" variant="body2">
                                            Kontakt na administrátora.
                                        </MUILink>
                                    </Link>
                                </Grid>
                            </Box>
                        </Box>
                    </Container>
                </Container>
            </ThemeProvider>
        </>
    )
}

export default Login