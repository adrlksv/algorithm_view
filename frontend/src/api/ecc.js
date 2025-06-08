// api/ecc.js
import axios from '@/utils/axios';

export const generateECCKeys = async (curveName = 'secp256r1') => {
  const response = await axios.post('http://localhost:8000/ecc/generate', { curve_name: curveName });
  return response.data;
};