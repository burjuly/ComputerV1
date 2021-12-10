import re

def leave():
    print('Invalid input')
    exit()

def solve_line_eq(coef):
    print(f'КОЭФФИЦИЕНТЫ{coef}')
    b = coef[1]
    c = coef[2]
    print('Polynomial degree: 1')
    if b == 0 and c == 0:
        print('Уравнение имеет бесконечно много решений')
    elif b == 0 and c != 0:
        print('Уравнение не имеет решений')
    elif b != 0 and c != 0:
        res = float((-1) * c / b)
        print(res) 

def sqrt(D):
    #print("КОРЕНЬ ИЗВЛЕКАЕТСЯ...")
    x = 1
    while x <= D:
        print(x)
        x = (x + D / x) / 2
        if int(x) * int(x) == D: 
            return (int(x))
        elif abs(x ** 2 - D) < 0.00001:
            return(x) 
    return (x)

def display_negative_discriminant(a, b , c, D):
    print('Discriminant < 0')
    print('Нет решений')
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
    print(f'КОРЕНЬ ИЗ ДИСКР {sq} ')
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

def check_term(term):
    degree_x = ['X^0', 'X', 'X^1', 'X^2']
    coef, var = '', ''
    if len(term) == 1: # X, 5X, 3X^2, -X
        if term[0].find('X') != -1:
            print('CASE2')
            term = term[0].replace('X', ' X').split(' ')
            print(f'TERM0 {term[0]} и TERM1 {term[1]}')
            var = term[1]
            if term[0] == '':
                coef = 1
            elif term[0] == '-':
                coef = -1
            else:
                coef = term[0]
            return coef, var
        else: # 10 ...
            if is_number(term[0]):
                return term[0], None
    elif len(term) == 2:
        if is_number(term[0]) and term[1] in degree_x:
            return term[0], term[1]
        if term[1] not in degree_x:
            print("Wrong term")

def edit_dic(dic):
    if 'X^1' in dic and 'X' in dic:
        val = dic.get('X') + dic.get('X^1')
        dic.update({'X^1': val})
        del dic['X'] 
    if None in dic and 'X^0' in dic:
        val = dic.get(None) + dic.get('X^0')
        dic.update({'X^0': val})
        del dic[None]
    return(dic)

def valid(eq):
    oppos = 1
    coef, var = '', ''
    dic = {}
    print(eq)
    if eq.count('') > 0 or eq.count('=') != 1:
        leave()
        print('Invalid input')
        return
    for i in eq:
        if i == '=':
            oppos = -1
            continue
        elif i.count('*') > 1:
            print('Invalid input. Too many characters "*"')
        else:
            i = i.split('*')
            coef, var = check_term(i)
            print(f'Слагаемое {i}')
            print(f'Коэффициент {coef} Переменная {var}')
            if var in dic:
                new = dic.get(var) + (float(coef) * oppos)
                dic.update({var: new})
            else:
                dic.update({var: float(coef) * oppos})
            print(dic)
    dic = edit_dic(dic)
    return(dic)

def print_reduce_form(dic):
    a = dic.get('X^2') if 'X^2' in dic else 0
    b = dic.get('X^1') if 'X^1' in dic else 0
    c = dic.get('X^0') if 'X^0' in dic else 0   
    print('a =', a)
    print('b =', b)
    print('c =', c)
    print(f"Reduced form: {a} * X^2 + {b} * X^1 + {c} * X^0 = 0")
    return([a, b, c])

def main():
    print('Введите уравнение: ', end='')
    eq = input()
    if not eq:
        print('Empty input')
        return
    eq = eq.replace(' ', '').replace('-', '+-').replace('=', '+=+')
    eq = eq.split('+')
    dic = valid(eq)
    coef = print_reduce_form(dic)
    solve_eq(coef)

if __name__== "__main__":
    main()