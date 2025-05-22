export class AESVisualizer {
  constructor(keySize, plaintext) {
    this.keySize = keySize;
    this.plaintext = plaintext;
    this.steps = [];
    this.state = Array(16).fill('00');
  }

  async visualize() {
    this.steps = [];
    
    // 1. Генерация ключа (имитация)
    await this.addStep('Инициализация', `Шифрование текста: "${this.plaintext}"`, this.state);
    
    // 2. Дополнение текста
    await this.simulatePadding();
    
    // 3. Преобразование в State matrix
    await this.convertToState();
    
    // 4. Раунды шифрования
    const rounds = this.getRoundsCount();
    
    // Начальное добавление ключа
    await this.addRoundKey('Начальное добавление ключа');
    
    // Основные раунды
    for (let round = 1; round <= rounds; round++) {
      await this.processRound(round, round === rounds);
    }
    
    // Финальный результат
    await this.addStep('Завершение', 'Шифрование завершено', this.state);
    
    return this.steps;
  }

  getRoundsCount() {
    return this.keySize === 128 ? 10 : this.keySize === 192 ? 12 : 14;
  }

  async simulatePadding() {
    const blockSize = 16;
    const padLength = blockSize - (this.plaintext.length % blockSize);
    const paddedText = this.plaintext + String.fromCharCode(padLength).repeat(padLength);
    
    this.addStep('Дополнение данных', `Добавлено ${padLength} байт заполнения`, 
      Array.from({length: 16}, (_, i) => 
        i < this.plaintext.length ? 
          this.plaintext.charCodeAt(i).toString(16).padStart(2, '0') :
          padLength.toString(16).padStart(2, '0')
      )
    );
  }

  async convertToState() {
    const text = this.plaintext.padEnd(16, '\0').slice(0, 16);
    this.state = Array.from(text, c => 
      c.charCodeAt(0).toString(16).padStart(2, '0')
    );
    
    this.addStep('Преобразование в State', 'Текст преобразован в матрицу 4x4', [...this.state]);
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
    await this.addRoundKey(`Раунд ${round}: Добавление ключа`);
  }

  async subBytes(round) {
    // Упрощенная замена байтов (в реальном AES используется S-Box)
    this.state = this.state.map(byte => {
      const val = parseInt(byte, 16);
      // Простое преобразование для демонстрации
      return ((val * 7) % 256).toString(16).padStart(2, '0');
    });
    
    this.addStep(`Раунд ${round}: SubBytes`, 'Каждый байт заменен по таблице замен (S-Box)', [...this.state]);
  }

  async shiftRows(round) {
    // Сдвиг строк в State матрице
    const shifted = [...this.state];
    
    // Строка 1: сдвиг на 1
    for (let i = 1; i < 4; i++) {
      const temp = shifted[i];
      shifted[i] = shifted[i + 4];
      shifted[i + 4] = shifted[i + 8];
      shifted[i + 8] = shifted[i + 12];
      shifted[i + 12] = temp;
    }
    
    this.state = shifted;
    this.addStep(`Раунд ${round}: ShiftRows`, 'Строки матрицы сдвинуты', [...this.state]);
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
    
    this.addStep(`Раунд ${round}: MixColumns`, 'Столбцы матрицы перемешаны', [...this.state]);
  }

  xorBytes(a, b) {
    return (parseInt(a, 16) ^ parseInt(b, 16)).toString(16).padStart(2, '0');
  }

  async addRoundKey(title) {
    // Генерация "псевдоключа" для визуализации
    const roundKey = Array.from({length: 16}, () => 
      Math.floor(Math.random() * 256).toString(16).padStart(2, '0')
    );
    
    // "Применение" ключа
    this.state = this.state.map((byte, i) => 
      this.xorBytes(byte, roundKey[i])
    );
    
    this.addStep(title, 'Раундовый ключ применен к состоянию', [...this.state]);
  }

  addStep(title, description, state = null) {
    this.steps.push({
      title,
      content: description,
      state: state || [...this.state]
    });
    
    // Возвращаем Promise для имитации асинхронности
    return new Promise(resolve => setTimeout(resolve, 100));
  }
}