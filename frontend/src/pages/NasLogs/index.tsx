import React, { useState, useEffect } from 'react';
import { Paper, Typography, FormControl, InputLabel, Select, MenuItem, TextField, Button, Stack, Box } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ru } from 'date-fns/locale';
import api from '@/api/axios';
import { useSnackbar } from '@/hooks/useSnackbar';
import { LoadingScreen } from '@/components/LoadingScreen';

interface NasStatusRecord {
  id: number;
  nas_device_id: number;
  status: string;
  checked_at: string;
  nas_name?: string;
}

export default function NasLogs() {
  const [records, setRecords] = useState<NasStatusRecord[]>([]);
  const [nasDevices, setNasDevices] = useState<{ id: number; name: string }[]>([]);
  const [selectedNas, setSelectedNas] = useState<number | ''>('');
  const [fromDate, setFromDate] = useState<Date | null>(null);
  const [toDate, setToDate] = useState<Date | null>(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(50);
  const [total, setTotal] = useState(0);
  const { showError } = useSnackbar();

  useEffect(() => {
    fetchNasDevices();
    fetchLogs();
  }, []);

  useEffect(() => {
    fetchLogs();
  }, [selectedNas, fromDate, toDate, page, pageSize]);

  const fetchNasDevices = async () => {
    try {
      const response = await api.get('/nas-devices');
      setNasDevices(response.data);
    } catch (err) {
      showError('Не удалось загрузить список устройств');
    }
  };

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const params: any = {
        skip: page * pageSize,
        limit: pageSize,
      };
      if (selectedNas) params.nas_device_id = selectedNas;
      if (fromDate) params.from_date = fromDate.toISOString().split('T')[0];
      if (toDate) params.to_date = toDate.toISOString().split('T')[0];
      const response = await api.get('/nas-status-history', { params });
      // Обогащаем записи именами устройств
      const enriched = response.data.map((rec: any) => ({
        ...rec,
        nas_name: nasDevices.find(d => d.id === rec.nas_device_id)?.name || `ID ${rec.nas_device_id}`,
      }));
      setRecords(enriched);
      // Предполагаем, что сервер не возвращает общее количество, поэтому total не обновляем
    } catch (err) {
      showError('Ошибка загрузки логов');
    } finally {
      setLoading(false);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nas_name', headerName: 'Устройство', width: 200 },
    { field: 'status', headerName: 'Статус', width: 120 },
    {
      field: 'checked_at',
      headerName: 'Время проверки',
      width: 200,
      valueFormatter: (params) => new Date(params.value).toLocaleString(),
    },
  ];

  if (loading && records.length === 0) return <LoadingScreen />;

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Логи состояния NAS</Typography>
      <Stack direction="row" spacing={2} sx={{ mb: 3 }} flexWrap="wrap">
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Устройство</InputLabel>
          <Select
            value={selectedNas}
            onChange={(e) => setSelectedNas(e.target.value as number)}
            label="Устройство"
          >
            <MenuItem value="">Все</MenuItem>
            {nasDevices.map(dev => <MenuItem key={dev.id} value={dev.id}>{dev.name}</MenuItem>)}
          </Select>
        </FormControl>
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
        <Button variant="contained" onClick={fetchLogs}>Применить</Button>
      </Stack>
      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={records}
          columns={columns}
          loading={loading}
          paginationMode="server"
          rowCount={total}
          pageSizeOptions={[50, 100, 200]}
          paginationModel={{ page, pageSize }}
          onPaginationModelChange={(model) => {
            setPage(model.page);
            setPageSize(model.pageSize);
          }}
        />
      </Box>
    </Paper>
  );
}