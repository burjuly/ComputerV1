import re

def solve_line_eq(coef):
    print(f'Сoefficient{coef}')
    b = coef[1]
    c = coef[2]
    print('Polynomial degree: 1')
    if b == 0 and c == 0:
        print('An infinite number of solutions')
    elif b == 0 and c != 0:
        print('The equation has no solutions')
    elif b != 0 and c != 0:
        res = float((-1) * c / b)
        print(res) 

def sqrt(D):
    #print("КОРЕНЬ ИЗВЛЕКАЕТСЯ...")
    x = 1
    while x <= D:
        #print(x)
        x = (x + D / x) / 2
        if int(x) * int(x) == D: 
            return (int(x))
        elif abs(x ** 2 - D) < 0.00001:
            return(x) 
    return (x)

def display_negative_discriminant(a, b , c, D):
    print('Discriminant < 0')
    print('The equation has no solutions')
    #sq = sqrt(-D)
    #print('The two solutions are:')
    #print(-b / (2*a), '+', sq / (2*a), '*', 'i' )
    #print(-b / (2*a), '-', sq / (2*a), '*', 'i' )

def display_zero_discriminant(a, b, c):
    print('Discriminant = 0')
    print('The solution is:')
    print(-b / (2 * a))

def display_positive_discriminant(a, b, c, D):
    sq = sqrt(D)
    #print(f'КОРЕНЬ ИЗ ДИСКР {sq} ')
    print('Discriminant is strictly positive, the two solutions are:')
    print((-b + sq) / (2 * a))
    print((-b - sq) / (2 * a))

def solve_quadratic_eq(coef):
    print('Polynomial degree: 2')
    print(f'Коэффициенты {coef}')
    a = coef[0]
    b = coef[1]
    c = coef[2]
    D = (b ** 2) - (4 * a * c)
    print('Discriminant', D)
    if D < 0:
        display_negative_discriminant(a, b, c, D)
    elif D == 0:
        display_zero_discriminant(a, b, c)
    else:
        display_positive_discriminant(a, b, c, D)

def solve_eq(coef):
    if coef[0] == 0:
        print('Solve liner eq')
        solve_line_eq(coef)
    else:
        solve_quadratic_eq(coef)

#Проверка на число (для float) Отрицательные числа?
def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_variable_coefficient(i):
    if '*' not in i: #Если нет умножения, то добавляем, чтобы потом рассплитить по *
        i = re.sub('X', '*X', i)
    i = i.split('*')        
    #TODO если есть точка в коэффициенте сделать float, если нет - int
    
    if i[0] == '-' or i[0] == '':
        coef = 1 if i[0] == '' else -1
    else:
        coef = float(i[0])
    if i[1] == 'X':
        var = 'X^1'
    else:
        var = i[1]
    return(coef, var)

def sort_dic(dic):
    sort_d = {}
    sort_d = sorted(dic.items(), key=lambda x: x[0])
    return(dict(sort_d))

def find_error(i):
    print('Errors were detected in the term')
    if len(re.findall('\*', i)) > 1:
        print('Too many characters "*" ')
    exit()

def error_empty_side(eq):
    print('Invalid input. ', end = '')
    if eq[0] == '':
        print('Empty left side.')
    else:
        print('Empty right side.')
    exit()

def validation(eq):
    oppos = 1
    dic = {}
    print(f'eq = {eq}')
    if eq.count('') > 0:
        error_empty_side(eq)
    for i in eq:
        if i == '=':
            oppos = -1
            continue
        # Число (положительное, отрицательное, float)
        elif len(re.findall(r'^[-]?[0-9]+[.]?[0-9]*$', i)):
            print(f'i = {i}')
            coef = float(i)
            var = 'X^0'
        # Слагаемое с переменной
        elif 'X' in i:
            if '.' in i: # Есть float коэффициент
                if len(re.findall(r'^[-]?[0-9]+[.][0-9]+[*]?[X][\^0-9]*$', i)) != 1:
                    find_error(i)
            else:
                if len(re.findall(r'^[-]?[0-9]*[*]?[X][\^0-9]*$', i)) != 1:
                    #l = len(re.findall(r'^[-]?[0-9]*[*]?[X][\^0-9]*$', i))
                    find_error(i)
                    #print('Wrong type of term')
                    #exit() 
            coef, var = get_variable_coefficient(i)
        if var in dic:
            new = dic.get(var) + (float(coef) * oppos)
            dic.update({var: new})
        else:
            dic.update({var: float(coef) * oppos})
    print(f'dic = {dic}')
    dic = sort_dic(dic)
    print(f'dic {dic}')
    return(dic)    

def print_reduce_form(dic):
    flag = 0
    print(f'Reduced form: ', end='')
    for d in dic:
        coef = dic[d]
        if coef < 0:
            print(f'- ', end='')
            coef = coef * (-1)
        elif flag == 1: #не добавлять +, если в начале строки положительный коэффициент
            print(f'+ ', end='')
        flag = 1
        print(f'{coef} * {d} ', end = '')
    print(f'= 0')
    a = dic.get('X^2') if 'X^2' in dic else 0
    b = dic.get('X^1') if 'X^1' in dic else 0
    c = dic.get('X^0') if 'X^0' in dic else 0   
    #print('a =', a)
    #print('b =', b)
    #print('c =', c)
    return([a, b, c])

def make_decision(dic):
    #TODO дополнить
    if dic is None:
        exit()
    i = len(dic) - 1
    keys = list(dic.keys())
    while i >= 0:
        if dic[keys[i]] == 0:
            i -= 1
            continue
        power = int(re.sub(r'X[\^]', '', keys[i]))
        if power > 2:
            print(f'Polynomial degree: {power}')
            print(f'The polynomial degree is stricly greater than 2, I can\'t solve.')
            exit()
        i -= 1
def check_symbols(eq):
    if len(re.findall('[^X\^0-9\+-=\*]', eq)) > 0:
        print('Invalid characters in string')
        exit()

def main():
    print('Enter equation: ', end='')
    equation = input()
    if not equation:
        print('Empty input')
        exit()
    equation = re.sub(r'\s+', '', equation)
    equation = re.sub(r'\b[-]', '+-', equation).replace('=', '+=+')
    if len(re.findall('=', equation)) != 1:
        print('Wrong number of characters "=" ')
        exit()
    check_symbols(equation)
    equation = equation.split('+')
    dic = validation(equation)
    make_decision(dic)
    coef = print_reduce_form(dic)
    solve_eq(coef)

if __name__== "__main__":
    main()