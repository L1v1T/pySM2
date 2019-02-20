from Integer import *

# 有限域参数 q #
q = 0

def set_q(a):
    global q
    if isPrime(a) or is_Power_of_two(a):
        q = a
    else:
        print("*** ERROR: q必须为奇素数或2的幂 *** function: set_q")

def get_q():
    return q

# 二元阔域中做模数的素多项式 #
fx = '0b0'

def set_fx(a):
    global fx
    if a[0:2] != '0b':
        print("*** ERROR: 参数必须是比特串 *** function: set_fx")
    else:
        fx = a

def get_fx():
    return fx
# test set_fx #
#print(fx)
#set_fx('0b10101111')
#print(fx)