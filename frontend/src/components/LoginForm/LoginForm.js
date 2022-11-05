import {Box, Button, Grid, Link as MUILink, TextField, Typography} from "@mui/material";
import Link from "next/link";
import {theme} from "./LoginForm.styles";

function LoginForm () {
    return (
        <Box sx={theme.formBg}>
            <Typography component="h1" variant="h4" fontWeight="700">
                Prihlásenie
            </Typography>
            <Box component="form" sx={theme.formContent}>
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
                <Button type="submit" fullWidth variant="contained" sx={theme.submitButton}>
                    Prihlásiť sa
                </Button>
                <Grid item xs>
                    <Link href="/">
                        <MUILink href="#" variant="body2" sx={theme.adminContact}>
                            Kontakt na administrátora
                        </MUILink>
                    </Link>
                </Grid>
            </Box>
        </Box>
    )
}

export default LoginForm