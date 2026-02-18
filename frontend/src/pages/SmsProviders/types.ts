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
  user: string;          // логин (номер телефона)
  apikey: string;        // API ключ
  sender?: string;       // опциональное альфа-имя
}

// Основной тип провайдера
export interface SmsProvider {
  id: number;
  name: string;
  type: SmsProviderType;
  config: RocketSmsConfig | CallPasswordConfig | WebSmsConfig | Record<string, any>;
  is_active: boolean;
  priority?: number;      // приоритет (меньше = выше)
  created_at: string;
  updated_at?: string;
}

// Для форм создания/редактирования
export interface SmsProviderFormData {
  name: string;
  type: SmsProviderType;
  config: Record<string, any>;
  is_active: boolean;
  priority?: number;      // опционально, можно добавить в форму позже
}