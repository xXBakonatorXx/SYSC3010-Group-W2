import numpy as np
import matplotlib.pyplot as plt

def bit_shift(val_l, n) :
    # convert to str
    val_i = int('0b' + str(val_l)\
                .replace('[','')\
                .replace(']','')\
                .replace(', ',''), 2)
    multiply = 0
    overflow = 0
    output = [0, 0, 0, 0]

    for shift in range(1,abs(n)+1):
        if (n >= 0):
            multiply = 0xf & val_i << 1
            overflow = (0x8 & val_i) // 0x8
        else:
            multiply = 0xf & val_i >> 1
            overflow = (0x1 & val_i) * 0x8

        val_i = multiply + overflow

    for i in range(4):
        output[3 - i] = val_i % 2
        val_i = val_i // 2
    return output

def bin_l(val):
    output = [0, 0, 0, 0]
    for i in range(4):
        output[3 - i] = val % 2
        val = val // 2
    return output


def get_turn(curr, next):
    if (next >= curr):
        turn = np.log2(2**next//2**curr)
    else:
        turn = (-np.log2(2**curr//2**next) + 2**2)

    return turn - 2

if __name__ == '__main__':
    test_node = ["A", "B", "C", "D"]

    test_data = [[("A","A"), ("A","B"), ("A","C"),  ("A","D")],\
                 [("B","A"), ("B","B"), ("B","C"),  ("B","D")],\
                 [("C","A"), ("C","B"), ("C","C"),  ("C","D")],\
                 [("D","A"), ("D","B"), ("D","C"),  ("D","D")]]

    print("(path in, path_out) degrees to turn")
    for test_set in test_data:
        for test in test_set:
            turn = get_turn(test_node.index(test[0]), test_node.index(test[1]))
            print(test, turn)
        print()

    #test = test_data[]
    #turn = get_turn(test_node.index(test[0]), test_node.index(test[1]))