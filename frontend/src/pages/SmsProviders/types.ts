// Типы провайдеров, которые приходят с бэкенда
export type SmsProviderType = 'rocketsms' | 'callpassword';

// Конфигурация для RocketSMS
export interface RocketSmsConfig {
  username: string;
  password_md5: string;
  sender?: string;
}

// Конфигурация для CallPassword (будет расширяться)
export interface CallPasswordConfig {
  api_key?: string; // placeholder, позже заменим на реальные поля
  [key: string]: any;
}

// Основной тип провайдера
export interface SmsProvider {
  id: number;
  name: string;
  type: SmsProviderType;
  config: RocketSmsConfig | CallPasswordConfig | Record<string, any>;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

// Для форм создания/редактирования
export interface SmsProviderFormData {
  name: string;
  type: SmsProviderType;
  config: Record<string, any>;
  is_active: boolean;
}