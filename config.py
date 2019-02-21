from Integer import *

# 有限域参数 q #
q = 0

def set_q(a):
    global q
    if isPrime_MR(a, 15) or is_Power_of_two(a):
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
### test set_fx ###
#print(fx)
#set_fx('0b10101111')
#print(fx)

# 椭圆曲线参数 #
a = 0
b = 0

def set_a(ia):
    global a
    a = ia

def get_a():
    return a

def set_b(ib):
    global b
    b = ib

def get_b():
    return b

n = 0
def set_n(a):
    global n
    n = a
def get_n():
    return n