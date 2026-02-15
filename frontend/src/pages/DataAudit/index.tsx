import { useState, useEffect } from 'react';
import {
  Box, Typography, Button, TextField, MenuItem, Grid,
  Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Pagination, Alert, FormControl, InputLabel, Select, Stack
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ru } from 'date-fns/locale';
import { format } from 'date-fns';
import api from '@/api/axios';
import { useAuth } from '@/hooks/useAuth';
import DownloadIcon from '@mui/icons-material/Download';

interface AuthLog {
  id: number;
  type: string;
  created_at: string;
  mac_address: string;
  phone_number: string | null;
  data: any;
}

export default function DataAudit() {
  const { user } = useAuth();
  const [logs, setLogs] = useState<AuthLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    mac: '',
    phone: '',
    from_date: null as Date | null,
    to_date: null as Date | null,
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchLogs = async () => {
    setLoading(true);
    setError('');
    try {
      const params: any = {
        page,
        limit: 20,
        ...filters,
        from_date: filters.from_date ? format(filters.from_date, 'yyyy-MM-dd') : undefined,
        to_date: filters.to_date ? format(filters.to_date, 'yyyy-MM-dd') : undefined,
      };
      const response = await api.get('/export/auth-logs', { params });
      setLogs(response.data.items);
      setTotalPages(response.data.total_pages);
    } catch (err) {
      setError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: 'csv' | 'json') => {
    const params: any = {
      format,
      ...filters,
      from_date: filters.from_date ? format(filters.from_date, 'yyyy-MM-dd') : undefined,
      to_date: filters.to_date ? format(filters.to_date, 'yyyy-MM-dd') : undefined,
    };
    const url = `/api/v1/export/auth-logs?${new URLSearchParams(params)}`;
    window.open(url, '_blank');
  };

  useEffect(() => {
    fetchLogs();
  }, [page, filters]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Мои данные (аудит авторизаций)</Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              label="MAC"
              value={filters.mac}
              onChange={(e) => setFilters({ ...filters, mac: e.target.value })}
              fullWidth
              size="small"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              label="Телефон"
              value={filters.phone}
              onChange={(e) => setFilters({ ...filters, phone: e.target.value })}
              fullWidth
              size="small"
            />
          </Grid>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ru}>
            <Grid item xs={12} sm={6} md={3}>
              <DatePicker
                label="От"
                value={filters.from_date}
                onChange={(newValue) => setFilters({ ...filters, from_date: newValue })}
                slotProps={{ textField: { size: 'small', fullWidth: true } }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <DatePicker
                label="До"
                value={filters.to_date}
                onChange={(newValue) => setFilters({ ...filters, to_date: newValue })}
                slotProps={{ textField: { size: 'small', fullWidth: true } }}
              />
            </Grid>
          </LocalizationProvider>
          <Grid item xs={12}>
            <Stack direction="row" spacing={2}>
              <Button variant="contained" onClick={fetchLogs} disabled={loading}>
                Применить
              </Button>
              <Button variant="outlined" startIcon={<DownloadIcon />} onClick={() => handleExport('csv')}>
                CSV
              </Button>
              <Button variant="outlined" startIcon={<DownloadIcon />} onClick={() => handleExport('json')}>
                JSON
              </Button>
            </Stack>
          </Grid>
        </Grid>
      </Paper>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Тип</TableCell>
              <TableCell>Дата</TableCell>
              <TableCell>MAC</TableCell>
              <TableCell>Телефон</TableCell>
              <TableCell>Данные</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.map((log) => (
              <TableRow key={log.id}>
                <TableCell>{log.id}</TableCell>
                <TableCell>{log.type}</TableCell>
                <TableCell>{new Date(log.created_at).toLocaleString()}</TableCell>
                <TableCell>{log.mac_address}</TableCell>
                <TableCell>{log.phone_number}</TableCell>
                <TableCell>{JSON.stringify(log.data)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
        <Pagination count={totalPages} page={page} onChange={(_, val) => setPage(val)} />
      </Box>
    </Box>
  );
}