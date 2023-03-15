import logging
import random
import math


# Скорость передачи информации
def InformationTransfer(t, inf):
    J = (1.0 / t * 4) * inf
    return round(J, 4)


# Энтропия утечки
def LeakEntropy(kmi, receiver, sender):
    H = 0.0
    Receive = list(receiver.values())
    Send = list(sender.values())
    for receive in range(0, len(kmi[0])):
        Sum = 0.0
        for sent in range(0, len(kmi)):
            t = kmi[sent][receive] * Send[sent] / Receive[receive]
            if t != 0:
                Sum += t * math.log2(t)
        H -= Sum * Receive[receive]
    return round(H, 4)


# Апостериорная энтропия шума
def NoiseEntropy(kmi, reality):
    H = 0.0
    Reality = list(reality.values())
    for sent in range(0, len(kmi)):
        Sum = 0
        for receive in range(0, len(kmi[sent])):
            if kmi[sent][receive] != 0:
                Sum += kmi[sent][receive] * math.log2(kmi[sent][receive])
            else:
                continue
        H -= Sum * Reality[sent]
    return round(H, 4)


# Апостериорная энтропия источника
def Entropy(reality):
    H = 0.0
    for x in reality:
        H += reality[x] * math.log2(reality[x])
    return round(-H, 4)


# Моделирование приема сообщения.
def MessageReceive(KMI, ProbToSend):
    Receive = []
    Send = list(ProbToSend.values())
    for receive in range(0, len(KMI[0])):
        Sum = 0
        for sent in range(0, len(KMI)):
            Sum += KMI[sent][receive] * Send[sent]
        Receive.append(Sum)
    Received = {
        'a': Receive[0],
        'e': Receive[1],
        "i": Receive[2],
        "o": Receive[3],
        "n": Receive[4],
        "r": Receive[5],
        "t": Receive[6],
        "l": Receive[7],
        "?": Receive[8]
    }
    return Received


# Функция поиска значения внутри списка
def FindElem(elem, array):
    for i in range(0, len(array)):
        if array[i] == elem:
            return i
    return len(array) + 1


# Для нахождения суммы по строке (для апостериорной КМИ)
def RowSum(array):
    Sum = 0
    for i in range(0, len(array)):
        Sum += array[i]
    return Sum


# Моделирование отправки сообщения.
def MessageGenerate(symbols, p):
    K = 300  # Размер пакета из символов
    t0 = 0.3  # Время передачи одного разряда
    KMI = [[0] * (len(symbols) + 1) for i in range(len(symbols))]  # Матрица размером N x N + 1
    SymbolProb = {  # Словарь содержит символ и его вероятность. Логика следующая:
        # Если символ входит в промежуток между a и b - сгенерирован символ a.
        'a': 0.1888,
        'e': 0.3597,
        "i": 0.4946,
        "o": 0.6271,
        "n": 0.7349,
        "r": 0.8213,
        "t": 0.9060,
        "l": 1.0,
    }
    Reality = {
        'a': 0.0,
        'e': 0.0,
        "i": 0.0,
        "o": 0.0,
        "n": 0.0,
        "r": 0.0,
        "t": 0.0,
        "l": 0.0,
    }
    Symb = list(symbols.keys())  # Для удобной индексации
    Codes = list(symbols.values())
    # print(KMI)
    for i in range(0, K):
        Rand = round(random.random(), 4)
        if SymbolProb["a"] > Rand:
            Reality["a"] += 1
        if SymbolProb["a"] < Rand < SymbolProb["e"]:
            Reality["e"] += 1
        if SymbolProb["e"] < Rand < SymbolProb["i"]:
            Reality["i"] += 1
        if SymbolProb["i"] < Rand < SymbolProb["o"]:
            Reality["o"] += 1
        if SymbolProb["o"] < Rand < SymbolProb["n"]:
            Reality["n"] += 1
        if SymbolProb["n"] < Rand < SymbolProb["r"]:
            Reality["r"] += 1
        if SymbolProb["r"] < Rand < SymbolProb["t"]:
            Reality["t"] += 1
        if SymbolProb["t"] < Rand < SymbolProb["l"]:
            Reality["l"] += 1
    index_i = 0
    for x in Reality:
        for i in range(0, int(Reality[x])):
            SymbolCode = symbols[x]
            result = ""
            for j in range(0, len(SymbolCode)):
                rand = round(random.random(), 3)
                if SymbolCode[j] == "0" and rand <= 0.66:
                    result += "0"
                elif SymbolCode[j] == "0" and rand > 0.67:
                    result += "1"
                elif SymbolCode[j] == "1" and rand <= 0.65:
                    result += "1"
                elif SymbolCode[j] == "1" and rand > 0.66:
                    result += "0"
            # print(result)  # До данного момента всё работает исправно
            if result in Codes:
                KMI[index_i][FindElem(result, Codes)] += 1
            else:

                KMI[index_i][len(symbols)] += 1
        index_i += 1
    for x in Reality:
        Reality[x] /= 300.0
    for i in range(0, len(KMI)):
        Sum = RowSum(KMI[i])
        for j in range(0, len(KMI[i])):
            KMI[i][j] /= float(Sum)
            KMI[i][j] = round(KMI[i][j], 3)
    # print(KMI)
    return Reality, KMI


# Функция суммы по строке для нахождения последнего элемента в строке КМИ.
def SumOfRow(matrix, index):
    Sum = 0
    for i in matrix[index]:
        Sum += i
    print(round((1 - Sum), 4), end="")
    matrix[index][8] = round((1 - Sum), 4)


