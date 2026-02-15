import { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Paper, IconButton,
  Dialog, DialogTitle, DialogContent, DialogActions, TextField,
  Alert, Chip
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import api from '@/api/axios';
import { useAuth } from '@/hooks/useAuth';

interface WireGuardPeer {
  id: number;
  nas_device_id: number;
  public_key: string;
  allowed_ips: string;
  endpoint: string | null;
  is_active: boolean;
  created_at: string;
}

export default function WireGuardPeers() {
  const { user } = useAuth();
  const [peers, setPeers] = useState<WireGuardPeer[]>([]);
  const [nasDevices, setNasDevices] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPeer, setEditingPeer] = useState<WireGuardPeer | null>(null);
  const [form, setForm] = useState({
    nas_device_id: 0,
    public_key: '',
    allowed_ips: '',
    endpoint: '',
  });

  useEffect(() => {
    fetchPeers();
    fetchNasDevices();
  }, []);

  const fetchPeers = async () => {
    setLoading(true);
    try {
      const response = await api.get('/wireguard/peers');
      setPeers(response.data);
    } catch (err) {
      setError('Ошибка загрузки пиров');
    } finally {
      setLoading(false);
    }
  };

  const fetchNasDevices = async () => {
    try {
      const response = await api.get('/nas-devices');
      setNasDevices(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpen = (peer?: WireGuardPeer) => {
    if (peer) {
      setEditingPeer(peer);
      setForm({
        nas_device_id: peer.nas_device_id,
        public_key: peer.public_key,
        allowed_ips: peer.allowed_ips,
        endpoint: peer.endpoint || '',
      });
    } else {
      setEditingPeer(null);
      setForm({
        nas_device_id: 0,
        public_key: '',
        allowed_ips: '',
        endpoint: '',
      });
    }
    setDialogOpen(true);
  };

  const handleClose = () => {
    setDialogOpen(false);
    setEditingPeer(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingPeer) {
        await api.put(`/wireguard/peers/${editingPeer.id}`, form);
      } else {
        await api.post('/wireguard/peers', form);
      }
      fetchPeers();
      handleClose();
    } catch (err) {
      alert('Ошибка сохранения');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Удалить пир?')) {
      await api.delete(`/wireguard/peers/${id}`);
      fetchPeers();
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>WireGuard Peers</Typography>
      <Button variant="contained" startIcon={<AddIcon />} onClick={() => handleOpen()} sx={{ mb: 2 }}>
        Добавить пир
      </Button>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>NAS устройство</TableCell>
              <TableCell>Публичный ключ</TableCell>
              <TableCell>Allowed IPs</TableCell>
              <TableCell>Endpoint</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {peers.map((peer) => {
              const nas = nasDevices.find(d => d.id === peer.nas_device_id);
              return (
                <TableRow key={peer.id}>
                  <TableCell>{peer.id}</TableCell>
                  <TableCell>{nas?.name || peer.nas_device_id}</TableCell>
                  <TableCell>{peer.public_key.substring(0, 20)}…</TableCell>
                  <TableCell>{peer.allowed_ips}</TableCell>
                  <TableCell>{peer.endpoint}</TableCell>
                  <TableCell>
                    <Chip label={peer.is_active ? 'Активен' : 'Неактивен'} color={peer.is_active ? 'success' : 'default'} size="small" />
                  </TableCell>
                  <TableCell>
                    <IconButton size="small" onClick={() => handleOpen(peer)}><EditIcon /></IconButton>
                    <IconButton size="small" onClick={() => handleDelete(peer.id)}><DeleteIcon /></IconButton>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>{editingPeer ? 'Редактировать пир' : 'Новый пир'}</DialogTitle>
        <DialogContent>
          <TextField
            select
            margin="dense"
            label="NAS устройство"
            fullWidth
            value={form.nas_device_id}
            onChange={(e) => setForm({ ...form, nas_device_id: parseInt(e.target.value) })}
            SelectProps={{ native: true }}
          >
            <option value={0}>Выберите...</option>
            {nasDevices.map(dev => (
              <option key={dev.id} value={dev.id}>{dev.name} ({dev.ip_address})</option>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Публичный ключ"
            fullWidth
            multiline
            rows={2}
            value={form.public_key}
            onChange={(e) => setForm({ ...form, public_key: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Allowed IPs"
            fullWidth
            value={form.allowed_ips}
            onChange={(e) => setForm({ ...form, allowed_ips: e.target.value })}
            placeholder="192.168.99.2/32"
          />
          <TextField
            margin="dense"
            label="Endpoint"
            fullWidth
            value={form.endpoint}
            onChange={(e) => setForm({ ...form, endpoint: e.target.value })}
            placeholder="10.0.0.2:51820"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Отмена</Button>
          <Button onClick={handleSubmit} variant="contained">Сохранить</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}