import axios from '@/utils/axios';

export const generateAESKey = async (keySize = 256, sampleText = "Test message") => {
  const response = await axios.post('http://localhost:8000/aes/generate', { key_size: keySize, sample_text: sampleText });
  return response.data;
};
