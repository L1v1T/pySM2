from Integer import *
import config
from SM2_Code import *
import math

# 3.1.2 素域 Fp 运算
# 素域加法
'''
input: 域元素 a 和 b
output: 域元素 (a+b)
'''
def field_ele_add(a, b):
    #print("--- 素域 Fp 加法 ---")

    q = config.get_q()
    # q 为奇素数
    if isPrime(q) and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是域中元素 *** function: field_ele_add ***")
            return -1;
        elif not (b >=0 and b<= q-1):
            print("*** ERROR: b不是域中元素 *** function: field_ele_add ***")
            return -1;
        else:
            return((a + b) % q)
    else:
        print("*** ERROR: 模数q不是奇素数 *** function: field_ele_add ***")
        return -1;
### test field_ele_add ###
#config.set_q(997)
#print(field_ele_add(996, 2))

# 素域乘法
'''
input: 域元素 a 和 b
output: 域元素 (a*b)
'''
def field_ele_time(a, b):
    #print("--- 素域 Fp 乘法 ---")

    q = config.get_q()
    # q 为奇素数
    if isPrime(q) and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是域中元素 *** function: field_ele_time ***")
            return -1;
        elif not (b >=0 and b<= q-1):
            print("*** ERROR: b不是域中元素 *** function: field_ele_time ***")
            return -1;
        else:
            return((a * b) % q)
    else:
        print("*** ERROR: 模数q不是奇素数 *** function: field_ele_time ***")
        return -1;
### test field_ele_time ###
#config.set_q(997)
#print(field_ele_time(56, 46))

# 3.1.3 二元扩域 F2m 运算
# 二元扩域加法
'''
input: 域元素（比特串） a 和 b
output: 域元素（比特串） (a+b)
'''
def field_ele_add_2m(a, b):
    q = config.get_q()
    # q是2的幂
    if is_Power_of_two(q):
        m = math.log2(q)
        if (len(a)-2) > m or (len(b)-2) >m:
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_add ***")
            return -1;
        else:
            c_int = ele_to_int_2m(a) ^ (ele_to_int_2m(b))
            c_bytes = int_to_bytes(c_int, 2)
            c_ele = bytes_to_ele(q, c_bytes)
            return c_ele
    else:
        print("*** ERROR: q不是2的幂 *** function: field_ele_add ***")
        return -1;
### test field_ele_add ###
config.set_q(1024)
print(field_ele_add_2m('0b1010101010', '0b1111111100'))
# 二元扩域乘法
'''
input: 域元素（比特串） a 和 b
output: 域元素（比特串） (a+b)
'''