import secrets

how_many_codes = 120

pool = ['A', 'B', 'D', 'E', 'F', 'H', 'K', 'L', 'M', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'] + \
       [chr(ord('1') + i) for i in range(9)]
for _ in range(how_many_codes):
    print(''.join([secrets.choice(pool) for _ in range(9)]))
