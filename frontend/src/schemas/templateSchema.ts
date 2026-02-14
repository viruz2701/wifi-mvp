import * as yup from 'yup';

export const templateSchema = yup.object({
  venue_id: yup.number().required('Выберите площадку'),
  type: yup.string().oneOf(['auth', 'welcome', 'error']).required('Выберите тип'),
  html_content: yup.string().required('HTML-код обязателен'),
  is_active: yup.boolean(),
}).required();