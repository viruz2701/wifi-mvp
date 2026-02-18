import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { useSnackbar } from '@/hooks/useSnackbar';
import { getSocialActions } from '@/api/socialActions';
import {
  getVenueSocialActions,
  addVenueSocialAction,
  updateVenueSocialAction,
  deleteVenueSocialAction,
} from '@/api/socialActions';
import { SocialAction, VenueSocialAction } from '@/types';
import api from '@/api/axios';

interface VenueSocialActionsProps {
  venueId: number;
}

interface Tariff {
  id: number;
  name: string;
}

interface FormData {
  action_id: number | '';
  reward_tariff_id: number | '';
  reward_duration_hours: number;
}

const VenueSocialActions: React.FC<VenueSocialActionsProps> = ({ venueId }) => {
  const [actions, setActions] = useState<VenueSocialAction[]>([]);
  const [availableActions, setAvailableActions] = useState<SocialAction[]>([]);
  const [tariffs, setTariffs] = useState<Tariff[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<FormData>({
    action_id: '',
    reward_tariff_id: '',
    reward_duration_hours: 1,
  });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const { showSuccess, showError } = useSnackbar();

  const fetchData = async () => {
    setLoading(true);
    try {
      const [actionsRes, availableRes, tariffsRes] = await Promise.all([
        getVenueSocialActions(venueId),
        getSocialActions(),
        api.get('/tariff-plans/'),
      ]);
      setActions(actionsRes.data);
      setAvailableActions(availableRes.data.filter(a => a.is_active));
      setTariffs(tariffsRes.data);
    } catch (err) {
      showError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (venueId) fetchData();
  }, [venueId]);

  const handleOpenDialog = (item?: VenueSocialAction) => {
    if (item) {
      setEditingId(item.id);
      setFormData({
        action_id: item.action_id,
        reward_tariff_id: item.reward_tariff_id || '',
        reward_duration_hours: item.reward_duration_hours,
      });
    } else {
      setEditingId(null);
      setFormData({
        action_id: '',
        reward_tariff_id: '',
        reward_duration_hours: 1,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setFormErrors({});
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (formErrors[name]) {
      setFormErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};
    if (!formData.action_id) {
      errors.action_id = 'Выберите действие';
    }
    if (formData.reward_duration_hours < 1) {
      errors.reward_duration_hours = 'Длительность должна быть не менее 1 часа';
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSave = async () => {
    if (!validate()) return;
    try {
      const payload = {
        action_id: formData.action_id as number, // на этом этапе уже число, если прошло валидацию
        reward_tariff_id: formData.reward_tariff_id || null,
        reward_duration_hours: formData.reward_duration_hours,
      };
      if (editingId) {
        await updateVenueSocialAction(editingId, payload);
        showSuccess('Привязка обновлена');
      } else {
        await addVenueSocialAction(venueId, payload);
        showSuccess('Привязка добавлена');
      }
      fetchData();
      handleCloseDialog();
    } catch (err: any) {
      showError(err.response?.data?.detail || 'Ошибка сохранения');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить привязку?')) return;
    try {
      await deleteVenueSocialAction(id);
      showSuccess('Привязка удалена');
      fetchData();
    } catch (err) {
      showError('Ошибка удаления');
    }
  };

  const getActionName = (actionId: number) => {
    const action = availableActions.find(a => a.id === actionId);
    return action ? `${action.name} (${action.network})` : `ID ${actionId}`;
  };

  const getTariffName = (tariffId?: number) => {
    if (!tariffId) return '—';
    const tariff = tariffs.find(t => t.id === tariffId);
    return tariff ? tariff.name : `ID ${tariffId}`;
  };

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">Социальные акции площадки</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => handleOpenDialog()}>
          Добавить
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Действие</TableCell>
              <TableCell>Тариф-награда</TableCell>
              <TableCell>Длительность (часы)</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {actions.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{getActionName(item.action_id)}</TableCell>
                <TableCell>{getTariffName(item.reward_tariff_id)}</TableCell>
                <TableCell>{item.reward_duration_hours}</TableCell>
                <TableCell align="right">
                  <IconButton size="small" onClick={() => handleOpenDialog(item)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDelete(item.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
            {actions.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  Нет привязанных социальных акций
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Редактировать привязку' : 'Добавить привязку'}</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            margin="dense"
            name="action_id"
            label="Социальное действие"
            value={formData.action_id}
            onChange={handleChange}
            error={!!formErrors.action_id}
            helperText={formErrors.action_id}
          >
            <MenuItem value="">
              <em>Выберите действие</em>
            </MenuItem>
            {availableActions.map((a) => (
              <MenuItem key={a.id} value={a.id}>
                {a.name} ({a.network}) - {a.type}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            fullWidth
            margin="dense"
            name="reward_tariff_id"
            label="Тариф-награда (необязательно)"
            value={formData.reward_tariff_id}
            onChange={handleChange}
          >
            <MenuItem value="">Без тарифа</MenuItem>
            {tariffs.map((t) => (
              <MenuItem key={t.id} value={t.id}>
                {t.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            fullWidth
            margin="dense"
            name="reward_duration_hours"
            label="Длительность награды (часы)"
            type="number"
            value={formData.reward_duration_hours}
            onChange={handleChange}
            error={!!formErrors.reward_duration_hours}
            helperText={formErrors.reward_duration_hours}
            inputProps={{ min: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSave} variant="contained">
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default VenueSocialActions;