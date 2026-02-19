import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography, Chip, Tooltip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import InfoIcon from '@mui/icons-material/Info';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import api from '@/api/axios';
import { NASDevice } from '@/types';
import { useSnackbar } from '@/hooks/useSnackbar';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { LoadingScreen } from '@/components/LoadingScreen';
import NASConnectionInfo from './NASConnectionInfo';

interface NasDevicesListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function NasDevicesList({ onEdit, onAdd }: NasDevicesListProps) {
  const [devices, setDevices] = useState<NASDevice[]>([]);
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [infoOpen, setInfoOpen] = useState(false);
  const [selectedNasId, setSelectedNasId] = useState<number | null>(null);
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    setLoading(true);
    try {
      const response = await api.get('/nas-devices');
      setDevices(response.data);
    } catch {
      showError('Не удалось загрузить список устройств');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (id: number) => setDeleteId(id);

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/nas-devices/${deleteId}`);
      showSuccess('Устройство удалено');
      fetchDevices();
    } catch {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
    }
  };

  const handleInfoClick = (id: number) => {
    setSelectedNasId(id);
    setInfoOpen(true);
  };

  const handleInfoClose = () => {
    setInfoOpen(false);
    setSelectedNasId(null);
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Название', width: 200 },
    { field: 'type', headerName: 'Тип', width: 120 },
    { field: 'ip_address', headerName: 'IP адрес', width: 150 },
    { field: 'venue_id', headerName: 'Площадка', width: 100 },
    {
      field: 'wireguard',
      headerName: 'WireGuard',
      width: 120,
      renderCell: (params) => {
        const hasWireguard = params.row.wireguard_pubkey;
        return (
          <Tooltip title={hasWireguard ? 'WireGuard настроен' : 'WireGuard не настроен'}>
            <Chip
              icon={<VpnKeyIcon />}
              label={hasWireguard ? 'Да' : 'Нет'}
              color={hasWireguard ? 'success' : 'default'}
              size="small"
              variant={hasWireguard ? 'filled' : 'outlined'}
            />
          </Tooltip>
        );
      },
    },
    {
      field: 'is_active',
      headerName: 'Статус',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Активно' : 'Неактивно'}
          color={params.value ? 'success' : 'default'}
          size="small"
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 180,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <Tooltip title="Информация о подключении">
            <IconButton size="small" onClick={() => handleInfoClick(params.row.id)}>
              <InfoIcon />
            </IconButton>
          </Tooltip>
          <IconButton size="small" onClick={() => onEdit(params.row.id)}>
            <EditIcon />
          </IconButton>
          <IconButton size="small" onClick={() => handleDeleteClick(params.row.id)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      ),
    },
  ];

  if (loading && devices.length === 0) return <LoadingScreen message="Загрузка устройств..." />;

  return (
    <>
      <div style={{ height: 600, width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography variant="h5">NAS-устройства</Typography>
            <Tooltip title="Открыть документацию по настройке">
              <IconButton
                component="a"
                href="/docs/admin_guide.md"
                target="_blank"
                size="small"
              >
                <MenuBookIcon />
              </IconButton>
            </Tooltip>
          </Stack>
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
      <ConfirmDialog
        open={deleteId !== null}
        message="Вы уверены, что хотите удалить устройство?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteId(null)}
      />
      {selectedNasId && (
        <NASConnectionInfo
          open={infoOpen}
          onClose={handleInfoClose}
          nasId={selectedNasId}
        />
      )}
    </>
  );
}