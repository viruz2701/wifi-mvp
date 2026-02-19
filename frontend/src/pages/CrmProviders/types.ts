export type CrmProviderType = 'bitrix24';

export interface Bitrix24Config {
  webhook_url: string;
  field_mapping?: {
    phone?: string;
    email?: string;
    full_name?: string;
    marketing_consent?: string;
  };
}

export type CrmProviderConfig = Bitrix24Config;

export interface CrmProvider {
  id: number;
  name: string;
  type: CrmProviderType;
  config: CrmProviderConfig;
  is_active: boolean;
  priority: number;
  created_at: string;
  updated_at?: string;
}

export interface CrmProviderFormData {
  name: string;
  type: CrmProviderType;
  config: Partial<CrmProviderConfig>;
  is_active: boolean;
  priority: number;
}