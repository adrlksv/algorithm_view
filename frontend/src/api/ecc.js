import axios from '@/utils/axios';

export const generateECCKeys = async (curveName = 'secp256r1') => {
  const response = await axios.post('/ecc/generate', null, {
    params: {
      curve_name: curveName
    }
  });
  return response.data;
};