import re
import argparse

def print_irrational_result(b, c):
    c = c * (-1)
    if c < 0 and b < 0:
        c *= -1
        b *= -1
        print(f'{int(c)} / {int(b)}')
    elif c < 0 and b > 0:
        c *= -1
        print(f'- {int(c)} / {int(b)}')
    elif c > 0 and b < 0:
        b *= -1
        print(f'- {int(c)} / {int(b)}')
    else:
        print(f'{int(c)} / {int(b)}')

def solve_line_eq(coef, args):
    b = coef[1]
    c = coef[2]
    print('Polynomial degree: 1')
    if b == 0 and c == 0:
        print('Each real number is a solution')
    elif b == 0 and c != 0:
        print('The equation has no solutions')
    elif b != 0:
        if args.irrational:
            print_irrational_result(b, c)
        else:
            print(float((-1) * c / b))

def sqrt(D):
    x = 1
    while x <= D:
        x = (x + D / x) / 2
        if int(x) * int(x) == D: 
            return (int(x))
        elif abs(x ** 2 - D) < 0.00001:
            return(x) 
    return (x)

def display_negative_discriminant(a, b , c, D):
    print('Discriminant < 0')
    sq = sqrt(-D)
    print('The two solutions are:')
    print(-b / (2*a), '+', sq / (2*a), '*', 'i' )
    print(-b / (2*a), '-', sq / (2*a), '*', 'i' )

def display_zero_discriminant(a, b, c):
    print('Discriminant = 0')
    print('The solution is:')
    print(-b / (2 * a))

def display_positive_discriminant(a, b, c, D):
    sq = sqrt(D)
    print('Discriminant is strictly positive, the two solutions are:')
    print((-b + sq) / (2 * a))
    print((-b - sq) / (2 * a))

def solve_quadratic_eq(coef, args):
    print('Polynomial degree: 2')
    a = coef[0]
    b = coef[1]
    c = coef[2]
    D = (b ** 2) - (4 * a * c)
    if args.detail:
        print('D = b ^ 2 - 4 * a * c')
        print('Discriminant:', D)
        print('X1 = (-b + sqrt(D)) / (2 * a)')
        print('X2 = (-b - sqrt(D)) / (2 * a)')
    if D < 0:
        display_negative_discriminant(a, b, c, D)
    elif D == 0:
        display_zero_discriminant(a, b, c)
    else:
        display_positive_discriminant(a, b, c, D)

def solve_eq(coef, args):
    if coef[0] == 0:
        solve_line_eq(coef, args)
    else:
        solve_quadratic_eq(coef, args)

def get_variable_coefficient(i):
    if '*' not in i:
        i = re.sub('X', '*X', i)
    i = i.split('*')            
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
    print('Error was detected in the term')
    if len(re.findall('\*', i)) > 1:
        print('Too many characters "*" ')
    exit()

def error_empty_side(eq):
    print('Invalid input. ', end = '')
    if eq[0] == '':
        print('Empty left side.')
    elif eq[-1] == '':
        print('Empty right side.')
    else:
        print('Too many characters "+" ')
    exit()

def validation(eq):
    oppos = 1
    dic = {}
    if eq.count('') > 0:
        error_empty_side(eq)
    for i in eq:
        if i == '=':
            oppos = -1
            continue
        elif len(re.findall(r'^[-]?[0-9]+[.]?[0-9]*$', i)):
            coef = float(i)
            var = 'X^0'
        elif 'X' in i:
            if '.' in i:
                if len(re.findall(r'^[-]?[0-9]+[.][0-9]+[*]?[X][\^0-9]*$', i)) != 1:
                    find_error(i)
            else:
                if len(re.findall(r'^[-]?[0-9]*[*]?[X][\^0-9]*$', i)) != 1:
                    find_error(i)
            coef, var = get_variable_coefficient(i)
        if var in dic:
            new = dic.get(var) + (float(coef) * oppos)
            dic.update({var: new})
        else:
            dic.update({var: float(coef) * oppos})
    dic = sort_dic(dic)
    return(dic)    

def print_reduce_form(dic):
    flag = 0
    print(f'Reduced form: ', end='')
    for d in dic:
        coef = dic[d]
        if coef < 0:
            print(f'- ', end='')
            coef = coef * (-1)
        elif flag == 1:
            print(f'+ ', end='')
        flag = 1
        print(f'{coef} * {d} ', end = '')
    print(f'= 0')
    a = dic.get('X^2') if 'X^2' in dic else 0
    b = dic.get('X^1') if 'X^1' in dic else 0
    c = dic.get('X^0') if 'X^0' in dic else 0
    return([a, b, c])

def make_decision(dic):
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
    parser = argparse.ArgumentParser(description="Solve equation")
    parser.add_argument("-d", dest="detail", action='store_true')
    parser.add_argument("-i", dest="irrational", action='store_true')
    args = parser.parse_args()
    
    print('Enter equation: ', end='')
    equation = input().upper()
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
    solve_eq(coef, args)

if __name__== "__main__":
    main()