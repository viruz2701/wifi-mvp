import * as yup from 'yup';

export const nasDeviceSchema = yup.object({
  venue_id: yup.number().required('Выберите площадку'),
  name: yup.string().required('Название обязательно').min(2, 'Минимум 2 символа'),
  type: yup.string().oneOf(['mikrotik', 'openwrt', 'ubiquiti']).required(),
  ip_address: yup.string().required('IP адрес обязателен').matches(
    /^(\d{1,3}\.){3}\d{1,3}$/,
    'Некорректный IP адрес'
  ),
  secret: yup.string().when('$isNew', {
    is: true,
    then: (schema) => schema.required('RADIUS secret обязателен'),
    otherwise: (schema) => schema.notRequired(),
  }),
  api_username: yup.string().nullable(),
  api_password: yup.string().nullable(),
  wireguard_pubkey: yup.string().when(['generate_wireguard_keys', '$isNew'], {
    is: (generate: boolean, isNew: boolean) => !generate && isNew,
    then: (schema) => schema.required('Публичный ключ обязателен при ручном вводе'),
    otherwise: (schema) => schema.nullable(),
  }),
  wireguard_ip: yup.string().nullable(), // оставляем для совместимости, но в форме не используется
  is_active: yup.boolean(),
  generate_wireguard_keys: yup.boolean(),
});

export type NasDeviceFormValues = yup.InferType<typeof nasDeviceSchema>;