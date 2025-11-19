def long_mul(a, b):
    """
    Perform long multiplication (schoolbook multiplication) on two arbitrarily large integers.
    This implementation does NOT use Python's built-in big integers for multiplication,
    except at the digit level. It simulates the exact process taught in school.
    """

    # Convert integers to reversed strings so index 0 is the least significant digit.
    a = str(a)[::-1]
    b = str(b)[::-1]

    # Result array: max possible digits = len(a) + len(b)
    res = [0] * (len(a) + len(b))

    # Multiply each digit of a with each digit of b
    for i in range(len(a)):
        for j in range(len(b)):
            res[i + j] += int(a[i]) * int(b[j])  # accumulate digit product

    # Handle carries
    carry = 0
    for i in range(len(res)):
        total = res[i] + carry
        res[i] = total % 10
        carry = total // 10

    # Remove leading zeros
    while len(res) > 1 and res[-1] == 0:
        res.pop()

    # Convert back to integer
    return int("".join(map(str, res[::-1])))
