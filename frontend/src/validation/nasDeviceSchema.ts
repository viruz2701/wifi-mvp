import * as yup from 'yup';

export const nasDeviceSchema = yup.object({
  venue_id: yup.number().required('Выберите площадку'),
  name: yup.string().required('Название обязательно').min(2, 'Минимум 2 символа'),
  type: yup.string().oneOf(['mikrotik', 'openwrt', 'ubiquiti']).required(),
  ip_address: yup.string().required('IP адрес обязателен').matches(
    /^(\d{1,3}\.){3}\d{1,3}$/,
    'Некорректный IP адрес'
  ),
  secret: yup.string().required('RADIUS secret обязателен'),
  api_username: yup.string().nullable(),
  api_password: yup.string().nullable(),
  wireguard_pubkey: yup.string().nullable(),
  wireguard_ip: yup.string().nullable(),
  is_active: yup.boolean(),
});

export type NasDeviceFormValues = yup.InferType<typeof nasDeviceSchema>;
