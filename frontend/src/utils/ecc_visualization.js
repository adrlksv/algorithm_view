export class ECCVisualizer {
  constructor(curveName) {
    this.curveName = curveName;
    this.steps = [];
    this.curveParams = this.getCurveParams();
  }

  getCurveParams() {
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
    return curves[this.curveName] || curves.secp256r1;
  }

  async visualize(progressCallback) {
    this.steps = [];
    const totalSteps = 5; // Базовые шаги
    let currentProgress = 0;
    
    const updateProgress = (step) => {
      currentProgress = step / totalSteps;
      if (progressCallback) progressCallback(currentProgress);
    };

    // 1. Выбор кривой (более подробное описание)
    await this.addStep({
      title: '1. Выбор эллиптической кривой',
      content: `На этом этапе выбирается стандартная эллиптическая кривая ${this.curveParams.name} (${this.curveName})`,
      details: [
        'Эллиптическая кривая - это множество точек, удовлетворяющих уравнению:',
        'y² = x³ + ax + b mod p',
        'Где:',
        '- a, b - параметры кривой',
        '- p - простое число, определяющее конечное поле',
        'Кривая определяет математическую группу, используемую для криптографии'
      ],
      operations: [
        { title: "Уравнение кривой", value: `y² = x³ + ${this.curveParams.a}x + ${this.shortHex(this.curveParams.b)}` },
        { title: "Модуль p", value: this.shortHex(this.curveParams.p), description: "Определяет конечное поле для операций" },
        { title: "Порядок n", value: this.shortHex(this.curveParams.n), description: "Количество точек в подгруппе" },
        { title: "Кофактор h", value: this.curveParams.h, description: "h = #E(F_p)/n, где #E(F_p) - количество точек на кривой" }
      ],
      points: [
        { x: -1.5, y: 0.5, label: 'G', color: '#60a5fa' }
      ]
    });
    updateProgress(1);

    // 2. Базовая точка (более подробное описание)
    await this.addStep({
      title: '2. Выбор базовой точки G',
      content: 'Базовая точка G - это генератор циклической подгруппы точек кривой',
      details: [
        'G имеет порядок n (n×G = O, где O - точка на бесконечности)',
        'Все операции будут выполняться в подгруппе, порожденной точкой G',
        'Эта точка является публичным параметром кривой'
      ],
      operations: [
        { title: "Координата x", value: this.shortHex(this.curveParams.Gx) },
        { title: "Координата y", value: this.shortHex(this.curveParams.Gy) },
        { title: "Порядок точки", value: this.shortHex(this.curveParams.n), description: "n×G = O (точка на бесконечности)" }
      ],
      points: [
        { x: 0, y: 1.2, label: 'G', color: '#60a5fa' }
      ]
    });
    updateProgress(2);

    // 3. Закрытый ключ (более подробное описание)
    const privateKey = this.generateRandomBigInt(this.curveParams.n);
    await this.addStep({
      title: '3. Генерация закрытого ключа d',
      content: 'Закрытый ключ - это случайное целое число в диапазоне [1, n-1]',
      details: [
        'd выбирается случайным образом из диапазона [1, n-1]',
        'Это число должно храниться в строгом секрете',
        'По закрытому ключу вычисляется открытый ключ Q = d×G'
      ],
      operations: [
        { title: "Закрытый ключ d", value: this.shortHex(privateKey.toString(16)), description: "Случайное число от 1 до n-1" },
        { title: "Диапазон значений", value: `1 ≤ d ≤ ${this.shortHex(this.curveParams.n)}` },
        { title: "Битовая длина", value: `${privateKey.toString(2).length} бит` }
      ],
      points: [
        { x: 0, y: 1.2, label: 'G', color: '#60a5fa' },
        { x: 0.5, y: 0.8, label: 'd', color: '#f87171' }
      ]
    });
    updateProgress(3);

    // 4. Открытый ключ (оптимизированное умножение точки)
    await this.visualizePointMultiplication(privateKey, progressCallback, 3, totalSteps);
    
    // 5. Формирование ключей (более подробное описание)
    await this.addStep({
      title: '5. Формирование ключевой пары',
      content: 'Создание ключевой пары в стандартных форматах',
      details: [
        'Закрытый ключ: хранится в защищенном хранилище',
        'Открытый ключ: может свободно распространяться',
        'Форматы:',
        '- PEM: текстовый формат с Base64 кодированием',
        '- DER: бинарный формат',
        '- JWK: JSON Web Key'
      ],
      operations: [
        { title: "Закрытый ключ", value: "Число d в защищенном хранилище", description: "Используется для подписи и расшифрования" },
        { title: "Открытый ключ", value: "Точка Q в формате PEM", description: "Используется для проверки подписи и шифрования" },
        { title: "Безопасность", value: "Основана на сложности ECDLP", description: "Задача дискретного логарифмирования на эллиптической кривой" }
      ],
      points: [
        { x: 0, y: 1.2, label: 'G', color: '#60a5fa' },
        { x: 1.2, y: 0.5, label: 'Q', color: '#4ade80' }
      ]
    });
    updateProgress(totalSteps);

    return {
      steps: this.steps,
      curveParams: {
        a: -3,
        b: 5,
        p: 17 // Упрощенные параметры для визуализации
      }
    };
  }

  async visualizePointMultiplication(privateKey, progressCallback, completedSteps, totalSteps) {
    const binaryKey = privateKey.toString(2);
    const stepsForMultiplication = totalSteps - completedSteps - 1;
    const stepsPerBit = stepsForMultiplication / binaryKey.length;
    
    let currentPoint = { x: 0, y: 1.2 }; // Начальная точка G
    let resultPoint = { x: 0, y: 0 }; // Нейтральный элемент
    
    // Начальный шаг
    await this.addStep({
      title: '4.1 Начало умножения точки',
      content: `Умножение точки G на закрытый ключ d (${this.shortHex(privateKey.toString(16))})`,
      details: [
        'Алгоритм double-and-add:',
        '1. Инициализация: Q = O (точка на бесконечности)',
        '2. Для каждого бита d (начиная со старшего):',
        '   a. Удвоение: Q = 2×Q',
        '   b. Если бит = 1: Q = Q + G',
        '3. Результат: Q = d×G'
      ],
      points: [
        { ...currentPoint, label: 'G', color: '#60a5fa' },
        { ...resultPoint, label: 'Q', color: '#4ade80', visible: false }
      ]
    });

    // Оптимизированный алгоритм double-and-add
    for (let i = 0; i < binaryKey.length; i++) {
      const bit = binaryKey[i];
      
      // Удвоение (только после первого бита)
      if (i > 0) {
        await this.addStep({
          title: `4.${i+1} Удвоение точки (бит ${i+1}/${binaryKey.length})`,
          content: `Удваиваем текущую точку P (2×P)`,
          details: [
            'Формула удвоения точки:',
            'λ = (3x₁² + a) / (2y₁) mod p',
            'x₃ = λ² - 2x₁ mod p',
            'y₃ = λ(x₁ - x₃) - y₁ mod p',
            'Где a - параметр кривой, p - модуль'
          ],
          operation: 'double',
          points: [
            { ...currentPoint, label: 'P', color: '#f59e0b' },
            { ...resultPoint, label: 'Q', color: '#4ade80' }
          ]
        });
        
        currentPoint = this.pointDouble(currentPoint);
      }
      
      // Сложение если бит = 1
      if (bit === '1') {
        await this.addStep({
          title: `4.${i+1} Сложение точек (бит ${i+1} = 1)`,
          content: `Добавляем точку P к результату Q (Q + P)`,
          details: [
            'Формула сложения точек:',
            'λ = (y₂ - y₁) / (x₂ - x₁) mod p',
            'x₃ = λ² - x₁ - x₂ mod p',
            'y₃ = λ(x₁ - x₃) - y₁ mod p',
            'Для P + P используется формула удвоения'
          ],
          operation: 'add',
          points: [
            { ...currentPoint, label: 'P', color: '#f59e0b' },
            { 
              ...(resultPoint.x === 0 && resultPoint.y === 0 ? currentPoint : resultPoint), 
              label: 'Q', 
              color: '#4ade80' 
            }
          ]
        });
        
        resultPoint = this.pointAdd(resultPoint, currentPoint);
      }
      
      // Обновление прогресса
      if (progressCallback) {
        const progress = completedSteps + (i + 1) * stepsPerBit;
        progressCallback(progress / totalSteps);
      }
    }
    
    // Финальный результат
    await this.addStep({
      title: '4. Открытый ключ вычислен',
      content: `Получена точка Q = (${resultPoint.x.toFixed(2)}, ${resultPoint.y.toFixed(2)})`,
      details: [
        'Открытый ключ - это точка Q на эллиптической кривой',
        'Q = d×G, где:',
        '- d - закрытый ключ',
        '- G - базовая точка',
        'Зная Q и G, вычислить d - это сложная задача (ECDLP)'
      ],
      points: [
        { x: 0, y: 1.2, label: 'G', color: '#60a5fa' },
        { ...resultPoint, label: 'Q', color: '#4ade80' }
      ]
    });
  }

  pointAdd(p1, p2) {
    // Упрощенное сложение точек для визуализации
    if (p1.x === 0 && p1.y === 0) return p2;
    if (p2.x === 0 && p2.y === 0) return p1;
    
    // Для демонстрации просто усредняем координаты
    return {
      x: (p1.x + p2.x) / 2,
      y: (p1.y + p2.y) / 2
    };
  }

  pointDouble(p) {
    // Упрощенное удвоение точки для визуализации
    return {
      x: p.x * 1.5,
      y: p.y * 1.5
    };
  }

  shortHex(longHex) {
    if (longHex.length > 20) {
      return `${longHex.substring(0, 10)}...${longHex.substring(longHex.length - 5)}`;
    }
    return longHex;
  }

  generateRandomBigInt(maxHex) {
    if (maxHex.startsWith('0x') || maxHex.startsWith('0X')) {
      maxHex = maxHex.slice(2);
    }
    
    const max = BigInt(`0x${maxHex}`);
    const range = max - 1n;
    const bits = range.toString(2).length;
    let result;
    
    do {
      const randomBits = Array.from({length: bits}, () => 
        Math.random() > 0.5 ? '1' : '0').join('');
      result = BigInt(`0b${randomBits}`);
    } while (result < 1n || result >= max);
    
    return result;
  }

  async addStep(step) {
    this.steps.push(step);
    await new Promise(resolve => setTimeout(resolve, 50));
  }
}