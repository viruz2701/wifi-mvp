import api from './axios';
import { NASDevice } from '@/types';

export const getNasDevices = (params?: any) => api.get<NASDevice[]>('/nas-devices', { params });
export const getNasDevice = (id: number) => api.get<NASDevice>(`/nas-devices/${id}`);
export const createNasDevice = (data: Partial<NASDevice>) => api.post('/nas-devices', data);
export const updateNasDevice = (id: number, data: Partial<NASDevice>) => api.put(`/nas-devices/${id}`, data);
export const deleteNasDevice = (id: number) => api.delete(`/nas-devices/${id}`);