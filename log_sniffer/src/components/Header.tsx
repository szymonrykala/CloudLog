import MenuIcon from '@mui/icons-material/Menu';
import GroupRoundedIcon from '@mui/icons-material/GroupRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
import LogoutIcon from '@mui/icons-material/Logout';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import IconButton from '@mui/joy/IconButton';
import Divider from '@mui/joy/Divider';
import { useColorScheme } from '@mui/joy/styles';
import { useState, useEffect } from 'react';


function ColorSchemeToggle() {
    const { mode, setMode } = useColorScheme();
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) {
        return <IconButton size="sm" variant="outlined" color="primary" />;
    }

    return (
        <IconButton
            id="toggle-mode"
            size="sm"
            variant="outlined"
            color="primary"
            onClick={() => {
                if (mode === 'light') {
                    setMode('dark');
                } else {
                    setMode('light');
                }
            }}
        >
            {mode === 'light' ? <DarkModeRoundedIcon /> : <LightModeRoundedIcon />}
        </IconButton>
    );
}

function removeCredentials(){
    localStorage.clear()
    window.location.reload()
}

export default function Header() {

    return (
        <>
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center',
                    gap: 1.5,
                }}
            >
                <IconButton
                    variant="outlined"
                    size="sm"
                    onClick={() => {}}
                    sx={{ display: { sm: 'none' } }}
                >
                    <MenuIcon />
                </IconButton>
                <IconButton
                    size="sm"
                    variant="solid"
                    sx={{ display: { xs: 'none', sm: 'inline-flex' } }}
                >
                    <GroupRoundedIcon />
                </IconButton>
                <Typography component="h1" fontWeight="xl">
                    LogSniffer
                </Typography>
            </Box>

            <Box sx={{ display: 'flex', flexDirection: 'row', gap: 1.5 }}>
                <ColorSchemeToggle />
                <Divider />
                <IconButton
                    size="sm"
                    variant="outlined"
                    color="danger"
                    onClick={removeCredentials}
                >
                    <LogoutIcon />
                </IconButton>


            </Box>
        </>
    );
}