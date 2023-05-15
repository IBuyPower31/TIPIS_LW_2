import math


def ConvertTo2(number, r):
    result = ""
    while number > 0:
        result += str(number % 2)
        number = int(number / 2)
    while len(result) != r:
        result += "0"
    return result[::-1]  # Обратный срез: постоянная практика для реверса чего-то


def MatrixRightRotate(matrix):
    NewMatrix = []
    for j in range(0, len(matrix[0])):
        Helper = []
        """
        Да, возможно этот цикл выглядит так себе, но он имеет смысл.
        Мы идем от элемента I - 1 до нулевого, то есть снизу. 
        Мне показалось, что это самый интуитивно понятный способ повернуть матрицу.
        """
        for i in range(len(matrix) - 1, -1, -1):
            Helper.append(matrix[i][j])
        NewMatrix.append(Helper)
    return NewMatrix


# Транспонирование матрицы (мне всё же удобно работать со строками, нежели со столбцами)
def TranspositionMatrix(matrixToTranspose):
    # Как же я люблю питон за генераторы
    Transposed = [[0 for j in range(len(matrixToTranspose))] for i in range(len(matrixToTranspose[0]))]
    for i in range(0, len(matrixToTranspose)):
        for j in range(0, len(matrixToTranspose[0])):
            Transposed[j][i] = matrixToTranspose[i][j]
    return Transposed


# Создает столбцы матрицы базиса. Меняет единицу с последующим нулём до конца.
def BasisMatrix(array):
    for i in range(0, len(array)):
        if array[i] == '1' and i != len(array) - 1:
            array[i], array[i + 1] = array[i + 1], array[i]
            return array


# Сложение сообщения и вектора по модулю 2
def AdditionMessageAndVector(u, E):
    result = []
    for i in range(0, len(u)):
        if E[i] == '1':
            result.append((int(E[i]) + int(u[i])) % 2)
        else:
            result.append(u[i])
    return result


def MultiplyMessageAndMatrix(m, G):
    """
    print(m)
    print("(*)")
    print(G)
    print("==")
    """
    ArrayR = []
    counter = 0
    #print(f"m: {m} || G: {G}")
    for i in range(0, len(G)):
        for j in range(0, len(G[0])):
           #print(f"M = {m[j]} G[{i}][{j}] = {G[i][j]}")
            if m[j] == G[i][j] == '1':
                counter += 1
        if counter % 2 == 0:
            ArrayR.append('0')
        else:
            ArrayR.append('1')
        counter = 0
    return ArrayR


def HammingCode(k, r):
    H = [[0] * (k + r) for i in range(r)]
    List = []
    for i in range(0, k + r):
        List.append(ConvertTo2(i + 1, r))  # Формируем список из всех индексов, конвертированных в 2СС
    i: int
    for i in range(0, len(H[0])):
        for j in range(0, len(H)):
            H[j][i] = List[i][j]
    # На этом этапе у нас имеется матрица H
    # Теперь мы можем выделить проверочную подматрицу P.
    # Для этого будем выбирать столбцы, стоящие на разрядах, не являющихся степенями двойки.
    P = []
    for i in range(0, len(H)):
        Helper = []
        for j in range(0, len(H[0])):
            if j + 1 not in [1, 2, 4]:
                Helper.append(H[i][j])
        P.append(Helper)
    # На данном этапе у нас есть проверочная подматрица P.
    # Повернем ее на 90 градусов.
    P1 = MatrixRightRotate(P)
    # Матрица повернута. Переходим к шагу создания матрицы G.
    """
    Ставим столбцы P’ на разряды с номерами, равными степеням двойки. 
    Остальные заполняем единичной матрицей. Получаем матрицу G. 
    """
    transposedP1 = TranspositionMatrix(P1)
    strG = []
    iterator = 0
    iterator_j = 0
    # TODO: Пофиксить костыльность кода при создании G
    Column = [['1', '0', '0', '0'], ['0', '1', '0', '0'], ['0', '0', '1', '0'], ['0', '0', '0', '1']]
    for i in range(0, (k + r)):
        if (i + 1) in [1, 2, 4, 8, 16, 32]:
            strG.append(transposedP1[iterator])  # Если позиция есть степень двойки, то добавляем.
            iterator += 1
        else:
            strG.append(Column[iterator_j])
            iterator_j += 1
    G = TranspositionMatrix(strG)
    # Построение матрицы G закончено.
    # Мы работали сначала со строками, потом матрицу транспонировали, получили необходимую G как в лекциях.
    # Вернём все необходимые данные в основную программу и теперь,
    # после всех предварительных работ, можем шифровать и дешифровать.
    return H, G, strG


def Encrypt(m, strG, H):
    # Чтобы получить зашифрованное сообщение u необходимо воспользоваться формулой:
    # u = m * G, где m - исходное сообщение, G - матрица, построенная выше.
    u = MultiplyMessageAndMatrix(m, strG)
    # Если тестировать комбинацию 1010 из лекции, то всё сходится. u = 1011010.
    # print(f"Исходное сообщение: {m} || Закодированное сообщение: {ConvertToString(u)}")
    return u


def Decrypt(u, H):
    syndrome = MultiplyMessageAndMatrix(u, H)
    u1 = u
    if '1' in syndrome:
        # print("Найдена ошибка. Попробуем исправить")
        E = FindVector(syndrome, u)
        u1 = AdditionMessageAndVector(u, E)
    m = []
    for i in range(0, len(u1)):
        if i + 1 not in [1, 2, 4, 8, 16]:
            m.append(u1[i])
    # print(f"Закодированное сообщение: {u} || Синдром: {syndrome} || Исправленное сообщение: {u1}"
    #      f" || Исходное сообщение: {ConvertToString(m)}")
    return m


# Находит вектор ошибки.
def FindVector(syndrome, u):
    res = ConvertToString(syndrome)
    mistake = int(res, 2)
    E = []
    for i in range(0, len(u)):
        if i + 1 == mistake:
            E.append('1')
        else:
            E.append('0')
    #print(f"Вектор ошибки E: {E}")
    return E


def ConvertToString(array):
    result = ""
    for i in range(0, len(array)):
        result += str(array[i])
    return result

"""
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
    K = len(list(dictionary.values())[0])  # Получение числа K.
    R = math.ceil(math.log2(1 + K))  # Поскольку программа должна исправлять только однократные ошибки.
    H, G, strG = HammingCode(K, R)
    print("\t\tКОДИРОВАНИЕ ИСХОДНОГО СЛОВАРЯ:")
    for key in dictionary:
        Encrypt(dictionary[key], strG, H)
    # Decrypt("1011110", H)
    print("\n\n")
    Answer = '1'
    while Answer != '0':
        print("Выберите действие. \n"
              "1 - Кодирование \n"
              "2 - Декодирование \n"
              "0 - Завершить выполнение программы")
        Answer = input()
        if Answer == '1':
            print("Введите кодовую последовательность, которую хотите закодировать:")
            Code = input()
            Encrypt(Code, strG, H)
        elif Answer == '2':
            print("Введите закодированную последовательность, которую нужно раскодировать:")
            Coded = input()
            Decrypt(Coded, H)
        else:
            print("Неизвестное действие")


# Точка входа в основную программу
#main()
"""
