import random
import math


# Скорость передачи информации
def InformationTransfer(t, inf):
    J = (inf / (t * 7))
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


# Функция нахождения кодового расстояние между последовательностями.
def CodeDistance(coded_first, coded_second):
    counter = 0
    for i in range(0, len(coded_first)):
        if coded_first[i] == coded_second[i]:
            counter += 1
    #print(f"First = {coded_first}  Second = {coded_second}  Distance = {len(coded_first) - counter}")
    return len(coded_first) - counter


# Функция суммы по строке для нахождения последнего элемента в строке КМИ.
def SumOfRow(matrix, index):
    Sum = 0
    for i in matrix[index]:
        Sum += i
    #print(round((1 - Sum), 4), end="")
    #matrix[index][len(matrix) - 1] = round((1 - Sum), 4)
    return round((1 - Sum), 4)


# Функция, которая выводит КМИ и записывает ее в матрицу.
def FindMatrix(symbols, p):
    KMI = [[0] * (len(symbols)) for i in range(len(symbols))]
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
        #SumOfRow(KMI, index_i)  # Получаем значение последнего элемента. Из свойств КМИ, сумма по строке равна 1.
        index_i += 1  # Увеличиваем индекс по столбцу.
        print()
    return KMI


def UpdateMatrix(AprKMI, symbols):
    syms = list(symbols.values())
    #print(syms)
    for row in AprKMI:
        for i in range(0, len(row)):
            for j in range(0, len(row)):
                #print(f"i = {i} j = {j} Len = {len(row)} LenSyms = {len(syms)}")
                if CodeDistance(syms[i], syms[j]) == 1:
                    AprKMI[i][i] += AprKMI[i][j]
                    AprKMI[i][j] = 0
    #print(AprKMI)
    return AprKMI


def PrintMatrix(AprKMI, symbols, newsymbol, mainsymb):
    keys = list(symbols.keys())
    syms = list(symbols.values())
    print("   \t\t\t\t", end=" ")  # Быстрое и эффективное начало строки :)
    for x in symbols:
        print(f"{x:9}", end="")
    if newsymbol:
        print(f"{newsymbol:9}", end="")
    print()
    for i in range(0, len(mainsymb)):
        print(f"{keys[i]}\t {syms[i]}", end="   ")
        for j in range(0, len(AprKMI[i])):
            print(f"{AprKMI[i][j]:1.4f}", end="   ")
        print()


def CollapseMatrix(AprKMI, symbols):
    KMI = [[0] * (len(symbols) + 1) for i in range(len(symbols))]
    for i in range(0, len(AprKMI)):
        for j in range(0, len(AprKMI[0]) - 1):
            if j < len(KMI[0]) and i < len(KMI):
                KMI[i][j] = AprKMI[i][j]
        if i < len(KMI) - 1:
            KMI[i][len(KMI[0]) - 1] = SumOfRow(KMI, i)
    KMI[len(KMI) - 1][len(KMI[0]) - 1] = SumOfRow(KMI, len(KMI) - 1)
    return KMI


def main1():
    # Словарь для хранения символа и его кодовой последовательности.
    MainSymbols = {
        'a': "0001",
        'e': "0010",
        "i": "0011",
        "o": "0100",
        "n": "0101",
        "r": "0110",
        "t": "0111",
        "l": "1000",
    }
    dictionary = {
        'a': "0001",
        'e': "0010",
        "i": "0011",
        "o": "0100",
        "n": "0101",
        "r": "0110",
        "t": "0111",
        "l": "1000",
        "1": "1001",
        "2": "1010",
        "3": "1011",
        "4": "1100",
        "5": "1101",
        "6": "1110",
        "7": "1111",
        "8": "0000",

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
    print(12 * "\t" + "Исходная развернутая априорная канальная матрица источника")  # Питон может всё...
    AprKMI = FindMatrix(dictionary, inv)
    UpdateMatrix(AprKMI, dictionary)
    print(2 * "\n")
    print(12 * "\t" + "Развернутая априорная канальная матрица источника при исправлении однократной ошибки")  # Питон может всё...
    PrintMatrix(AprKMI, dictionary, None, MainSymbols)
    KMI = CollapseMatrix(AprKMI, MainSymbols)
    print(2 * "\n")
    print(2 * "\t" + "Свернутая априорная канальная матрица источника при исправлении однократной ошибки")
    PrintMatrix(KMI, MainSymbols, "?", MainSymbols)
    Probability = {
        'a': 0.1888,
        'e': 0.1709,
        "i": 0.1349,
        "o": 0.1325,
        "n": 0.1078,
        "r": 0.0864,
        "t": 0.0847,
        "l": 0.0940,
    }
    Receive = MessageReceive(KMI, Probability)
    GeneratorEntropy = Entropy(Probability)
    ReceiverEntropy = Entropy(Receive)
    Noise = NoiseEntropy(KMI, Probability)
    Leak = LeakEntropy(KMI, Receive, Probability)
    print(f"Априорная энтропия источника: {GeneratorEntropy}")
    print(f"Априорная энтропия приемника: {ReceiverEntropy}")
    print(f"Априорная энтропия шума: {Noise}")
    print(f"Априорная энтропия утечки: {Leak}")
    print(f"Количество полезной информации (энтропия приемника - шум): {round(ReceiverEntropy - Noise, 4)}")
    print(f"Количество полезной информации (энтропия источника - утечка): {round(GeneratorEntropy - Leak, 4)}")
    t = 0.0003  # 0.3 мс = 0.0003 с
    print(f"Скорость передачи информации: {InformationTransfer(t, round(ReceiverEntropy - Noise, 4))}")


main1()
