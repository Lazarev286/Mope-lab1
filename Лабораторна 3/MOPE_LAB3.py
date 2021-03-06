import numpy as np
import random
from numpy.linalg import solve
from scipy.stats import f, t
from functools import partial
x_range = [(10, 50), (-20, 60), (-20, 20)]
x_aver_max = (50 + 60 + 20)/ 3
x_aver_min = (10 - 20 - 20) / 3
y_max = 200 + int(x_aver_max)
y_min = 200 + int(x_aver_min)
def regress(x, b):
    y = sum([x[i]*b[i] for i in range(len(x))])
    return y
def MATRIX(n, m):
    y = np.zeros(shape=(n, m))
    for i in range(n):
        for j in range(m):
            y[i][j] = random.randint(y_min, y_max)
    x_norm = np.array([[1, -1, -1, -1],
                       [1, -1, 1, 1],
                       [1, 1, -1, 1],
                       [1, 1, 1, -1],
                       [1, -1, -1, 1],
                       [1, -1, 1, -1],
                       [1, 1, -1, -1],
                       [1, 1, 1, 1]])
    x_norm = x_norm[:len(y)]
    x = np.ones(shape=(len(x_norm), len(x_norm[0])))
    for i in range(len(x_norm)):
        for j in range(1, len(x_norm[i])):
            if x_norm[i][j] == -1:
                x[i][j] = x_range[j-1][0]
            else:
                x[i][j] = x_range[j-1][1]
    print('\n1. Матриця планування:')
    print(np.concatenate((x, y), axis=1))
    return x, y, x_norm
def Coeff(x, y_aver, n):
    mx1 = sum(x[:, 1]) / n
    mx2 = sum(x[:, 2]) / n
    mx3 = sum(x[:, 3]) / n
    my = sum(y_aver) / n
    a12 = sum([x[i][1] * x[i][2] for i in range(len(x))]) / n
    a13 = sum([x[i][1] * x[i][3] for i in range(len(x))]) / n
    a23 = sum([x[i][2] * x[i][3] for i in range(len(x))]) / n
    a11 = sum([i ** 2 for i in x[:, 1]]) / n
    a22 = sum([i ** 2 for i in x[:, 2]]) / n
    a33 = sum([i ** 2 for i in x[:, 3]]) / n
    a1 = sum([y_aver[i] * x[i][1] for i in range(len(x))]) / n
    a2 = sum([y_aver[i] * x[i][2] for i in range(len(x))]) / n
    a3 = sum([y_aver[i] * x[i][3] for i in range(len(x))]) / n
    X = [[1, mx1, mx2, mx3], [mx1, a11, a12, a13], [mx2, a12, a22, a23], [mx3, a13, a23, a33]]
    Y = [my, a1, a2, a3]
    B = [round(i, 2) for i in solve(X, Y)]
    print('\n2. Рівняння регресії:')
    print(f'{B[0]} + {B[1]}*x1 + {B[2]}*x2 + {B[3]}*x3')
    return B
#----------------------------------------------------------------
def S_KV(y, y_aver, n, m):#знаходження суми дисперсії по рядках
    res = []
    for i in range(n):
        s = sum([(y_aver[i] - y[i][j])**2 for j in range(m)]) / m
        res.append(s)
    return res
#-----------------------------------------------------------------
def bs(x, y, y_aver, n):
    res = [sum(1 * y for y in y_aver) / n]
    for i in range(3):  # 4 - ксть факторів
        b = sum(j[0] * j[1] for j in zip(x[:, i], y_aver)) / n
        res.append(b)
    return res
def Cochren(y, y_aver, n, m):
    S_kv = S_KV(y, y_aver, n, m)
    Gp = max(S_kv) / sum(S_kv)
    print('\n3. Перевірка за критерієм Кохрена:')
    return Gp
def KR_ST(x, y, y_aver, n, m):
    S_kv = S_KV(y, y_aver, n, m)
    s_kv_aver = sum(S_kv) / n
    s_Bs = (s_kv_aver / n / m) ** 0.5
    Bs = bs(x, y, y_aver, n)
    ts = [abs(B) / s_Bs for B in Bs]
    return ts
def Fisher(y, y_aver, y_new, n, m, d):
    S_ad = m / (n - d) * sum([(y_new[i] - y_aver[i])**2 for i in range(len(y))])
    S_kv = S_KV(y, y_aver, n, m)
    S_kv_aver = sum(S_kv) / n
    return S_ad / S_kv_aver
def cohren(f1, f2, q=0.05):
    q1 = q / f1
    fisher_value = f.ppf(q=1 - q1, dfn=f2, dfd=(f1 - 1) * f2)
    return fisher_value / (fisher_value + f1 - 1)
def main(n, m):
    f1 = m - 1
    f2 = n
    f3 = f1 * f2
    q = 0.05
    student = partial(t.ppf, q=1-0.025)
    t_student = student(df=f3)
    G_kr = cohren(f1, f2)
    x, y, x_norm = MATRIX(n, m)
    print("-"*88)
    y_aver = [round(sum(i) / len(i), 2) for i in y]
    B = Coeff(x, y_aver, n)
    print("-" * 88)
    Gp = Cochren(y, y_aver, n, m)
    print(f'Gp = {Gp}')
    if Gp < G_kr:
        print(f'З ймовірністю {1-q} дисперсії однорідні.')
    else:
        print("Необхідно збільшити кількість дослідів")
        m += 1
        main(n, m)
    print("-" * 88)
    ts = KR_ST(x_norm[:, 1:], y, y_aver, n, m)
    print('\n4. Критерій Стьюдента:\n', ts)
    res = [t for t in ts if t > t_student]
    final_k = [B[ts.index(i)] for i in ts if i in res]
    print('Коефіцієнти {} статистично незначні, тому ми виключаємо їх з рівняння.'.format([i for i in B if i not in final_k]))
    print("-" * 88)
    y_new = []
    for j in range(n):
        y_new.append(regress([x[j][ts.index(i)] for i in ts if i in res], final_k))
    print(f'\n5. Значення Y з коефіцієнтами: {final_k}')
    print(y_new)
    print("-" * 88)
    d = len(res)
    f4 = n - d
    F_p = Fisher(y, y_aver, y_new, n, m, d)
    fisher = partial(f.ppf, q=1 - 0.05)
    f_t = fisher(dfn=f4, dfd=f3)  # табличне знач
    print('\n6. Перевірка адекватності за критерієм Фішера:')
    print('Fp =', F_p)
    print('F_t =', f_t)
    if F_p < f_t:
        print('Математична модель адекватна експериментальним даним')
    else:
        print('Математична модель не адекватна експериментальним даним')
main(4, 4)
