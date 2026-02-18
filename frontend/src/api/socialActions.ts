import api from './axios';
import { SocialAction, VenueSocialAction } from '@/types';

export const getSocialActions = () => api.get<SocialAction[]>('/social/actions');

export const getVenueSocialActions = (venueId: number) =>
  api.get<VenueSocialAction[]>(`/social/venue/${venueId}/actions`);

export const addVenueSocialAction = (venueId: number, data: Partial<VenueSocialAction>) =>
  api.post(`/social/venue/${venueId}/actions`, { ...data, venue_id: venueId });

export const updateVenueSocialAction = (id: number, data: Partial<VenueSocialAction>) =>
  api.put(`/social/venue/actions/${id}`, data);

export const deleteVenueSocialAction = (id: number) =>
  api.delete(`/social/venue/actions/${id}`);