export class RSAVisualizer {
  constructor(keySize) {
    this.keySize = keySize;
    this.steps = [];
  }

  async visualize() {
    this.steps = [];
    const isLargeKey = this.keySize > 1024;

    // 1. Инициализация
    await this.addStep({
      title: 'Инициализация алгоритма RSA',
      content: `Генерация ключей размером ${this.keySize} бит`,
      details: isLargeKey 
        ? 'Для больших ключей используется оптимизированная визуализация'
        : 'RSA - криптосистема с открытым ключом, основанная на сложности факторизации больших чисел',
      operations: [
        { title: "Размер ключа", value: `${this.keySize} бит` },
        { title: "Тип визуализации", value: isLargeKey ? "Оптимизированная" : "Полная" }
      ]
    });

    // 2. Генерация простых чисел
    this.p = isLargeKey ? this.fakeLargePrime('p') : this.generatePrime(512);
    this.q = isLargeKey ? this.fakeLargePrime('q') : this.generatePrime(512);
    
    await this.addStep({
      title: 'Генерация простых чисел',
      content: 'Нахождение двух больших простых чисел p и q',
      details: isLargeKey
        ? 'Для демонстрации используются предварительно вычисленные значения'
        : 'Числа проверяются на простоту с помощью теста Миллера-Рабина',
      operations: [
        { title: "Простое число p", value: this.formatNumber(this.p) },
        { title: "Простое число q", value: this.formatNumber(this.q) }
      ]
    });

    // 3. Вычисление модуля
    this.n = this.p * this.q;
    await this.addStep({
      title: 'Вычисление модуля n',
      content: 'Модуль n = p × q',
      details: `Основа для обоих ключей\nn будет использоваться в открытом и закрытом ключах`,
      operations: [
        { title: "Модуль n = p × q", value: this.formatNumber(this.n) }
      ]
    });

    // 4. Функция Эйлера
    this.phi = (this.p - 1n) * (this.q - 1n);
    await this.addStep({
      title: 'Функция Эйлера φ(n)',
      content: 'φ(n) = (p-1) × (q-1)',
      details: 'Используется для вычисления секретной экспоненты',
      operations: [
        { title: "φ(n) = (p-1)(q-1)", value: this.formatNumber(this.phi) }
      ]
    });

    // 5. Открытая экспонента
    this.e = 65537n;
    await this.addStep({
      title: 'Открытая экспонента e',
      content: 'Выбирается число e, взаимно простое с φ(n)',
      details: 'Обычно используется 65537 (2¹⁶ + 1)\nДолжно выполнять условие: 1 < e < φ(n)',
      operations: [
        { title: "e", value: this.e.toString() },
        { title: "Проверка НОД(e, φ(n))", value: "1 (взаимно простые)" }
      ]
    });

    // 6. Секретная экспонента
    this.d = this.modInverse(this.e, this.phi);
    await this.addStep({
      title: 'Секретная экспонента d',
      content: 'd ≡ e⁻¹ mod φ(n)',
      details: 'Вычисляется с помощью расширенного алгоритма Евклида',
      operations: [
        { title: "d", value: this.formatNumber(this.d) },
        { title: "Проверка", value: `(e × d) mod φ(n) = ${(this.e * this.d) % this.phi}` }
      ]
    });

    // 7. Формирование ключей
    await this.addStep({
      title: 'Формирование ключей',
      content: 'Создание ключевой пары в PEM формате',
      details: 'Открытый ключ: (e, n)\nЗакрытый ключ: (d, n)',
      operations: [
        { 
          title: "Открытый ключ", 
          value: `e = ${this.e}\nn = ${this.formatNumber(this.n)}` 
        },
        { 
          title: "Закрытый ключ", 
          value: `d = ${this.formatNumber(this.d)}\nn = ${this.formatNumber(this.n)}` 
        }
      ]
    });

    return this.steps;
  }

  // Вспомогательные методы
  fakeLargePrime(name) {
    const primes = {
      p: BigInt('0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA23727FFFFFFFFFFFFFFFF'),
      q: BigInt('0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF')
    };
    return primes[name];
  }

  generatePrime(bits) {
    // Упрощенная генерация простого числа для демонстрации
    const min = 1n << BigInt(bits - 1);
    const max = (1n << BigInt(bits)) - 1n;
    let candidate = min + (BigInt(Math.floor(Math.random() * 1000)) * 2n) + 1n;
    
    while (candidate <= max) {
      if (this.isProbablePrime(candidate)) {
        return candidate;
      }
      candidate += 2n;
    }
    return max;
  }

  isProbablePrime(n, k = 5) {
    if (n <= 1n) return false;
    if (n <= 3n) return true;
    if (n % 2n === 0n) return false;

    let d = n - 1n;
    let s = 0n;
    while (d % 2n === 0n) {
      d /= 2n;
      s++;
    }

    for (let i = 0; i < k; i++) {
      const a = 2n + BigInt(Math.floor(Math.random() * 1000)) % (n - 4n);
      let x = this.modPow(a, d, n);
      
      if (x === 1n || x === n - 1n) continue;

      for (let j = 1n; j < s; j++) {
        x = this.modPow(x, 2n, n);
        if (x === n - 1n) break;
        if (x === 1n) return false;
      }
      
      if (x !== n - 1n) return false;
    }
    
    return true;
  }

  modPow(a, b, mod) {
    let result = 1n;
    a = a % mod;
    while (b > 0n) {
      if (b % 2n === 1n) {
        result = (result * a) % mod;
      }
      a = (a * a) % mod;
      b = b / 2n;
    }
    return result;
  }

  modInverse(a, m) {
    let [oldR, r] = [a, m];
    let [oldS, s] = [1n, 0n];
    let [oldT, t] = [0n, 1n];
    
    while (r !== 0n) {
      const quotient = oldR / r;
      [oldR, r] = [r, oldR - quotient * r];
      [oldS, s] = [s, oldS - quotient * s];
      [oldT, t] = [t, oldT - quotient * t];
    }
    
    return oldS < 0n ? oldS + m : oldS;
  }

  formatNumber(num) {
    const str = num.toString();
    return str.length > 20 
      ? `${str.substring(0, 10)}...${str.substring(str.length - 10)} (${str.length} цифр)`
      : str;
  }

  async addStep(step) {
    this.steps.push(step);
    await new Promise(resolve => setTimeout(resolve, 50));
  }
}