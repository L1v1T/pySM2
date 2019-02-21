from Integer import *
import config
from SM2_Code import *
import math
from polynomial import *
from Point import *

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
            return bytes_to_ele(q, bits_to_bytes(result_bits))
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_times ***")
        return -1
### test field_ele_time ###
#config.set_q(997)
#print(field_ele_times(56, 46))
#config.set_q(32)
#config.set_fx('0b100101')
#print(field_ele_times('0b111', '0b1101'))

# 有限域除法
'''
input: 被除数 a 和除数 b
output: 除法所得商
'''
def field_ele_a_devide_b(a, b):
    #print("--- 有限域 除法 ---")

    q = config.get_q()
    # q 为奇素数
    if isPrime(q) and q > 2:
        if not (a >= 0 and a <= q-1):
            print("*** ERROR: a不是域中元素 *** function: field_ele_a_devide_b ***")
            return -1
        elif not (b >= 0 and b <= q-1):
            print("*** ERROR: b不是域中元素 *** function: field_ele_a_devide_b ***")
            return -1
        else:
            return int(a / b)
    # q 为 2 的幂
    elif is_Power_of_two(q):
        m = math.log2(q)
        if (len(a)-2) > m or (len(b)-2) >m:
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_a_devide_b ***")
            return -1
        else:
            result_bits = polynomial_a_mod_b(polynomial_times(a, b), config.get_fx())
            return bytes_to_ele(q, bits_to_bytes(result_bits))
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_a_devide_b ***")
        return -1

# 有限域幂运算
'''
iuput: 域元素 a 和 幂次 x
output: 域元素 a**x
'''
def field_ele_a_pow_x(a, x):
    #print("--- 有限域 幂运算 ---")

    q = config.get_q()
    # q 为奇素数
    if isPrime(q) and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是域中元素 *** function: field_ele_a_pow_x ***")
            return -1
        else:
            return((a**x) % q)
    # q 为 2 的幂
    elif is_Power_of_two(q):
        m = math.log2(q)
        if (len(a)-2) > m:
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_a_pow_x ***")
            return -1
        else:
            result_bits = polynomial_one()
            if x != 0:
                for i in range(1, x + 1):
                    result_bits = polynomial_times(result_bits, a)
                result_bits = polynomial_a_mod_b(result_bits, config.get_fx())
            return bytes_to_ele(q, bits_to_bytes(result_bits))
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_a_pow_x ***")
        return -1
### test field_ele_a_pow_x ###
#config.set_q(23)
#print(field_ele_a_pow_x(7, 4))
#config.set_q(16)
#config.set_fx('0b10011')
#print(field_ele_a_pow_x('0b0010', 9))

# 3.2.3 椭圆曲线群 #
# 椭圆曲线元素判断 #
# 元素为零 #
def ECG_ele_is_zero(p):
    if p.x == 0 and p.y == 0:
        return True
    else:
        return False
# 元素互为逆元素 #
def ECG_is_inverse_ele(p1, p2):
    q = config.get_q()
    # q 为素数
    if isPrime(q):
        if p1.x == p2.x and p1.y == -p2.y:
            return True
        else:
            return False
    elif is_Power_of_two(q):
        if p1.x == p2.x and p2.y == p1.x + p1.y:
            return True
        else:
            return False
    else:
        print("*** ERROR: q 不是素数或者 2 的幂 *** function: ECG_is_inverse_ele ***")
        return False
# 元素相等 #
def ECG_ele_equal(p1, p2):
    if p1.x == p2.x and p1.y == p2.y:
        return True
    else:
        return False

