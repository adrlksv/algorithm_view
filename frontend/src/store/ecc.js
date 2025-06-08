import { defineStore } from 'pinia';
import { generateECCKeys } from '../api/ecc';

export const useECCStore = defineStore('ecc', {
  state: () => ({
    privateKey: '',
    publicKey: '',
    curveName: 'secp256r1',
    loading: false,
    error: null,
    steps: []
  }),
  actions: {
    async generateKeys(curveName = 'secp256r1') {
      this.loading = true;
      this.error = null;
      this.curveName = curveName;
      
      try {
        const result = await generateECCKeys(curveName);
        this.privateKey = result.private_key;
        this.publicKey = result.public_key;
        
        return true;
      } catch (error) {
        this.error = error.message;
        console.error('ECC generation error:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    async addStep(step) {
      this.steps.push(step);
      await new Promise(resolve => setTimeout(resolve, 500));
    },
    
    resetSteps() {
      this.steps = [];
    }
  },
  
  getters: {
    curveParams: (state) => {
      const curves = {
        'secp256r1': {
          name: 'NIST P-256',
          a: -3,
          b: '0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b',
          p: '0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff',
          n: '0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551',
          h: 1,
          Gx: '0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296',
          Gy: '0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5'
        },
        'secp384r1': {
          name: 'NIST P-384',
          a: -3,
          b: '0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef',
          p: '0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff',
          n: '0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973',
          h: 1,
          Gx: '0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7',
          Gy: '0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f'
        },
        'secp521r1': {
          name: 'NIST P-521',
          a: -3,
          b: '0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00',
          p: '0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
          n: '0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409',
          h: 1,
          Gx: '0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66',
          Gy: '0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650'
        }
      };
      
      return curves[state.curveName] || curves.secp256r1;
    }
  }
});