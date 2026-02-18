import React, { useState, useEffect, useRef } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, TextField, Box, Typography, Alert, IconButton,
  InputAdornment,
} from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DownloadIcon from '@mui/icons-material/Download';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { useSnackbar } from '@/hooks/useSnackbar';
import api from '@/api/axios';

interface NASConnectionInfoProps {
  open: boolean;
  onClose: () => void;
  nasId: number;
}

interface NASDetail {
  id: number;
  name: string;
  type: string;
  ip_address: string;
  wireguard_ip?: string;
  wireguard_pubkey?: string;
  wireguard_generated?: boolean;
  api_username?: string;
  api_password?: string;
}

interface WireGuardSettings {
  server_public_key: string;
  server_endpoint: string;
}

const NASConnectionInfo: React.FC<NASConnectionInfoProps> = ({ open, onClose, nasId }) => {
  const [nas, setNas] = useState<NASDetail | null>(null);
  const [wgSettings, setWgSettings] = useState<WireGuardSettings | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [privateKey, setPrivateKey] = useState<string | null>(null);
  const { showSuccess, showError } = useSnackbar();
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    if (open && nasId) {
      fetchData();
    }
    return () => {
      mounted.current = false;
    };
  }, [open, nasId]);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [nasRes, wgRes] = await Promise.all([
        api.get(`/nas-devices/${nasId}`),
        api.get('/settings/wireguard'),
      ]);
      if (!mounted.current) return;
      setNas(nasRes.data);
      setWgSettings(wgRes.data);
      if (nasRes.data.wireguard_generated) {
        try {
          const privRes = await api.get(`/nas-devices/${nasId}/wireguard-private-key`);
          if (mounted.current) setPrivateKey(privRes.data.private_key);
        } catch (err) {
          console.warn('Could not fetch private key', err);
        }
      }
    } catch (err) {
      if (mounted.current) setError('Не удалось загрузить данные');
    } finally {
      if (mounted.current) setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    showSuccess('Скопировано в буфер обмена');
  };

  const getSshCommand = () => {
    if (!nas) return '';
    return `ssh ${nas.api_username || 'root'}@${nas.wireguard_ip || nas.ip_address}`;
  };

  const getWireGuardConfig = (): string => {
    if (!wgSettings || !nas?.wireguard_pubkey) return '';
    const privKeyLine = privateKey 
      ? `PrivateKey = ${privateKey}`
      : '# PrivateKey = <ваш приватный ключ> (сгенерируйте сами)';
    return `[Interface]
Address = ${nas.wireguard_ip}/32
DNS = 8.8.8.8
${privKeyLine}

[Peer]
PublicKey = ${wgSettings.server_public_key}
Endpoint = ${wgSettings.server_endpoint}
AllowedIPs = ${nas.wireguard_ip}/32
PersistentKeepalive = 25`;
  };

  const downloadConfig = () => {
    const config = getWireGuardConfig();
    const blob = new Blob([config], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `wg-${nas?.name || 'nas'}.conf`;
    a.click();
    URL.revokeObjectURL(url);
    showSuccess('Конфигурация скачана');
  };

  const downloadPrivateKey = async () => {
    try {
      const response = await api.get(`/nas-devices/${nasId}/wireguard-private-key`);
      const { private_key } = response.data;
      const blob = new Blob([private_key], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `wg-${nas?.name || 'nas'}.key`;
      a.click();
      URL.revokeObjectURL(url);
      showSuccess('Приватный ключ скачан');
    } catch (err: any) {
      if (err.response?.status === 404) {
        showError('Приватный ключ не найден (возможно, введён вручную)');
      } else {
        showError('Ошибка загрузки ключа');
      }
    }
  };

  if (!nas) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Подключение к NAS: {nas.name}</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error">{error}</Alert>}
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle1">Основные параметры</Typography>
          <TextField
            label="Тип устройства"
            value={nas.type}
            fullWidth
            margin="dense"
            InputProps={{ readOnly: true }}
          />
          <TextField
            label="Публичный IP"
            value={nas.ip_address}
            fullWidth
            margin="dense"
            InputProps={{
              readOnly: true,
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => copyToClipboard(nas.ip_address)}>
                    <ContentCopyIcon />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
          {nas.wireguard_ip && (
            <TextField
              label="WireGuard IP"
              value={nas.wireguard_ip}
              fullWidth
              margin="dense"
              InputProps={{
                readOnly: true,
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => copyToClipboard(nas.wireguard_ip)}>
                      <ContentCopyIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          )}
          <TextField
            label="Имя пользователя API"
            value={nas.api_username || 'не указан'}
            fullWidth
            margin="dense"
            InputProps={{ readOnly: true }}
          />
          <TextField
            label="Пароль API"
            value={nas.api_password ? (showPassword ? nas.api_password : '••••••••') : 'не указан'}
            fullWidth
            margin="dense"
            InputProps={{
              readOnly: true,
              endAdornment: nas.api_password ? (
                <InputAdornment position="end">
                  <IconButton onClick={() => setShowPassword(!showPassword)}>
                    {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                  </IconButton>
                  <IconButton onClick={() => copyToClipboard(nas.api_password)}>
                    <ContentCopyIcon />
                  </IconButton>
                </InputAdornment>
              ) : null,
            }}
          />
          <Typography variant="subtitle1" sx={{ mt: 2 }}>Команда SSH</Typography>
          <TextField
            value={getSshCommand()}
            fullWidth
            margin="dense"
            InputProps={{
              readOnly: true,
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => copyToClipboard(getSshCommand())}>
                    <ContentCopyIcon />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
          {wgSettings && nas.wireguard_pubkey && (
            <>
              <Typography variant="subtitle1" sx={{ mt: 2 }}>WireGuard конфигурация для клиента</Typography>
              <TextField
                multiline
                rows={8}
                value={getWireGuardConfig()}
                fullWidth
                margin="dense"
                InputProps={{
                  readOnly: true,
                  endAdornment: (
                    <InputAdornment position="end" sx={{ alignSelf: 'flex-start', mt: 1 }}>
                      <IconButton onClick={() => copyToClipboard(getWireGuardConfig())} title="Копировать">
                        <ContentCopyIcon />
                      </IconButton>
                      <IconButton onClick={downloadConfig} title="Скачать .conf">
                        <DownloadIcon />
                      </IconButton>
                      {privateKey && (
                        <IconButton onClick={downloadPrivateKey} title="Скачать приватный ключ">
                          <DownloadIcon color="primary" />
                        </IconButton>
                      )}
                    </InputAdornment>
                  ),
                }}
              />
            </>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};

export default NASConnectionInfo;