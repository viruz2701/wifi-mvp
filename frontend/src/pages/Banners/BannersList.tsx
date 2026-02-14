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
import { getBanners, deleteBanner } from '@/api/banners';
import { getVenues } from '@/api/venues';
import { Banner, Venue } from '@/types';
import FileUploader from '@/components/FileUploader/FileUploader';
import { useAuth } from '@/hooks/useAuth';

interface BannersListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function BannersList({ onEdit, onAdd }: BannersListProps) {
  const { user } = useAuth();
  const [banners, setBanners] = useState<Banner[]>([]);
  const [venues, setVenues] = useState<Venue[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedVenue, setSelectedVenue] = useState<number>(
    user?.role === 'admin' ? 0 : user?.venue_id || 1
  );

  // Загружаем список площадок для админа
  useEffect(() => {
    if (user?.role === 'admin') {
      getVenues().then(res => setVenues(res.data));
    }
  }, [user]);

  // Загружаем баннеры при изменении выбранной площадки
  useEffect(() => {
    if (selectedVenue || selectedVenue === 0) {
      fetchBanners();
    }
  }, [selectedVenue]);

  const fetchBanners = async () => {
    setLoading(true);
    try {
      const response = await getBanners(selectedVenue === 0 ? undefined : selectedVenue);
      setBanners(response.data);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Удалить баннер?')) {
      await deleteBanner(id);
      fetchBanners();
    }
  };

  const handleUploadSuccess = (bannerId: number, newImageUrl: string) => {
    setBanners(prev =>
      prev.map(b => (b.id === bannerId ? { ...b, image_url: newImageUrl } : b))
    );
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
        pageSizeOptions={[10, 25, 50]}
        getRowId={(row) => row.id}
      />
    </div>
  );
}