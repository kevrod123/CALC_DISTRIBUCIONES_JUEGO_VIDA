# algoritmos.py
def cuadrados_medios(semilla, n):
    resultados = []
    x = semilla
    for i in range(n):
        y = x ** 2
        y_str = str(y)
        if len(y_str) % 2 == 1:
            y_str = "0" + y_str
        L = len(y_str)
        inicio = (L // 2) - 2
        medio = int(y_str[inicio:inicio + 4])
        ri = medio / 10000
        resultados.append([i, x, y_str, medio, ri])
        x = medio
    return resultados

def productos_medios(x0, x1, n):
    resultados = []
    xi = x0
    xi1 = x1
    for i in range(n):
        y = xi * xi1
        y_str = str(y)
        if len(y_str) % 2 == 1:
            y_str = "0" + y_str
        L = len(y_str)
        inicio = (L // 2) - 2
        medio = int(y_str[inicio:inicio + 4])
        ri = medio / 10000
        resultados.append([i, xi, xi1, y_str, medio, ri])
        xi = xi1
        xi1 = medio
    return resultados

def multiplicador_constante(x0, x1, n):
    resultados = []
    xi = x0
    xi1 = x1
    for i in range(n):
        y = xi * xi1
        y_str = str(y)
        if len(y_str) % 2 == 1:
            y_str = "0" + y_str
        L = len(y_str)
        inicio = (L // 2) - 2
        medio = int(y_str[inicio:inicio + 4])
        ri = medio / 10000
        resultados.append([i, xi, xi1, y_str, medio, ri])
        xi1 = medio
    return resultados