# Функция, которая выводит КМИ и записывает ее в матрицу.
def FindMatrix(symbols, p):
    KMI = [[0] * (len(symbols) + 1) for i in range(len(symbols))]
    """
    Канальная матрица источника. Первые 8 элементов в строке — вероятности
    перехода в известные символы. Последний элемент - в неизвестный.
    len(symbols) + 1 - учитывает все наши символы алфавита + неизвестные переходы.
    len(symbols) - количество строк в матрице.
    """
    result = 1
    print("   \t\t\t\t", end=" ")  # Быстрое и эффективное начало строки :)
    for x in symbols:
        print(f"{x:9}", end="")
    print("?", end="")
    print()
    index_i = 0
    index_j = 0
    for x in symbols:  # Пробег по словарю
        print(str(x) + " \t " + str(symbols[x]) + "  ", end=" ")  # Чтобы было понятно, какой символ и где стоит.
        index_j = 0
        for y in symbols:  # Каждый элемент с каждым
            for i in range(0, 4):  # Начало сравнения
                key = symbols[x][i] + symbols[y][i]  # Создаем ключ перехода.
                result *= p.get(key)  # Получаем по ключу значение. 00 - ноль перешел в ноль. Умножаем на результат.
            print(f"{round(result, 4):1.4f}  ", end=" ")  # Форматированный вывод
            KMI[index_i][index_j] = round(result, 4)
            result = 1  # Для следующих подсчетов.
            index_j += 1  # Увеличиваем индекс по строке.
        SumOfRow(KMI, index_i)  # Получаем значение последнего элемента. Из свойств КМИ, сумма по строке равна 1.
        index_i += 1  # Увеличиваем индекс по столбцу.
        print()
    return KMI


def FindKMO(kmi, reality, symbols):
    KMO = [[0] * (len(reality) + 1) for i in range(len(reality))]
    Reality = list(reality.values())
    for i in range(0, len(kmi)):
        for j in range(0, len(kmi[i])):
            KMO[i][j] = Reality[i] * kmi[i][j]
    print("   \t\t\t\t", end=" ")  # Быстрое и эффективное начало строки :)
    for x in symbols:
        print(f"{x:9}", end="")
    print("?", end="")
    print()
    syms = list(symbols.keys())
    codes = list(symbols.values())
    for i in range(0, len(KMO)):
        print(f"{syms[i]} \t{codes[i]} ", end="\t")
        for j in range(0, len(KMO[i])):
            print(f"{round(KMO[i][j], 4):1.4f}  ", end=" ")
        print()
    return KMO


def PrintKMI(kmi, symbols):
    syms = list(symbols.keys())
    codes = list(symbols.values())
    for i in range(0, len(kmi)):
        print(f"{syms[i]} \t{codes[i]} ", end="\t")
        for j in range(0, len(kmi[i])):
            print(f"{round(kmi[i][j], 4):1.4f}  ", end=" ")
        print()


def main():
    # Словарь для хранения символа и его кодовой последовательности.
    dictionary = {
        'a': "0001",
        'e': "0010",
        "i": "0011",
        "o": "0100",
        "n": "0101",
        "r": "0110",
        "t": "0111",
        "l": "1000",

    }
    # Словарь для хранения вероятностей перехода. Первый символ - был, второй - перешел.
    inv = {
        "00": 0.66,
        "01": 0.34,
        "10": 0.35,
        "11": 0.65
    }
    Reality = {}
    # Нахождение КМИ
    print(8 * "\t" + " АПРИОРНАЯ Канальная матрица источника")  # Питон может всё...
    AprKMI = FindMatrix(dictionary, inv)
    # Нахождение апостериорной КМИ
    Reality, KMI = MessageGenerate(dictionary, inv)  # Генератор входных сообщений
    print(8 * "\t" + " АПОСТЕРИОРНАЯ Канальная матрица источника")
    PrintKMI(KMI, dictionary)
    print("\t\t Апостериорные вероятности входных сообщений ")
    for x in Reality:
        print(f"{x} : {Reality[x]:1.5f}")
    print()
    Receive = MessageReceive(KMI, Reality)
    print("\t\t Апостериорные вероятности выходных сообщений ")
    for x in Receive:
        print(f"{x} : {Receive[x]:1.5f}")
    print()
    SourceEntropy = Entropy(Reality)
    print(f"Апостериорная энтропия источника: {SourceEntropy}")
    ReceiverEntropy = Entropy(Receive)
    print(f"Апостериорная энтропия приемника: {ReceiverEntropy}")
    Noise = NoiseEntropy(KMI, Reality)
    print(f"Апостериорная энтропия шума: {Noise}")
    Leak = LeakEntropy(KMI, Receive, Reality)
    print(f"Апостериорная энтропия утечки: {Leak}")
    print(f"Количество полезной информации (энтропия приемника - шум): {round(ReceiverEntropy - Noise, 4)}")
    print(f"Количество полезной информации (энтропия источника - утечка): {round(SourceEntropy - Leak, 4)}")
    t = 0.0003  # 0.3 мс = 0.0003 с
    print(f"Скорость передачи информации: {InformationTransfer(t, round(ReceiverEntropy - Noise, 4))}")
    print(8 * "\t" + " Канальная матрица объединения")  # Питон может всё...
    KMO = FindKMO(KMI, Reality, dictionary)


# Точка входа в основную программу
main()
