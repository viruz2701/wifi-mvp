// src/pages/WireGuardPeers/index.tsx
import { useState, useEffect } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { IconButton, Stack, Typography, Tooltip } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
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
  nas_name: string;
  venue_name: string;
  venue_id: number;
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
    } catch {
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
    } catch {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    showSuccess('Публичный ключ скопирован');
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nas_name', headerName: 'NAS устройство', width: 200 },
    { field: 'venue_name', headerName: 'Площадка', width: 150 },
    {
      field: 'public_key',
      headerName: 'Публичный ключ',
      width: 400,
      renderCell: (params) => (
        <Stack direction="row" spacing={1} alignItems="center" sx={{ width: '100%' }}>
          <Typography
            variant="body2"
            sx={{
              fontFamily: 'monospace',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              flex: 1,
            }}
          >
            {params.value}
          </Typography>
          <Tooltip title="Копировать ключ">
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                copyToClipboard(params.value);
              }}
            >
              <ContentCopyIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
      ),
    },
    { field: 'allowed_ips', headerName: 'Allowed IPs', width: 150 },
    { field: 'endpoint', headerName: 'Endpoint', width: 150 },
    {
      field: 'is_active',
      headerName: 'Активен',
      width: 100,
      type: 'boolean',
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 100,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <Tooltip title="Удалить пир">
            <IconButton size="small" onClick={() => handleDeleteClick(params.row.id)}>
              <DeleteIcon />
            </IconButton>
          </Tooltip>
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
        </Stack>
        <DataGrid
          rows={peers}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
          initialState={{
            sorting: {
              sortModel: [{ field: 'id', sort: 'desc' }],
            },
          }}
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