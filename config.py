from Integer import *

# 有限域参数 q #
q = 0
q_prime = False
q_2m = False
def q_is_prime():
    return q_prime
def q_is_power_of_two():
    return q_2m

def set_q(a):
    global q
    global q_prime
    global q_2m
    if isPrime_MR(a, 15):
        q = a
        q_prime = True
        if is_Power_of_two(q):
            q_2m = True
        else:
            q_2m = False
    elif is_Power_of_two(a):
        q = a
        q_2m = True
        if isPrime_MR(q, 15):
            q_prime = True
        else:
            q_prime = False
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
        for i in range(2, len(a)):
            if a[i] != '0' and a[i] != '1':
                print("*** ERROR: 参数必须是比特串 *** function: set_fx ***")
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