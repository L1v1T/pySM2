from Integer import *
import config
from SM2_Code import *
import math
from polynomial import *

# 3.1 有限域计算
# 有限域加法
'''
input: 域元素 a 和 b
output: 域元素 (a+b)
'''
def field_ele_add(a, b):
    #print("--- 有限域 加法 ---")

    q = config.get_q()
    # q 为奇素数
    if isPrime(q) and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是素域中元素 *** function: field_ele_add ***")
            return -1
        elif not (b >=0 and b<= q-1):
            print("*** ERROR: b不是素域中元素 *** function: field_ele_add ***")
            return -1
        else:
            return((a + b) % q)
    # q 为 2 的幂
    elif is_Power_of_two(q):
        m = math.log2(q)
        if (len(a)-2) > m or (len(b)-2) >m:
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_add ***")
            return -1
        else:
            c_int = ele_to_int(a) ^ (ele_to_int(b))
            c_bytes = int_to_bytes(c_int, 2)
            c_ele = bytes_to_ele(q, c_bytes)
            return c_ele
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***")
        return -1
### test field_ele_add ###
#config.set_q(997)
#print(field_ele_add(996, 2))
#config.set_q(1024)
#print(field_ele_add('0b1010101010', '0b1111111100'))

# 有限域乘法
'''
input: 域元素 a 和 b
output: 域元素 (a*b)
'''
def field_ele_times(a, b):
    #print("--- 有限域 乘法 ---")

    q = config.get_q()
    # q 为奇素数
    if isPrime(q) and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是域中元素 *** function: field_ele_times ***")
            return -1
        elif not (b >=0 and b<= q-1):
            print("*** ERROR: b不是域中元素 *** function: field_ele_times ***")
            return -1
        else:
            return((a * b) % q)
    # q 为 2 的幂
    elif is_Power_of_two(q):
        m = math.log2(q)
        if (len(a)-2) > m or (len(b)-2) >m:
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_times ***")
            return -1
        else:
            result_bits = polynomial_a_mod_b(polynomial_times(a, b), config.get_fx())
            return bytes_to_ele(q, bits_to_bytes(result_bits), )
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_times ***")
        return -1
### test field_ele_time ###
#config.set_q(997)
#print(field_ele_times(56, 46))
#config.set_q(32)
#config.set_fx('0b100101')
#print(field_ele_times('0b111', '0b1101'))