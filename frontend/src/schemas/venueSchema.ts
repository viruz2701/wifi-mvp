// frontend/src/schemas/venueSchema.ts
import * as yup from 'yup';

export const venueSchema = yup.object({
  name: yup.string().required('Название обязательно'),
  domain: yup.string().nullable(),
  description: yup.string().nullable(),
  address: yup.string().nullable(),
  contact_phone: yup.string().nullable(),
  contact_email: yup.string().email('Некорректный email').nullable(),
  is_active: yup.boolean(),
  ssl_enabled: yup.boolean(),
}).required();