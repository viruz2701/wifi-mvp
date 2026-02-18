export type SocialActionType = 'like' | 'share' | 'subscribe' | 'follow';
export type SocialNetwork = 'vk' | 'telegram' | 'instagram' | 'facebook' | 'viber';

export interface SocialAction {
  id: number;
  name: string;
  description?: string;
  type: SocialActionType;
  network: SocialNetwork;
  config: Record<string, any>;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface SocialActionFormData {
  name: string;
  description?: string;
  type: SocialActionType;
  network: SocialNetwork;
  config: Record<string, any>;
  is_active: boolean;
}

export interface VenueSocialAction {
  id: number;
  venue_id: number;
  action_id: number;
  reward_tariff_id?: number;
  reward_duration_hours: number;
  created_at: string;
  updated_at?: string;
}