# 椭圆曲线加法 #
'''
input: 椭圆曲线群中点 a 和 b
output: 椭圆曲线群中点(a+b)
'''
def ECG_ele_add(p1, p2):
    q = config.get_q()
    # Fp 上的椭圆曲线群
    if isPrime(q):
        if ECG_ele_is_zero(p1):
            return p2
        elif ECG_ele_is_zero(p2):
            return p1
        elif ECG_is_inverse_ele(p1, p2):
            return Point(0, 0)
        elif ECG_ele_equal(p1, p2):
            #lam = (3 * (p1.x**2) + config.get_a()) / (2 * p1.y)
            t1 = field_ele_add(field_ele_times(3, field_ele_a_pow_x(p1.x, 2)), config.get_a())
            t2 = field_ele_times(2, p1.y)
            lam = field_ele_a_devide_b(t1, t2)
            x = lam**2 - 2 * p1.x
            y = lam * (p1.x - x) - p1.y
            return Point(x, y)
        else:
            lam = (p2.y - p1.y) / (p2.x - p1.x)
            x = lam * lam - p1.x - p2.x
            y = lam * (p1.x - x) - p1.y
            return Point(x, y)

    # F2^m 上的椭圆曲线
    if is_Power_of_two(q):
        if ECG_ele_is_zero(p1):
            return p2
        elif ECG_ele_is_zero(p2):
            return p1
        elif ECG_is_inverse_ele(p1, p2):
            return Point(0, 0)
        elif ECG_ele_equal(p1, p2):
            lam = p1.x + (p1.y / p1.x)
            x = lam**2 + lam + config.get_a()
            y = p1.x**2 + (lam + 1) * x
            return Point(x, y)
        else:
            lam = (p1.y + p2.y) / (p1.x + p2.x)
            x = lam**2 + lam + p1.x + p2.x + config.get_a()
            y = lam * (p1.x + x) + x + p1.y
            return Point(x, y)

# 椭圆曲线求 2 倍点 #
'''
input: 椭圆曲线点 p
output: 点(P+P)
'''
def ECG_double_point(p):
    q = config.get_q()
    # Fp 上的椭圆曲线群
    if isPrime(q):
        if ECG_ele_is_zero(p):
            return p
        else:
            lam = (3 * (p.x**2) + config.get_a()) / (2 * p.y)
            x = lam**2 - 2 * p.x
            y = lam * (p.x - x) - p.y
            return Point(x, y)
    # F2^m 上的椭圆曲线
    if is_Power_of_two(q):
        if ECG_ele_is_zero(p):
            return p
        else:
            lam = p.x + (p.y / p.x)
            x = lam**2 + lam + config.get_a()
            y = p.x**2 + (lam + 1) * x
            return Point(x, y)


# 椭圆曲线求 k 倍点 #
'''
input: 倍数 k 和椭圆曲线点 p
output: p 的 k 倍点
'''
def ECG_k_point(k, p):
    pass
'''
# Fp 椭圆曲线测试 #
config.set_q(23)
config.set_a(1)
config.set_b(1)
### test ECG_ele_add ###
print(ECG_ele_add(Point(3, 10), Point(9, 7)))   #(3, 10) + (9, 7) = (17, 20)
### test ECG_double_point ###
print(ECG_double_point(Point(3, 10)))   # 2(3, 10) = (7, 12)

# F2^m 椭圆曲线测试 #
config.set_q(32)
config.set_fx('0b100101')
config.set_a('0b00001')
config.set_b('0b00001')
### test ECG_ele_add ###
# (01010, 11000) + (01000, 11111) = (11110, 10101)
print(ECG_ele_add(Point('0b01010', '0b11000'), Point('0b01000', '0b11111')))
### test ECG_double_point ###
# [2](01010, 11000) = (01000, 11111)
print(ECG_double_point(Point('0b01010', '0b11000')))
'''
# 6.1 密钥对的生成 #
'''
input: 有效的椭圆曲线系统参数集合
output: 与输入参数相关的一个密钥对(d, P)
'''
def key_pair_generation(parameters):
    pass

# 6.2 公钥的认证 #
'''
input: 有效的椭圆曲线系统参数集合以及一个相关的公钥
output: 若通过验证则输出“有效：， 无效则
'''
def public_key_verification(parameters, public_key):
    pass