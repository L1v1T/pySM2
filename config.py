from Integer import *

q = 0

def set_q(a):
    global q
    if isPrime(a) or is_Power_of_two(a):
        q = a
    else:
        print("*** ERROR: q必须为奇素数或2的幂 *** function: set_q")

def get_q():
    return q