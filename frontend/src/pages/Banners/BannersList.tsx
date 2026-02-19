import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import {
  Button,
  IconButton,
  Stack,
  Typography,
  Chip,
  Box,
  TextField,
  MenuItem,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import FileUploader from '@/components/FileUploader/FileUploader';
import { useSnackbar } from '@/hooks/useSnackbar';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { LoadingScreen } from '@/components/LoadingScreen';
import { useAuth } from '@/hooks/useAuth';
import { getBanners, deleteBanner } from '@/api/banners';
import { getVenues } from '@/api/venues';
import { Banner, Venue } from '@/types';

interface BannersListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function BannersList({ onEdit, onAdd }: BannersListProps) {
  const { user } = useAuth();
  const [banners, setBanners] = useState<Banner[]>([]);
  const [venues, setVenues] = useState<Venue[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedVenue, setSelectedVenue] = useState<number | ''>('');
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    if (user?.role === 'admin') {
      getVenues().then(res => setVenues(res.data));
    } else if (user?.venue_id) {
      setSelectedVenue(user.venue_id);
    }
  }, [user]);

  useEffect(() => {
    const fetchBanners = async () => {
      if (selectedVenue === '') return;
      setLoading(true);
      try {
        const venueId = selectedVenue === 0 ? undefined : selectedVenue;
        const response = await getBanners(venueId);
        setBanners(response.data);
      } catch {
        showError('Не удалось загрузить баннеры');
      } finally {
        setLoading(false);
      }
    };

    fetchBanners();
  }, [selectedVenue, showError]);

  const handleDeleteClick = (id: number) => setDeleteId(id);

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    try {
      await deleteBanner(deleteId);
      showSuccess('Баннер удалён');
      if (selectedVenue !== '') {
        const venueId = selectedVenue === 0 ? undefined : selectedVenue;
        const response = await getBanners(venueId);
        setBanners(response.data);
      }
    } catch {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
    }
  };

  const handleUploadSuccess = (bannerId: number, newImageUrl: string) => {
    setBanners(prev =>
      prev.map(b => (b.id === bannerId ? { ...b, image_url: newImageUrl } : b))
    );
    showSuccess('Изображение загружено');
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    {
      field: 'image',
      headerName: 'Изображение',
      width: 140,
      renderCell: (params) =>
        params.row.image_url ? (
          <img
            src={params.row.image_url}
            alt="баннер"
            style={{ maxWidth: 120, maxHeight: 60, objectFit: 'contain' }}
          />
        ) : (
          <FileUploader
            uploadUrl={`/api/v1/banners/${params.row.id}/upload`}
            onSuccess={(url) => handleUploadSuccess(params.row.id, url)}
            buttonText="Загрузить"
          />
        ),
    },
    { field: 'target_url', headerName: 'URL перехода', width: 200 },
    { field: 'clicks_count', headerName: 'Клики', width: 100 },
    { field: 'impressions_count', headerName: 'Показы', width: 100 },
    {
      field: 'is_active',
      headerName: 'Активен',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Да' : 'Нет'}
          color={params.value ? 'success' : 'default'}
          size="small"
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 150,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <IconButton
            size="small"
            onClick={() => window.open(params.row.target_url, '_blank')}
          >
            <VisibilityIcon />
          </IconButton>
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

  if (loading && banners.length === 0) return <LoadingScreen message="Загрузка баннеров..." />;

  return (
    <>
      <div style={{ height: 600, width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5">Баннеры</Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
            Добавить
          </Button>
        </Stack>

        {user?.role === 'admin' && (
          <Box mb={2} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <TextField
              select
              label="Площадка"
              value={selectedVenue}
              onChange={(e) => setSelectedVenue(Number(e.target.value))}
              sx={{ minWidth: 200 }}
              size="small"
            >
              <MenuItem value={0}>Все площадки</MenuItem>
              {venues.map(v => (
                <MenuItem key={v.id} value={v.id}>
                  {v.name}
                </MenuItem>
              ))}
            </TextField>
          </Box>
        )}

        <DataGrid
          rows={banners}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
          getRowId={(row) => row.id}
        />
      </div>

      <ConfirmDialog
        open={deleteId !== null}
        message="Вы уверены, что хотите удалить баннер?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteId(null)}
      />
    </>
  );
}