import { useEffect, useState, useCallback } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Button,
  Stack,
  Typography,
  Alert,
  CircularProgress,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import api from '@/api/axios';
import { useSnackbar } from '@/hooks/useSnackbar';
import { AxiosError } from 'axios';
import { RadiusAttribute } from './types';

interface RadiusAttributesListProps {
  onEdit: (attr: RadiusAttribute) => void;
  onAdd: () => void;
}

const RadiusAttributesList: React.FC<RadiusAttributesListProps> = ({ onEdit, onAdd }) => {
  const [attributes, setAttributes] = useState<RadiusAttribute[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { showSuccess, showError } = useSnackbar();

  const fetchAttributes = useCallback(async () => {
    setLoading(true);
    try {
      const response = await api.get('/radius-attributes/');
      setAttributes(response.data);
      setError('');
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.message : 'Ошибка загрузки';
      setError(errorMessage);
      showError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [showError]);

  useEffect(() => {
    fetchAttributes();
  }, [fetchAttributes]);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить RADIUS-атрибут?')) return;
    try {
      await api.delete(`/radius-attributes/${id}`);
      showSuccess('Атрибут удалён');
      fetchAttributes();
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.message : 'Ошибка удаления';
      showError(errorMessage);
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <div>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">RADIUS-атрибуты</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
          Добавить
        </Button>
      </Stack>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Имя</TableCell>
              <TableCell>Vendor ID</TableCell>
              <TableCell>Проприетарный</TableCell>
              <TableCell>Описание</TableCell>
              <TableCell>Формат</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {attributes.map((attr) => (
              <TableRow key={attr.id}>
                <TableCell>{attr.id}</TableCell>
                <TableCell>{attr.name}</TableCell>
                <TableCell>{attr.vendor_id || '—'}</TableCell>
                <TableCell>
                  <Chip
                    label={attr.is_proprietary ? 'Да' : 'Нет'}
                    color={attr.is_proprietary ? 'warning' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{attr.description || '—'}</TableCell>
                <TableCell>{attr.format_hint || '—'}</TableCell>
                <TableCell align="right">
                  <IconButton size="small" onClick={() => onEdit(attr)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDelete(attr.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default RadiusAttributesList;