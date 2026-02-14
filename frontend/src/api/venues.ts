import api from './axios';
import { Venue } from '@/types';

export const getVenues = () => api.get<Venue[]>('/venues');
export const getVenue = (id: number) => api.get<Venue>(`/venues/${id}`);
export const createVenue = (data: Partial<Venue>) => api.post('/venues', data);
export const updateVenue = (id: number, data: Partial<Venue>) => api.put(`/venues/${id}`, data);
export const deleteVenue = (id: number) => api.delete(`/venues/${id}`);