import axios from '@/utils/axios';

export const generateRSAKeys = async (keySize = 2048) => {
  const response = await axios.post('/rsa/generate', null, {
    params: {key_size: keySize}
  });
  return response.data;
};