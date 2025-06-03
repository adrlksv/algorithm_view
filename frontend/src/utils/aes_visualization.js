export class AESVisualizer {
  constructor(keySize, plaintext) {
    this.keySize = keySize;
    this.plaintext = plaintext;
    this.steps = [];
    this.state = Array(16).fill('00');
    this.roundKeys = this.generateRoundKeys();
  }

  async visualize() {
    this.steps = [];
    
    // 1. Инициализация
    await this.addStep('Инициализация', 
      `Начало шифрования текста: "${this.plaintext}" с ключом ${this.keySize} бит`,
      this.state,
      `Размер ключа: ${this.keySize} бит\nКоличество раундов: ${this.getRoundsCount()}`
    );
    
    // 2. Дополнение текста
    await this.simulatePadding();
    
    // 3. Преобразование в State matrix
    await this.convertToState();
    
    // 4. Раунды шифрования
    const rounds = this.getRoundsCount();
    
    // Начальное добавление ключа
    await this.addRoundKey(0, 'Начальное добавление ключа');
    
    // Основные раунды
    for (let round = 1; round <= rounds; round++) {
      await this.processRound(round, round === rounds);
    }
    
    // Финальный результат
    await this.addStep('Завершение', 
      'Шифрование завершено. Получен финальный зашифрованный блок.', 
      this.state,
      `Финальный зашифрованный текст: ${this.state.join(' ')}`
    );
    
    return this.steps;
  }

  getRoundsCount() {
    return this.keySize === 128 ? 10 : this.keySize === 192 ? 12 : 14;
  }

  generateRoundKeys() {
    const rounds = this.getRoundsCount() + 1; // +1 для начального ключа
    const keys = [];
    
    // Генерация псевдослучайных ключей для визуализации
    for (let i = 0; i < rounds; i++) {
      keys.push(Array.from({length: 16}, () => 
        Math.floor(Math.random() * 256).toString(16).padStart(2, '0')
      ));
    }
    
    return keys;
  }

  async simulatePadding() {
    const blockSize = 16;
    const padLength = blockSize - (this.plaintext.length % blockSize);
    const paddedText = this.plaintext + String.fromCharCode(padLength).repeat(padLength);
    
    const paddedState = Array.from({length: 16}, (_, i) => 
      i < this.plaintext.length ? 
        this.plaintext.charCodeAt(i).toString(16).padStart(2, '0') :
        padLength.toString(16).padStart(2, '0')
    );
    
    this.addStep('Дополнение данных (Padding)', 
      `Текст дополнен до кратного 16 байтам. Добавлено ${padLength} байт заполнения.`,
      paddedState,
      `Исходная длина: ${this.plaintext.length} байт\nДобавлено: ${padLength} байт\nНовая длина: ${paddedText.length} байт`
    );
    
    this.state = paddedState;
  }

  async convertToState() {
    const text = this.plaintext.padEnd(16, '\0').slice(0, 16);
    this.state = Array.from(text, c => 
      c.charCodeAt(0).toString(16).padStart(2, '0')
    );
    
    this.addStep('Преобразование в State Matrix', 
      'Текст преобразован в матрицу состояний 4x4 (16 байт)',
      [...this.state],
      'State Matrix представляет собой двумерный массив 4x4 байта,\nгде каждый байт исходного текста занимает свою позицию.'
    );
  }

  async processRound(round, isFinalRound) {
    // SubBytes
    await this.subBytes(round);
    
    // ShiftRows
    await this.shiftRows(round);
    
    // MixColumns (кроме последнего раунда)
    if (!isFinalRound) {
      await this.mixColumns(round);
    }
    
    // AddRoundKey
    await this.addRoundKey(round, `Раунд ${round}: Добавление ключа раунда`);
  }

  async subBytes(round) {
    // Упрощенная замена байтов (в реальном AES используется S-Box)
    const newState = this.state.map(byte => {
      const val = parseInt(byte, 16);
      // Простое преобразование для демонстрации
      return ((val * 7 + 99) % 256).toString(16).padStart(2, '0');
    });
    
    this.state = newState;
    this.addStep(`Раунд ${round}: SubBytes`, 
      'Каждый байт заменен по таблице замен (S-Box). Это нелинейная замена байтов,\nкоторая обеспечивает стойкость алгоритма к криптоанализу.',
      [...this.state],
      'S-Box преобразует каждый байт состояния независимо,\nиспользуя специальную таблицу замен.'
    );
  }

  async shiftRows(round) {
    // Сдвиг строк в State матрице
    const shifted = [...this.state];
    
    // Строка 1: сдвиг на 1
    [shifted[1], shifted[5], shifted[9], shifted[13]] = 
      [shifted[5], shifted[9], shifted[13], shifted[1]];
    
    // Строка 2: сдвиг на 2
    [shifted[2], shifted[6], shifted[10], shifted[14]] = 
      [shifted[10], shifted[14], shifted[2], shifted[6]];
    
    // Строка 3: сдвиг на 3
    [shifted[3], shifted[7], shifted[11], shifted[15]] = 
      [shifted[15], shifted[3], shifted[7], shifted[11]];
    
    this.state = shifted;
    this.addStep(`Раунд ${round}: ShiftRows`, 
      'Строки матрицы сдвинуты циклически:\n- Строка 0 не сдвигается\n- Строка 1 сдвигается на 1 позицию\n- Строка 2 сдвигается на 2 позиции\n- Строка 3 сдвигается на 3 позиции',
      [...this.state],
      'ShiftRows обеспечивает "размазывание" байтов по матрице состояния,\nчто увеличивает диффузию в алгоритме.'
    );
  }

  async mixColumns(round) {
    // Упрощенное перемешивание столбцов
    for (let col = 0; col < 4; col++) {
      const start = col * 4;
      const colBytes = this.state.slice(start, start + 4);
      
      // Простое преобразование для демонстрации
      const mixed = [
        this.xorBytes(colBytes[0], colBytes[1]),
        this.xorBytes(colBytes[1], colBytes[2]),
        this.xorBytes(colBytes[2], colBytes[3]),
        this.xorBytes(colBytes[3], colBytes[0])
      ];
      
      for (let i = 0; i < 4; i++) {
        this.state[start + i] = mixed[i];
      }
    }
    
    this.addStep(`Раунд ${round}: MixColumns`, 
      'Каждый столбец матрицы состояния умножается на фиксированную матрицу\nв конечном поле GF(2^8). Это обеспечивает диффузию между байтами.',
      [...this.state],
      'MixColumns преобразует каждый столбец матрицы состояния независимо,\nиспользуя умножение матриц в конечном поле.'
    );
  }

  xorBytes(a, b) {
    return (parseInt(a, 16) ^ parseInt(b, 16)).toString(16).padStart(2, '0');
  }

  async addRoundKey(round, title) {
    const roundKey = this.roundKeys[round];
    
    // "Применение" ключа
    const newState = this.state.map((byte, i) => 
      this.xorBytes(byte, roundKey[i])
    );
    
    this.state = newState;
    this.addStep(title, 
      `Ключ раунда ${round} применен к состоянию с помощью операции XOR.`,
      [...this.state],
      `Ключ раунда:\n${this.formatKeyForDisplay(roundKey)}`
    );
  }

  formatKeyForDisplay(key) {
    return key.reduce((acc, byte, i) => {
      if (i % 4 === 0) acc += '\n';
      acc += byte + ' ';
      return acc;
    }, '').trim();
  }

  addStep(title, content, state = null, details = '', extra = '') {
    const step = {
      title,
      content,
      state: state || [...this.state],
      details,
      extra
    };
    
    if (title.includes('Раунд')) {
      const roundMatch = title.match(/Раунд (\d+)/);
      if (roundMatch) step.round = parseInt(roundMatch[1]);
    }
    
    this.steps.push(step);
    
    // Возвращаем Promise для имитации асинхронности
    return new Promise(resolve => setTimeout(resolve, 100));
  }
}