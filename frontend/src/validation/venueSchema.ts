import * as yup from 'yup';

export const venueSchema = yup.object({
  name: yup.string().required('Название обязательно').min(2, 'Минимум 2 символа'),
  domain: yup.string().nullable().matches(
    /^[a-z0-9.-]+\.[a-z]{2,}$/,
    'Некорректный домен (например: example.com)'
  ),
  description: yup.string().nullable(),
  address: yup.string().nullable(),
  contact_phone: yup.string().nullable(),
  contact_email: yup.string().nullable().email('Некорректный email'),
  is_active: yup.boolean(),
  ssl_enabled: yup.boolean(),
  crm_enabled: yup.boolean(),
  show_email_field: yup.boolean(),
  show_name_field: yup.boolean(),
  show_marketing_consent: yup.boolean(),
  allow_nas_connection_info: yup.boolean(),
});

export type VenueFormValues = yup.InferType<typeof venueSchema>;
