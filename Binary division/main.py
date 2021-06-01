dividend_list = []
divider_list = []

divider_list_inv = []
reminder = [0] * 16
quotient = []

a = 0
b = 0

dividend = 213
divider = 17

# int to binary (ignore sign + or - bcs droping 0b and 1b)
dividend = bin(dividend)[2:]
divider = bin(divider)[2:]
print(type(dividend))
print(dividend, divider)

# до 16 разрядов
while len(dividend) < 16:
    dividend = '0' + dividend

while len(divider) < 16:
    divider = '0' + divider

print(dividend, divider)

# to list
for i in dividend:
    dividend_list.append(int(i))

for j in divider:
    divider_list.append(int(j))

# подсчет смещения
for i in dividend_list:
    a += 1
    if i == 1:
        break

for j in divider_list:
    b += 1
    if j == 1:
        break

# Предварительный сдвиг делителя
dif = b - a

print(dif)

# padding divider to match dividend
for i in range(dif):
    divider_list.append(0)
    divider_list.pop(1)

# invert обратный код
for i in divider_list:
    if i == 0:
        i = 1
    else:
        i = 0
    divider_list_inv.append(i)

# reverse way of writing binary code
dividend_list = list(reversed(dividend_list))
divider_list = list(reversed(divider_list))
divider_list_inv = list(reversed(divider_list_inv))

# прибавим 1 для получения дополнительного кода
for i in range(len(divider_list_inv)):
    if divider_list_inv[i] == 0:
        divider_list_inv[i] = 1
        for j in range(i):
            divider_list_inv[j] = 0
        break

# основной процесс деления
print('dividend_list', dividend_list)
print('divider_list_inv', divider_list_inv)
print('divider_list', divider_list)

for n in range(dif + 1):
    temp1 = 0
    if dividend_list[15] == 0:  # если остаток положительный
        for i in range(len(dividend_list)):
            if dividend_list[i] == 1 and divider_list_inv[i] == 0 or dividend_list[i] == 0 and divider_list_inv[
                i] == 1:
                if temp1 == 0:
                    reminder[i] = 1
                else:
                    reminder[i] = 0
            elif dividend_list[i] == 1 and divider_list_inv[i] == 1:
                if temp1 == 0:
                    temp1 = 1
                    reminder[i] = 0
                else:
                    reminder[i] = 1
            else:  # 0 and 0
                if temp1 == 0:
                    reminder[i] = 0
                else:
                    temp1 = 0
                    reminder[i] = 1
        if reminder[15] == 1:
            quotient.append(0)
        else:
            quotient.append(1)
    else:  # если остаток отрицательный
        for i in range(len(dividend_list)):
            if dividend_list[i] == 1 and divider_list[i] == 0 or dividend_list[i] == 0 and divider_list[i] == 1:
                if temp1 == 0:
                    reminder[i] = 1
                else:
                    reminder[i] = 0
            elif dividend_list[i] == 1 and divider_list[i] == 1:
                if temp1 == 0:
                    temp1 = 1
                    reminder[i] = 0
                else:
                    reminder[i] = 1
            else:  # 0 and 0
                if temp1 == 0:
                    reminder[i] = 0
                else:
                    temp1 = 0
                    reminder[i] = 1
        if reminder[15] == 1:
            quotient.append(0)
        else:
            quotient.append(1)

    # сдвиг кроме последнего шага
    if n != dif:
        print('---')
        reminder.pop(14)
        reminder.insert(0, 0)
        print(reminder)
        print('---')
        dividend_list = reminder
    else:
        pass

print('reminder', reminder)

# коррекция остатка (optional) если остаток отрицательный
if reminder[15] == 1:
    temp1 = 0
    for i in range(len(reminder)):
        if reminder[i] == 1 and divider_list[i] == 0 or reminder[i] == 0 and divider_list[i] == 1:
            if temp1 == 0:
                reminder[i] = 1
            else:
                reminder[i] = 0
        elif reminder[i] == 1 and divider_list[i] == 1:
            if temp1 == 0:
                temp1 = 1
                reminder[i] = 0
            else:
                reminder[i] = 1
        else:  # 0 and 0
            if temp1 == 0:
                reminder[i] = 0
            else:
                temp1 = 0
                reminder[i] = 1
    print('reminder corrected', reminder)

# убираем изначальный сдвиг
for n in range(dif):
    reminder.insert(14, 0)
    reminder.pop(0)

print('---')
print('quotient', quotient)
print('reminder', reminder)

res1 = list(map(str, quotient))
quotient_dec = int(''.join(res1), 2)

res2 = reversed(list(map(str, reminder)))
reminder_dec = int(''.join(res2), 2)

print('quotient decimal', quotient_dec)
print('reminder decimal', reminder_dec)
