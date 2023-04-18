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
            strG.append(transposedP1[iterator]) # Если позиция есть степень двойки, то добавляем.
            iterator += 1
        else:
            strG.append(Column[iterator_j])
            iterator_j += 1
    # Построение матрицы G закончено.
    # Мы работали сначала со строками, потом матрицу транспонировали, получили необходимую G как в лекциях.



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
    HammingCode(K, R)


# Точка входа в основную программу
main()

