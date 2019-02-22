import hashlib
import math
from random import randint
from SM2_Code import *
from SM2_ECG import *
from Point import *
from config import *
from binary import *

# hash函数
def hash_function(m):
	sha256 = hashlib.sha256()
	sha256.update(m.encode("utf8"))
	sha256 = bin(int(sha256.hexdigest(), 16))
	sha256 = padding_0_to_length(sha256, 32*8)
	return sha256
### test hash_function ###
print('1--',hash_function('akjkSsd'))
print('2--',hash_function('asd'))
#print('3--',hash_function('100000000101100001101100000000'))

# 密钥派生函数
'''
input：比特串Z，整数klen(表示要获得的密钥数据的比特长度，要求该值小于(2^32-1)*v)
output：长度为klen的密钥数据比特串K
'''
def KDF(Z, klen):
	if(klen < (2**32-1)*v):
		ct=0x00000001
		H = []
		H_ = []
		for i in range(0, math.ceil(klen/v)):
			H.append(remove_0b_at_beginning(hash_function(Z+str(ct))))
			ct = ct + 1
		if (klen/v == math.ceil(klen/v)):
			H_ = remove_0b_at_beginning(H[math.ceil(klen/v)-1])
		else:
			H_ = remove_0b_at_beginning(H[math.ceil(klen/v)-1][0:(klen-(v*math.floor(klen/v)))])
		K = ''
		for i in range(0, math.ceil(klen/v)):
			if(i != math.ceil(klen/v)-1):
				K = K + H[i]
			else:
				K = K + H_
	else:
		print("*** ERROR: klen要小于(2^32-1)*v *** function: KDF(Z, klen) ***")
	return K
### test KDF(Z,klen) ###
#v = 256
#print('KDF result', KDF('1101', 10))

def PRG_function(a, b):
	return randint(a, b)

# 判断a是否为全0比特串
def is_zero_bits(a):
	for i in a:
		if(i != '0'):
			return False
	return True

def Encryption(M):
	klen = len(M)
	t = '000000'
	while(is_zero_bits(t)):
		# A1：用随机数发生器产生随机数k∈[1,n-1]
		k = PRG_function(1, n-1)
		# A2.1：计算椭圆曲线点C1=[k]G=(x1,y1)
		# A2.2：按本文本第1部分4.2.8和4.2.4给出的细节，将C1的数据类型转换为比特串
		C1 = ECG_k_point(k, G)
		C1 = point_to_bytes(C1)
		C1 = bytes_to_bits(C1)

		# A3：计算椭圆曲线点S=[h]PB，若S是无穷远点，则报错并退出
		#S = ECG_k_point(h, G)
		#if():
		#	return -1

		# A4.1：计算椭圆曲线点[k]PB=(x2,y2)
		# A4.2：按本文本第1部分4.2.5和4.2.4给出的细节，将坐标x2、y2的数据类型转换为比特串
		x2 = ECG_k_point(k, PB).x
		y2 = ECG_k_point(k, PB).y
		x2 = bytes_to_bits(ele_to_bytes(x2))
		y2 = bytes_to_bits(ele_to_bytes(y2))	
		x2 = remove_0b_at_beginning(x2)
		y2 = remove_0b_at_beginning(y2)
		# A5：计算t=KDF(x2 ∥y2, klen)，若t为全0比特串，则返回A1
		t = KDF(x2+y2,klen)
	# A6：计算C2 = M ⊕t
	M = remove_0b_at_beginning(M)
	C2 = bin( int(M, 2)^int(t, 2) )
	C2 = padding_0_to_length(C2, klen)
	# A7：计算C3 = Hash(x2 ∥ M ∥ y2)
	C3 = hash_function(x2+M+y2)
	# A8：输出密文C = C1 ∥ C2 ∥ C3
	C1 = remove_0b_at_beginning(C1)
	C2 = remove_0b_at_beginning(C2)
	C3 = remove_0b_at_beginning(C3)
	C = C1 + C2 + C3
	return C
### test Encryption ###
# 密钥对生成
parameters = {  'q' : 211, 
                'f(x)' : polynomial_zero(), 
                'a' : 0, 
                'b' : 207, 
                'n' : 211, 
                'G' : Point(2, 2)}
key = key_pair_generation(parameters)
dB = key[0]
PB = key[1]

config.set_q(211)
config.set_a(0)
config.set_b(207)
#point = Point('0b100000000', '0b100000000')
#print(point_to_bytes(point))
q = config.get_q()
n = 10
G = Point(2, 2)
#PB = Point(115, 48)
v = 256
M = '101111111111111111111111111110000001111111111111111111111111111111111'
C = Encryption(M)


def Decryption(C):
	# B1.1：从C中取出比特串C1
	# B1.2：按本文本第1部分4.2.3和4.2.9给出的细节，将C1的数据类型转换为椭圆曲线上的点
	# B1.3：验证C1是否满足椭圆曲线方程，若不满足则报错并退出
	C1 = C[0:19]
	C2 = C[19:len(C)-256]
	C3 = C[len(C)-256:len(C)]
	C1 = '0b'+C1
	C1 = bytes_to_point(a, b, bits_to_bytes(C1))
	# B2：计算椭圆曲线点S=[h]C1，若S是无穷远点，则报错并退出

	# B3.1：计算[dB]C1=(x2,y2)
	# B3.2：按本文本第1部分4.2.5和4.2.4给出的细节，将坐标x2、y2的数据类型转换为比特串
	x2 = ECG_k_point(dB, C1).x
	y2 = ECG_k_point(dB, C1).y
	x2 = bytes_to_bits(ele_to_bytes(x2))
	y2 = bytes_to_bits(ele_to_bytes(y2))
	# B4：计算t=KDF(x2 ∥y2, klen)，若t为全0比特串，则报错并退出
	klen = len(C2)
	x2 = remove_0b_at_beginning(x2)
	y2 = remove_0b_at_beginning(y2)
	t = KDF(x2+y2, klen)
	if(is_zero_bits(t)):
		print("*** ERROR: t为全0比特串 *** function: Decryption ***")
		return -1
	# B5：从C中取出比特串C2，计算M′ = C2 ⊕t
	M_ = bin(int(C2, 2) ^ int(t, 2))
	# B6：计算u = Hash(x2 ∥ M′ ∥ y2)，从C中取出比特串C3，若u ̸= C3，则报错并退出
	x2 = remove_0b_at_beginning(x2)
	M_ = remove_0b_at_beginning(M_)
	y2 = remove_0b_at_beginning(y2)
	u = hash_function(x2+M_+y2)
	if(remove_0b_at_beginning(u) != remove_0b_at_beginning(C3)):
		print("*** ERROR: u不等于C3 *** function: Decryption ***")
		return -1
	# B7：输出明文M′
	return M_
### test ###
#dB = 121
a = config.get_a()
b = config.get_b()
M_ = Decryption(C)
print('M ',M)
print('M_', M_)