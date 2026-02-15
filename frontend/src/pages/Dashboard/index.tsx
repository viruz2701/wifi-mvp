import { useState, useEffect } from 'react';
import {
  Grid, Card, CardContent, Typography, Box,
  FormControl, InputLabel, Select, MenuItem, Button,
  Alert, CircularProgress
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ru } from 'date-fns/locale';
import { format, subDays } from 'date-fns';
import api from '@/api/axios';
import { useAuth } from '@/hooks/useAuth';

interface Metrics {
  unique_users: number;
  new_sessions: number;
  total_traffic_bytes: number;
  sms_sent: number;
  sms_confirmed: number;
}

export default function Dashboard() {
  const { user } = useAuth();
  const [period, setPeriod] = useState<'today' | 'week' | 'month'>('today');
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchMetrics = async () => {
    setLoading(true);
    setError('');
    try {
      const params: any = { period };
      const [metricsRes, chartRes] = await Promise.all([
        api.get('/reports/dashboard-metrics', { params }),
        api.get('/reports/activity', {
          params: {
            from_date: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
            to_date: format(new Date(), 'yyyy-MM-dd'),
          }
        })
      ]);
      setMetrics(metricsRes.data);
      setChartData(chartRes.data);
    } catch (err) {
      setError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, [period]);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Дашборд</Typography>
      <FormControl sx={{ mb: 2, minWidth: 200 }}>
        <InputLabel>Период</InputLabel>
        <Select value={period} onChange={(e) => setPeriod(e.target.value as any)} label="Период">
          <MenuItem value="today">Сегодня</MenuItem>
          <MenuItem value="week">Неделя</MenuItem>
          <MenuItem value="month">Месяц</MenuItem>
        </Select>
      </FormControl>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Уникальные пользователи</Typography>
              <Typography variant="h5">{metrics?.unique_users ?? '-'}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Новые сессии</Typography>
              <Typography variant="h5">{metrics?.new_sessions ?? '-'}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Трафик (МБ)</Typography>
              <Typography variant="h5">
                {metrics?.total_traffic_bytes ? (metrics.total_traffic_bytes / 1024 / 1024).toFixed(2) : '-'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>SMS отправлено/подтверждено</Typography>
              <Typography variant="h5">
                {metrics?.sms_sent ?? '-'} / {metrics?.sms_confirmed ?? '-'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Активность за последние 30 дней</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" tickFormatter={(str) => format(new Date(str), 'dd.MM')} />
                  <YAxis />
                  <Tooltip labelFormatter={(label) => format(new Date(label), 'dd.MM.yyyy')} />
                  <Legend />
                  <Line type="monotone" dataKey="sessions" stroke="#8884d8" name="Сессии" />
                  <Line type="monotone" dataKey="unique_users" stroke="#82ca9d" name="Уникальные" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}