import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { IconButton, Stack, Typography, Chip, TextField, Button, Box } from '@mui/material';
import BlockIcon from '@mui/icons-material/Block';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { getUserProfiles, updateUserProfile } from '@/api/userProfiles';
import { UserProfile } from '@/types';

export default function ProfilesList() {
  const [profiles, setProfiles] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ mac: '', phone: '', venue_id: '' });

  useEffect(() => {
    fetchProfiles();
  }, [filters]);

  const fetchProfiles = async () => {
    setLoading(true);
    try {
      const params = Object.fromEntries(Object.entries(filters).filter(([_, v]) => v));
      const response = await getUserProfiles(params);
      setProfiles(response.data);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleBlock = async (id: number, currentBlocked: boolean) => {
    await updateUserProfile(id, { is_blocked: !currentBlocked });
    fetchProfiles();
  };

  const handleToggleVip = async (id: number, currentVip: boolean) => {
    await updateUserProfile(id, { is_vip: !currentVip });
    fetchProfiles();
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'mac_address', headerName: 'MAC', width: 150 },
    { field: 'phone_number', headerName: 'Телефон', width: 130 },
    { field: 'email', headerName: 'Email', width: 180 },
    { field: 'total_sessions', headerName: 'Сессии', width: 100 },
    { field: 'total_traffic_bytes', headerName: 'Трафик (байт)', width: 130 },
    {
      field: 'is_blocked',
      headerName: 'Заблокирован',
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value ? 'Да' : 'Нет'} color={params.value ? 'error' : 'success'} size="small" />
      ),
    },
    {
      field: 'is_vip',
      headerName: 'VIP',
      width: 80,
      renderCell: (params) => (
        <Chip label={params.value ? 'VIP' : 'Нет'} color={params.value ? 'warning' : 'default'} size="small" />
      ),
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 150,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <IconButton size="small" onClick={() => handleToggleBlock(params.row.id, params.row.is_blocked)}>
            {params.row.is_blocked ? <CheckCircleIcon color="success" /> : <BlockIcon color="error" />}
          </IconButton>
          <IconButton size="small" onClick={() => handleToggleVip(params.row.id, params.row.is_vip)}>
            {params.row.is_vip ? 'Снять VIP' : 'Сделать VIP'}
          </IconButton>
        </Stack>
      ),
    },
  ];

  return (
    <div style={{ height: 600, width: '100%' }}>
      <Typography variant="h5" gutterBottom>Профили пользователей</Typography>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField label="MAC" value={filters.mac} onChange={(e) => setFilters({ ...filters, mac: e.target.value })} size="small" />
        <TextField label="Телефон" value={filters.phone} onChange={(e) => setFilters({ ...filters, phone: e.target.value })} size="small" />
        <TextField label="ID площадки" value={filters.venue_id} onChange={(e) => setFilters({ ...filters, venue_id: e.target.value })} size="small" />
        <Button variant="outlined" onClick={fetchProfiles}>Применить</Button>
      </Box>
      <DataGrid
        rows={profiles}
        columns={columns}
        loading={loading}
        pageSizeOptions={[10, 25, 50, 100]}
      />
    </div>
  );
}