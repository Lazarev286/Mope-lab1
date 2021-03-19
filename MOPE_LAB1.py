import random
from prettytable import PrettyTable
import time
start_time = time.process_time()
a0 = 4
a1 = 5
a2 = 9
a3 = 7
Xn1 = []
Xn2 = []
Xn3 = []
Y = []
Y1 = []
Y2 = []
X1 = []
X2 = []
X3 = []
for i in range(0,8):
    X1.append(random.randint(1, 21))
    X2.append(random.randint(1, 21))
    X3.append(random.randint(1, 21))
for i in range(8):
    Y.append(a0 + a1*X1[i] + a2*X2[i] + a3*X3[i])
X01 = (max(X1)+min(X1))/2
X02 = (max(X2)+min(X2))/2
X03 = (max(X3)+min(X3))/2
dX1 = X01-min(X1)
dX2 = X02-min(X2)
dX3 = X03-min(X3)
for i in range(0, 8):
    Xn1.append(round((X1[i] - X01)/dX1,4))
    Xn2.append(round((X2[i] - X02)/dX2,4))
    Xn3.append(round((X3[i] - X03)/dX3,4))
Y_et = a0 + a1*X01 + a2*X02 + a3*X03
print("\nНульовий рівень кожного фактору:")
print("X01: " + str(X01))
print("X02: " + str(X02))
print("X03: " + str(X03) + '\n')
print("dX1 = ", dX1)
print("dX2 = ", dX2)
print("dX3 = ", dX3, '\n')
#------------------------------------создание таблицы------------------------------------------------
th = ['№','X1', 'X2', 'X3', 'Y',' ','Xн1','Xн2','Xн3']
td = ['1', X1[0], X2[0],X3[0],Y[0],' ', Xn1[0],Xn2[0],Xn3[0],
      '2', X1[1], X2[1],X3[1],Y[1],' ', Xn1[1],Xn2[1],Xn3[1],
      '3', X1[2], X2[2],X3[2],Y[2],' ', Xn1[2],Xn2[2],Xn3[2],
      '4', X1[3], X2[3],X3[3],Y[3],' ', Xn1[3],Xn2[3],Xn3[3],
      '5', X1[4], X2[4],X3[4],Y[4],' ', Xn1[4],Xn2[4],Xn3[4],
      '6', X1[5], X2[5],X3[5],Y[5],' ', Xn1[5],Xn2[5],Xn3[5],
      '7', X1[6], X2[6],X3[6],Y[6],' ', Xn1[6],Xn2[6],Xn3[6],
      '8', X1[7], X2[7],X3[7],Y[7],' ', Xn1[7],Xn2[7],Xn3[7]]
columns = len(th)
table = PrettyTable(th)
td_data = td[:]
while td_data:
    table.add_row(td_data[:columns])
    td_data = td_data[columns:]
print(table)
#------------------------------------создание таблицы------------------------------------------------
def sr_sum(num):
    the_Sum = 0
    for i in num:
        the_Sum = the_Sum + i
    the_Sum1 = the_Sum/8
    return the_Sum1
SR_Y = sr_sum(Y)
print("Середнє значення Y ", SR_Y)
for i in range(8):
    k = SR_Y-Y[i]
    Y1.append(k)
for j in Y1:
    if j > 0:
        Y2.append(j)
zadanie = SR_Y - min(Y2)
print("Завдання по варіанту : ",zadanie)
print("Yэт: " + str(Y_et))
print("Час становить"+" %s секунд " % (start_time))


