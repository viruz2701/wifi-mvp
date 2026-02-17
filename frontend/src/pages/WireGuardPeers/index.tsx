import React, { useState, useEffect } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import api from '@/api/axios';
import { useSnackbar } from '@/hooks/useSnackbar';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { LoadingScreen } from '@/components/LoadingScreen';

interface WireGuardPeer {
  id: number;
  nas_device_id: number;
  public_key: string;
  allowed_ips: string;
  endpoint: string | null;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export default function WireGuardPeers() {
  const [peers, setPeers] = useState<WireGuardPeer[]>([]);
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    fetchPeers();
  }, []);

  const fetchPeers = async () => {
    setLoading(true);
    try {
      const response = await api.get('/wireguard/peers');
      setPeers(response.data);
    } catch (error) {
      showError('Не удалось загрузить список пиров');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (id: number) => setDeleteId(id);

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/wireguard/peers/${deleteId}`);
      showSuccess('Пир удалён');
      fetchPeers();
    } catch (error) {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nas_device_id', headerName: 'NAS Device', width: 120 },
    { field: 'public_key', headerName: 'Public Key', width: 300 },
    { field: 'allowed_ips', headerName: 'Allowed IPs', width: 150 },
    { field: 'endpoint', headerName: 'Endpoint', width: 150 },
    {
      field: 'is_active',
      headerName: 'Active',
      width: 100,
      type: 'boolean',
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 120,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <IconButton size="small" onClick={() => handleDeleteClick(params.row.id)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      ),
    },
  ];

  if (loading && peers.length === 0) return <LoadingScreen message="Загрузка пиров..." />;

  return (
    <>
      <div style={{ height: 600, width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5">WireGuard Peers</Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={() => {}}>
            Добавить
          </Button>
        </Stack>
        <DataGrid
          rows={peers}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
        />
      </div>
      <ConfirmDialog
        open={deleteId !== null}
        message="Вы уверены, что хотите удалить пир?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteId(null)}
      />
    </>
  );
}