def p_adic_representation(p, a, b, max_terms=10):

    if (b % p) == 0:
        raise ValueError("gcd(p,b) != 1")

    x_coeffs = []
    p_power = 1

    for n in range(max_terms):
        p_power *= p if n > 0 else p
        target = a % p_power
        x = 0

        while True:
            if (b * x) % p_power == target:
                if n == 0 or x % (p ** n) == x_coeffs[n - 1]:
                    x_coeffs.append(x)
                    break
            x += 1


    p_adic_digits = []
    for x in x_coeffs:
        digits = []
        num = x
        if num == 0:
            digits.append(0)
        else:
            while num > 0:
                digits.append(num % p)
                num = num // p

        p_adic_digits.append(digits[::-1])

    p_adic_str = ""
    for digits in p_adic_digits:
        p_adic_str += "".join(map(str, digits)) + ", "
    p_adic_str = p_adic_str.rstrip(", ") + f" (base {p})"

    return x_coeffs, p_adic_str


p = 3
a = 1
b = 2
max_terms = 6

x_coeffs, p_adic_str = p_adic_representation(p, a, b, max_terms)
print(f"p-adic coefs (x0, x1, ...): {x_coeffs}")
print(f"p-adic representation: {p_adic_str}")