import * as yup from 'yup';

export const userProfileSchema = yup.object({
  is_blocked: yup.boolean(),
  is_vip: yup.boolean(),
});

export type UserProfileFormValues = yup.InferType<typeof userProfileSchema>;
