from math import sqrt


def solve(a, b, c):
    """a * x^2 + b * x + c = 0
    """
    if a == 0:
        return float(-c) / b
    D = b * b - 4 * a * c
    if D > 0:
        d = sqrt(D)
        x_1 = (-b + d) / (2 * a)
        x_2 = (-b - d) / (2 * a)
        return (x_1, x_2)
    elif D == 0:
        x_1 = float(-b) / (2 * a)
        return x_1
    elif D < 0:
        raise Exception("later? Need to use complex numbers")


if __name__ == '__main__':
    print solve(2, 5, 2)
    print solve(2, 4, 2)
    print solve(0, 2, 3)
