
import sys


def my_sqrt(nb):
    mn = 0
    mx = nb if nb >= 1 else 1
    while mx - mn > 0.000000001:
        mid = (mn + mx) / 2
        if mid * mid < nb:
            mn = mid
        else:
            mx = mid
    return mx


def degree(a,b,c):
    if a == 0 and b == 0:
        return 0
    elif a == 0:
        return 1
    else:
        return 2


def discriminant(a,b,c):
    print(float(b*b - 4*a*b*c))
    return b*b - 4*a*c


def get_coeff(side):
    a, b, c = 0, 0, 0
    for coeff in side:
        if coeff == "":
            continue
        digit, power = coeff.split("*")
        var, power = power.split("^")
        power = float(power)
        if var != "X":
            raise()
        if power == 0:
            c += float(digit)
        elif power == 1:
            b += float(digit)
        elif power == 2:
            a += float(digit)
        else:
            sys.exit("Wrong power")
    return(a, b, c)


def print_reduc(a, b, c):
    print("The reduced form is : {} * X^2 + {} * X^1 + {} = 0".format(a, b, c))


def easy_solv(a,b,c):
    if c == 0:
        print("|R")
    else:
        print("There is no solution")
    return


def linear_solv(a,b,c):
    print("The solution is : ", -c/b)
    return


def second_degree_solv(a,b,c):
    D = discriminant(a,b,c)
    first_part = -b / (2 * a)
    if D < 0:
        print("Discrimant < 0")
        sqrt = my_sqrt(-D) / (2 * a)
        print("The two solutions are : \n{} + i * {}  \n{} - i * {}".format(first_part, sqrt, first_part, sqrt))
    elif D == 0:
        print("Discrimant = 0, one double solution : \n", first_part)
    else:
        print("Discrimant > 0")
        sqrt = my_sqrt(D) / (2 * a)
        print("The two solutions are : \n{} \n{}".format(first_part + sqrt, first_part - sqrt))
    return


def run(equation):
    a = 0
    b = 0
    c = 0
    #print("уравнение 1", equation)
    equation = equation.replace(" ", "").replace("-", "+-").split("=")
    #print("уравнение 2", equation)
    parts = [equation[i].split("+") for i in range(len(equation))]
    #print("уравнение 2", parts)
    if len(parts) != 2:
        print("Input not valid")
        return
    for index, side in enumerate(parts):
        print('index =', index)
        aN, bN, cN = get_coeff(side)
        if index == 0:
            a += aN
            b += bN
            c += cN
        else:
            a -= aN
            b -= bN
            c -= cN
    print_reduc(a,b,c)
    deg = degree(a,b,c)
    print("Polynomial degree : {}".format(degree(a,b,c)))
    if deg == 0:
        easy_solv(a,b,c)
    elif deg == 1:
        linear_solv(a,b,c)
    else:
        second_degree_solv(a,b,c)


if __name__== "__main__":
    print("Write down an equation : ", end="")
    equation = str(input())
    try:
        run(equation)
    except:
        sys.exit("Input not valid")