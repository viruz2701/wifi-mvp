export interface Tariff {
  id: number;
  name: string;
  description?: string;
  price: number;
  currency: string;
  duration_hours: number;
  speed_limit_up_kbps?: number;
  speed_limit_down_kbps?: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface TariffFormData {
  name: string;
  description?: string;
  price: number;
  currency: string;
  duration_hours: number;
  speed_limit_up_kbps?: number;
  speed_limit_down_kbps?: number;
  is_active: boolean;
}