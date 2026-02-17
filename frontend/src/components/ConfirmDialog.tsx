import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button } from '@mui/material';

interface ConfirmDialogProps {
  open: boolean;
  title?: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

export const ConfirmDialog = ({ open, title = 'Подтверждение', message, onConfirm, onCancel }: ConfirmDialogProps) => (
  <Dialog open={open} onClose={onCancel}>
    <DialogTitle>{title}</DialogTitle>
    <DialogContent>
      <DialogContentText>{message}</DialogContentText>
    </DialogContent>
    <DialogActions>
      <Button onClick={onCancel}>Отмена</Button>
      <Button onClick={onConfirm} color="error" variant="contained">Удалить</Button>
    </DialogActions>
  </Dialog>
);