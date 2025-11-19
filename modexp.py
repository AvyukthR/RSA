from long_multiplication import long_mul

def mul_mod(a, b, m):
    """Multiply using long_mul, then reduce modulo m."""
    return long_mul(a, b) % m

def modexp(base, exponent, mod):
    """
    Modular exponentiation using square-and-multiply.
    This avoids Python's built-in multiplication by using mul_mod().
    """
    if mod == 1:
        return 0


    result = 1
    base = base % mod
    e = exponent   

    # Standard binary exponentiation loop
    while e > 0:
        # If the current bit of exponent is 1, multiply result by base
        if e & 1:
            result = mul_mod(result, base, mod)
        e >>= 1 # shift exponent right 
        # Square the base for next bit
        if e:
            base = mul_mod(base, base, mod)
    return result
