export interface RadiusAttribute {
  id: number;
  name: string;
  vendor_id?: number | null;
  is_proprietary: boolean;
  description?: string;
  format_hint?: string;
  created_at: string;
  updated_at?: string;
}

export interface RadiusAttributeFormData {
  name: string;
  vendor_id?: number | null;
  is_proprietary: boolean;
  description?: string;
  format_hint?: string;
}