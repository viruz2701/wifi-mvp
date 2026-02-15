import api from './axios';
import { UserProfile } from '@/types';

export const getUserProfiles = (params?: Record<string, any>) =>
  api.get<UserProfile[]>('/user-profiles', { params });
export const getUserProfile = (id: number) => api.get<UserProfile>(`/user-profiles/${id}`);
export const updateUserProfile = (id: number, data: Partial<UserProfile>) =>
  api.put(`/user-profiles/${id}`, data);
export const deleteUserProfile = (id: number) => api.delete(`/user-profiles/${id}`);
