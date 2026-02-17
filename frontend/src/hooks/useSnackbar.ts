import { useSnackbar as useNotistackSnackbar } from 'notistack';

export const useSnackbar = () => {
  const { enqueueSnackbar } = useNotistackSnackbar();

  const showSuccess = (message: string) => {
    enqueueSnackbar(message, { variant: 'success' });
  };

  const showError = (message: string) => {
    enqueueSnackbar(message, { variant: 'error' });
  };

  const showInfo = (message: string) => {
    enqueueSnackbar(message, { variant: 'info' });
  };

  const showWarning = (message: string) => {
    enqueueSnackbar(message, { variant: 'warning' });
  };

  return { showSuccess, showError, showInfo, showWarning };
};