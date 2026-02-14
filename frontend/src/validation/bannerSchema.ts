import * as yup from 'yup';

export const bannerSchema = yup.object({
  venue_id: yup.number().required('Выберите площадку'),
  target_url: yup.string().required('URL перехода обязателен').url('Некорректный URL'),
  image_url: yup.string().nullable(),
  is_active: yup.boolean(),
});

export type BannerFormValues = yup.InferType<typeof bannerSchema>;
