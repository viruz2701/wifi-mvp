export interface User {
  id: number;
  email: string;
  role: 'admin' | 'venue_owner' | 'marketing' | 'support';
  is_superuser: boolean;
  is_active: boolean;
  venue_id?: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Venue {
  id: number;
  name: string;
  domain?: string;
  ssl_enabled: boolean;
  is_active: boolean;
  description?: string;
  address?: string;
  contact_phone?: string;
  contact_email?: string;
  created_at: string;
  updated_at?: string;
  crm_enabled?: boolean;
  show_email_field?: boolean;
  show_name_field?: boolean;
  show_marketing_consent?: boolean;
  allow_nas_connection_info?: boolean;
}

export interface NASDevice {
  id: number;
  venue_id: number;
  name: string;
  type: 'mikrotik' | 'openwrt' | 'ubiquiti';
  ip_address: string;
  api_username?: string;
  wireguard_pubkey?: string;
  wireguard_ip?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface PortalTemplate {
  id: number;
  venue_id: number;
  type: 'auth' | 'welcome' | 'error';
  html_content: string;
  css_files: string[];
  js_files: string[];
  images: string[];
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Banner {
  id: number;
  venue_id: number;
  image_url: string;
  target_url: string;
  clicks_count: number;
  impressions_count: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UserProfile {
  id: number;
  mac_address: string;
  phone_number?: string;
  email?: string;
  first_seen: string;
  last_seen?: string;
  total_sessions: number;
  total_traffic_bytes: number;
  is_blocked: boolean;
  is_vip: boolean;
  device_oui?: string;
  venue_id?: number;
}

export interface ActivityReportItem {
  day: string;
  sessions: number;
  unique_users: number;
}

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

export interface VenueSocialAction {
  id: number;
  venue_id: number;
  action_id: number;
  reward_tariff_id?: number;
  reward_duration_hours: number;
  created_at: string;
  updated_at?: string;
}

export interface RadiusAttribute {
  id: number;
  name: string;
  vendor_id?: number;
  is_proprietary: boolean;
  description?: string;
  format_hint?: string;
  created_at: string;
  updated_at?: string;
}

export interface TariffRadiusAttribute {
  id: number;
  tariff_id: number;
  attribute: RadiusAttribute;
  value: string;
}