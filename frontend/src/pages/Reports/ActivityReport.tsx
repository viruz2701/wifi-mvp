import { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, FormControl, InputLabel, Select, MenuItem, Button, Alert } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '@/api/axios';
import { useAuth } from '@/hooks/useAuth';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ru } from 'date-fns/locale';
import { format } from 'date-fns';
import { ActivityReportItem } from '@/types';

export default function ActivityReport() {
  const { user } = useAuth();
  const [venues, setVenues] = useState<any[]>([]);
  const [selectedVenue, setSelectedVenue] = useState<number | ''>('');
  const [fromDate, setFromDate] = useState<Date | null>(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000));
  const [toDate, setToDate] = useState<Date | null>(new Date());
  const [data, setData] = useState<ActivityReportItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user?.role === 'admin') {
      api.get('/venues').then(res => setVenues(res.data));
    } else if (user?.venue_id) {
      setSelectedVenue(user.venue_id);
    }
  }, [user]);

  const fetchReport = async () => {
    if (!fromDate || !toDate) return;
    setLoading(true);
    setError('');
    try {
      const params: any = {
        from_date: format(fromDate, 'yyyy-MM-dd'),
        to_date: format(toDate, 'yyyy-MM-dd'),
      };
      if (selectedVenue) params.venue_id = selectedVenue;
      const response = await api.get('/reports/activity', { params });
      setData(response.data);
    } catch (err) {
      setError('Ошибка загрузки отчёта');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>Активность пользователей</Typography>
        <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
          {user?.role === 'admin' && (
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Площадка</InputLabel>
              <Select value={selectedVenue} onChange={(e) => setSelectedVenue(e.target.value as number)} label="Площадка">
                <MenuItem value="">Все</MenuItem>
                {venues.map(v => <MenuItem key={v.id} value={v.id}>{v.name}</MenuItem>)}
              </Select>
            </FormControl>
          )}
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ru}>
            <DatePicker
              label="От"
              value={fromDate}
              onChange={(newValue) => setFromDate(newValue)}
              slotProps={{ textField: { size: 'small' } }}
            />
            <DatePicker
              label="До"
              value={toDate}
              onChange={(newValue) => setToDate(newValue)}
              slotProps={{ textField: { size: 'small' } }}
            />
          </LocalizationProvider>
          <Button variant="contained" onClick={fetchReport} disabled={loading}>
            {loading ? 'Загрузка...' : 'Сформировать'}
          </Button>
        </Box>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" tickFormatter={(str) => format(new Date(str), 'dd.MM.yyyy')} />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip labelFormatter={(label) => format(new Date(label), 'dd.MM.yyyy')} />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="sessions" stroke="#8884d8" name="Сессии" />
            <Line yAxisId="right" type="monotone" dataKey="unique_users" stroke="#82ca9d" name="Уникальные пользователи" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}