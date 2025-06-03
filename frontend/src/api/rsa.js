import axios from '@/utils/axios';

export const generateRSAKeys = async (keySize = 2048) => {
  const response = await axios.post('/rsa/generate', { key_size: keySize });
  return response.data;
};