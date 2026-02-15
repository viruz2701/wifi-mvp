import api from './axios';
import { User } from '@/types';

export const getUsers = () => api.get<User[]>('/users');
export const getUser = (id: number) => api.get<User>(`/users/${id}`);
export const createUser = (data: Partial<User> & { password: string }) => api.post('/users', data);
export const updateUser = (id: number, data: Partial<User>) => api.put(`/users/${id}`, data);
export const deleteUser = (id: number) => api.delete(`/users/${id}`);