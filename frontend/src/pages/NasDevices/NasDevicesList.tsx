import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { getNasDevices, deleteNasDevice } from '@/api/nasDevices';
import { NASDevice } from '@/types';

interface NasDevicesListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function NasDevicesList({ onEdit, onAdd }: NasDevicesListProps) {
  const [devices, setDevices] = useState<NASDevice[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    setLoading(true);
    try {
      const response = await getNasDevices();
      setDevices(response.data);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Удалить устройство?')) {
      await deleteNasDevice(id);
      fetchDevices();
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Название', width: 200 },
    { field: 'type', headerName: 'Тип', width: 120 },
    { field: 'ip_address', headerName: 'IP адрес', width: 150 },
    { field: 'venue_id', headerName: 'Площадка', width: 100 },
    {
      field: 'is_active',
      headerName: 'Статус',
      width: 100,
      renderCell: (params) => (
        <Chip label={params.value ? 'Активно' : 'Неактивно'} color={params.value ? 'success' : 'default'} size="small" />
      ),
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 120,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <IconButton size="small" onClick={() => onEdit(params.row.id)}>
            <EditIcon />
          </IconButton>
          <IconButton size="small" onClick={() => handleDelete(params.row.id)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      ),
    },
  ];

  return (
    <div style={{ height: 600, width: '100%' }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">NAS-устройства</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
          Добавить
        </Button>
      </Stack>
      <DataGrid
        rows={devices}
        columns={columns}
        loading={loading}
        pageSizeOptions={[10, 25, 50, 100]}
      />
    </div>
  );
}