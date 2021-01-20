
def ecc_encode(number: int) -> str:
    if not isinstance(number, int):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    def alpha_encode(number):
        ALPHABET, base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', list('AAA')
        len_ab = len(ALPHABET)
        len_base = len(base)
        for i in range(len_base):
            number, idx = divmod(number, len_ab)
            base[i] = ALPHABET[idx]

        base.reverse()
        return "".join(base)
    return alpha_encode(number // 1000) + f"{number % 1000:03}"
