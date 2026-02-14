import * as yup from 'yup';

export const userSchema = yup.object({
  email: yup.string().required('Email обязателен').email('Некорректный email'),
  password: yup.string().when('$isNew', {
    is: true,
    then: (schema) => schema.required('Пароль обязателен').min(6, 'Минимум 6 символов'),
    otherwise: (schema) => schema.notRequired(),
  }),
  role: yup.string().oneOf(['admin', 'venue_owner', 'marketing', 'support']).required(),
  venue_id: yup.number().nullable().when('role', {
    is: 'venue_owner',
    then: (schema) => schema.required('Выберите площадку'),
    otherwise: (schema) => schema.nullable(),
  }),
  is_active: yup.boolean(),
  is_superuser: yup.boolean(),
});

export type UserFormValues = yup.InferType<typeof userSchema>;
