// src/pages/SocialActions/types.ts

export type SocialActionType = 'like' | 'share' | 'subscribe' | 'follow';
export type SocialNetwork = 'vk' | 'telegram' | 'instagram' | 'facebook' | 'viber';

// Конфигурация для VK
export interface VkConfig {
  group_id: string;
  access_token: string;
}

// Конфигурация для Telegram
export interface TelegramConfig {
  channel_id: string;
  bot_token: string;
}

// Конфигурация для Viber
export interface ViberConfig {
  bot_token: string;
  bot_name?: string;
}

// Заглушки для Instagram и Facebook (можно расширить позже)
export interface InstagramConfig {
  // Добавить поля по мере необходимости
  [key: string]: unknown;
}

export interface FacebookConfig {
  // Добавить поля по мере необходимости
  [key: string]: unknown;
}

// Объединённый тип конфигурации
export type SocialActionConfig = VkConfig | TelegramConfig | ViberConfig | InstagramConfig | FacebookConfig;

// Основной тип социальной акции (из бэкенда)
export interface SocialAction {
  id: number;
  name: string;
  description?: string;
  type: SocialActionType;
  network: SocialNetwork;
  config: SocialActionConfig;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

// Тип для формы создания/редактирования
export interface SocialActionFormData {
  name: string;
  description?: string;
  type: SocialActionType;
  network: SocialNetwork;
  config: Partial<SocialActionConfig>;
  is_active: boolean;
}