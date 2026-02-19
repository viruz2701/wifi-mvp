// Типы провайдеров, которые приходят с бэкенда
export type SmsProviderType = 'rocketsms' | 'callpassword' | 'websms';

// Конфигурация для RocketSMS
export interface RocketSmsConfig {
  username: string;
  password_md5: string;
  sender?: string;
}

// Конфигурация для CallPassword
export interface CallPasswordConfig {
  api_key?: string;
  api_secret?: string;
  timeout?: number;
}

// Конфигурация для WebSMS.by
export interface WebSmsConfig {
  user: string;
  apikey: string;
  sender?: string;
}

// Объединённый тип конфигурации
export type SmsProviderConfig = RocketSmsConfig | CallPasswordConfig | WebSmsConfig;

// Основной тип провайдера
export interface SmsProvider {
  id: number;
  name: string;
  type: SmsProviderType;
  config: SmsProviderConfig;
  is_active: boolean;
  priority?: number;
  created_at: string;
  updated_at?: string;
}

// Для форм создания/редактирования
export interface SmsProviderFormData {
  name: string;
  type: SmsProviderType;
  config: Partial<SmsProviderConfig>;
  is_active: boolean;
  priority?: number;
}