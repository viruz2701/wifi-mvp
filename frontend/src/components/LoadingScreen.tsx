import { Box, CircularProgress, Typography } from '@mui/material';

export const LoadingScreen = ({ message = 'Загрузка...' }) => (
  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', minHeight: 400 }}>
    <CircularProgress />
    <Typography sx={{ mt: 2 }}>{message}</Typography>
  </Box>
);