// frontend/src/hooks/useSnackbar.ts
import { useCallback } from 'react';
import { useSnackbar as useNotistackSnackbar } from 'notistack';

export const useSnackbar = () => {
  const { enqueueSnackbar } = useNotistackSnackbar();

  const showSuccess = useCallback((message: string) => {
    enqueueSnackbar(message, { variant: 'success' });
  }, [enqueueSnackbar]);

  const showError = useCallback((message: string) => {
    enqueueSnackbar(message, { variant: 'error' });
  }, [enqueueSnackbar]);

  const showInfo = useCallback((message: string) => {
    enqueueSnackbar(message, { variant: 'info' });
  }, [enqueueSnackbar]);

  const showWarning = useCallback((message: string) => {
    enqueueSnackbar(message, { variant: 'warning' });
  }, [enqueueSnackbar]);

  return { showSuccess, showError, showInfo, showWarning };
};