import api from './axios';
import { Banner } from '@/types';

export const getBanners = (venueId?: number) => {
  const params = venueId ? { venue_id: venueId } : {};
  return api.get<Banner[]>('/banners', { params });
};
export const getBanner = (id: number) => api.get<Banner>(`/banners/${id}`);
export const createBanner = (data: Partial<Banner>) => api.post('/banners', data);
export const updateBanner = (id: number, data: Partial<Banner>) => api.put(`/banners/${id}`, data);
export const deleteBanner = (id: number) => api.delete(`/banners/${id}`);
// Функция для загрузки изображения (используется отдельно, но можно добавить для удобства)
export const uploadBannerImage = (id: number, file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/banners/${id}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};