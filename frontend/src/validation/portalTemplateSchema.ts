import * as yup from 'yup';

export const portalTemplateSchema = yup.object({
  venue_id: yup.number().required('Выберите площадку'),
  type: yup.string().oneOf(['auth', 'welcome', 'error']).required(),
  html_content: yup.string().required('HTML-код не может быть пустым'),
  css_files: yup.array().of(yup.string()),
  js_files: yup.array().of(yup.string()),
  images: yup.array().of(yup.string()),
  is_active: yup.boolean(),
});

export type PortalTemplateFormValues = yup.InferType<typeof portalTemplateSchema>;
