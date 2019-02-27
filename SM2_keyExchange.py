import hashlib
import math
from random import randint
from SM2_ECG import *
import config

# hash函数
def hash_function(m):
	sha256 = hashlib.sha256()
	sha256.update(m.encode("utf8"))
	sha256 = bin(int(sha256.hexdigest(), 16))
	sha256 = padding_0_to_length(sha256, 32*8)
	return sha256
### test hash_function ###
#print('1--',hash_function('akjkSsd'))
#print('2--',hash_function('asd'))
#print('3--',hash_function('100000000101100001101100000000'))

# 密钥派生函数
'''
input：比特串Z，整数klen(表示要获得的密钥数据的比特长度，要求该值小于(2^32-1)*v)
output：长度为klen的密钥数据比特串K
'''
def KDF(Z, klen):
	v = config.get_v()
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

def get_Z(ID, PA):
	a = config.get_a()
	a = bytes_to_bits(ele_to_bytes(a))
	b = config.get_b()
	b = bytes_to_bits(ele_to_bytes(b))
	n = config.get_n()
	Gx = config.get_Gx()
	Gx_ = bytes_to_bits(ele_to_bytes(Gx))
	Gy = config.get_Gy()
	Gy_ = bytes_to_bits(ele_to_bytes(Gy))

	ID = bytes_to_bits(str_to_bytes(ID))
	ENTL = int_to_bytes(math.ceil((len(ID)-2)/8)*8, 2)
	ENTL = bytes_to_bits(ENTL)
	xA = bytes_to_bits(ele_to_bytes(PA.x))
	yA = bytes_to_bits(ele_to_bytes(PA.y))
	ZA = hash_function(ENTL+ID+a+b+Gx_+Gy_+xA+yA)
	return ZA
### test get_Z ###
#ID = 'ALICE123@YAHOO.COM'
#ID = 'BILL456@YAHOO.COM'
#ID = str_to_bytes(ID)
#ID = bytes_to_bits(ID)
#print(ID)
#ENTL = int_to_bytes(math.ceil((len(ID)-2)/8)*8, 2)
#ENTL = bytes_to_bits(ENTL)
#print(ENTL)

def key_generation_A_1():
	n = config.get_n()
	Gx = config.get_Gx()
	Gy = config.get_Gy()
	# A1. 用随机数发生器产生随机数rA ∈[1, n-1]
	rA = PRG_function(1, n-1)
	# A2. 计算椭圆曲线点RA = [rA]G=(x1,y1)
	RA = ECG_k_point(rA, Point(Gx, Gy))
	# A3. 将RA发送给用户B
	return RA, rA

def key_generation_B_1(IDA, IDB, RA, dB, PA, klen):
	q = config.get_q()
	a = config.get_a()
	b = config.get_b()
	n = config.get_n()
	Gx = config.get_Gx()
	Gy = config.get_Gy()
	h = config.get_h()
	w = math.ceil( math.ceil( math.log(n, 2) )/2 ) - 1
	ZA = get_Z(IDA, PA)
	ZB = get_Z(IDB, PB)
	# B1. 用随机数发生器产生随机数rB∈[1, n-1]
	rB = PRG_function(1, n-1)
	# B2. 计算椭圆曲线点RB = [rB]G=(x2,y2)
	RB = ECG_k_point(rB, Point(Gx, Gy))
	# B3. 从RB中取出域元素x2，将x2的数据类型转换为整数，计算x2_ = 2w +(x2&(2w−1))
	x2 = RB.x
	x2 = ele_to_int(x2)
	y2 = RB.y
	y2 = ele_to_int(y2)
	x2_ = 2**w + (x2 & (2**w - 1))
	# B4. 计算tB = (dB + x2_·rB)modn
	tB = (dB+x2_*rB) % n
	# B5.1 验证RA是否满足椭圆曲线方程，若不满足则协商失败；
	# B5.2 否则从RA中取出域元素x1，将x1的数据类型转换为整数，计算x1_ = 2w +(x1&(2w−1))
	x1 = RA.x
	x1 = ele_to_int(x1)
	y1 = RA.y
	y1 = ele_to_int(y1)
	if (y1**2)%q != (x1**3 + a*x1 + b)%q:
		print("keyExchange Fail: RA do not satisfy the equation")
		return -1
	x1_ = 2**w + (x1 & (2**w - 1))
	# B6. 计算椭圆曲线点V = [h·tB](PA +[x1_]RA) = (xV,yV)
	# 若V是无穷远点，则B协商失败；否则将xV、yV 的数据类型转换为比特串
	V = ECG_k_point(h*tB, ECG_ele_add(PA, ECG_k_point(x1_, RA)))
	if V.x == ECG_ele_zero().x and V.y == ECG_ele_zero().y:
		print('keyExchange Fail: V is zero point')
		return -1
	xV = V.x
	yV = V.y
	xV = bytes_to_bits(ele_to_bytes(xV))
	xV = remove_0b_at_beginning(xV)
	yV = bytes_to_bits(ele_to_bytes(yV))
	yV = remove_0b_at_beginning(yV)
	# B7. 计算KB=KDF(xV ∥yV ∥ZA ∥ZB,klen)
	kB = KDF(xV+yV+ZA+ZB, klen)
	print('kB', kB)
	# B8.1 (选项)将RA的坐标x1、y1 和RB的坐标x2、y2的数据类型转换为比特串
	# B8.2 计算SB= Hash(0x02∥yV ∥Hash(xV ∥ZA ∥ZB ∥x1 ∥y1 ∥x2 ∥y2))
	x1 = bytes_to_bits(ele_to_bytes(x1))
	x1 = remove_0b_at_beginning(x1)
	y1 = bytes_to_bits(ele_to_bytes(y1))
	y1 = remove_0b_at_beginning(y1)
	x2 = bytes_to_bits(ele_to_bytes(x2))
	x2 = remove_0b_at_beginning(x2)
	y2 = bytes_to_bits(ele_to_bytes(y2))
	y2 = remove_0b_at_beginning(y2)
	prefix = remove_0b_at_beginning(bytes_to_bits(int_to_bytes(2, 1)))
	SB = hash_function(prefix+yV+hash_function(xV+ZA+ZB+x1+y1+x2+y2))
	SB = remove_0b_at_beginning(SB)
	# B9. 将RB、(选项SB)发送给用户A
	return RB, SB, xV, yV, ZA, ZB, x1, y1, x2, y2

def key_generation_A_2(IDA, IDB, rA, RA, RB, SB, PB, klen):
	q = config.get_q()
	a = config.get_a()
	b = config.get_b()
	n = config.get_n()
	Gx = config.get_Gx()
	Gy = config.get_Gy()
	h = config.get_h()
	w = math.ceil( math.ceil( math.log(n, 2) )/2 ) - 1
	ZA = get_Z(IDA, PA)
	ZB = get_Z(IDB, PB)
	# A4. 从RA中取出域元素x1，将x1的数据类型转换为整数，计算x1_ = 2w +(x1&(2w−1))； 
	x1 = RA.x
	x1 = ele_to_int(x1)
	y1 = RA.y
	y1 = ele_to_int(y1)
	x1_ = 2**w + (x1 & (2**w - 1))
	# A5. 计算tA = (dA + ¯ x1·rA)modn
	tA = (dA+x1_*rA) % n
	# A6.1 验证RB是否满足椭圆曲线方程，若不满足则协商失败；
	# A6.2 否则从RB中取出域元素x2，将x2的数据类型转换为整数，计算x2_ = 2w +(x2&(2w−1))； 
	x2 = RB.x
	x2 = ele_to_int(x2)
	y2 = RB.y
	y2 = ele_to_int(y2)
	if (y2**2)%q != (x2**3 + a*x2 + b)%q:
		print("keyExchange Fail: RB do not satisfy the equation")
		return -1
	x2_ = 2**w + (x2 & (2**w - 1))
	# A7.1 计算椭圆曲线点U = [h·tA](PB +[x2_]RB) = (xU,yU)
	# A7.2 若U是无穷远点，则A协商失败；否则将xU、yU的数据类型转换为比特串
	U = ECG_k_point(h*tA, ECG_ele_add(PB, ECG_k_point(x2_, RB)))
	xU = U.x
	yU = U.y
	xU = bytes_to_bits(ele_to_bytes(xU))
	xU = remove_0b_at_beginning(xU)
	yU = bytes_to_bits(ele_to_bytes(yU))
	yU = remove_0b_at_beginning(yU)
	# A8. 计算KA=KDF(xU ∥yU ∥ZA ∥ZB,klen)
	kA = KDF(xU+yU+ZA+ZB, klen)
	print('kA', kA)
	# A9. 将RA的坐标x1、y1 和RB的坐标x2、y2的数据类型转换为比特串
	# 计算S1= Hash(0x02∥yU ∥Hash(xU ∥ZA ∥ZB ∥x1 ∥y1 ∥x2 ∥y2))
	# 并检验S1=SB是否成立，若等式不成立则从B到A的密钥确认失败；
	x1 = bytes_to_bits(ele_to_bytes(x1))
	x1 = remove_0b_at_beginning(x1)
	y1 = bytes_to_bits(ele_to_bytes(y1))
	y1 = remove_0b_at_beginning(y1)
	x2 = bytes_to_bits(ele_to_bytes(x2))
	x2 = remove_0b_at_beginning(x2)
	y2 = bytes_to_bits(ele_to_bytes(y2))
	y2 = remove_0b_at_beginning(y2)
	prefix = remove_0b_at_beginning(bytes_to_bits(int_to_bytes(2, 1)))
	S1 = hash_function(prefix+yU+hash_function(xU+ZA+ZB+x1+y1+x2+y2))
	S1 = remove_0b_at_beginning(S1)
	if S1 != SB:
		print('keyExchange Fail: S1 unequal SB')
		return -1
	# A10. (选项)计算SA= Hash(0x03∥yU ∥Hash(xU ∥ZA ∥ZB ∥x1 ∥y1 ∥x2 ∥y2))，并将SA发送给用户B
	prefix = remove_0b_at_beginning(bytes_to_bits(int_to_bytes(3, 1)))
	SA = hash_function(prefix+yU+hash_function(xU+ZA+ZB+x1+y1+x2+y2))
	SA = remove_0b_at_beginning(SA)
	return SA

def key_generation_B_2(xV, yV, ZA, ZB, x1, y1, x2, y2, SA):
	# B10. (选项)计算S2= Hash(0x03∥yV ∥Hash(xV ∥ZA ∥ZB ∥x1 ∥y1 ∥x2 ∥y2))
	# 并检验S2=SA是否成立， 若等式不成立则从A到B的密钥确认失败
	prefix = remove_0b_at_beginning(bytes_to_bits(int_to_bytes(3, 1)))
	S2 = hash_function(prefix+yV+hash_function(xV+ZA+ZB+x1+y1+x2+y2))
	S2 = remove_0b_at_beginning(S1)
	if S2 != SA:
		print('keyExchange Fail: S2 unequal SA')
		return -1
	return

### test keyExchange ###
'''
config.default_config()
#dA = 121
#Gx = config.get_Gx()
#Gy = config.get_Gy()
#PA = ECG_k_point(dA, Point(Gx,Gy))
parameters = config.get_parameters()
key = key_pair_generation(parameters)
dA = key[0]
PA = key[1]
key = key_pair_generation(parameters)
dB = key[0]
PB = key[1]

IDA = 'ALICE123@YAHOO.COM'
IDB = 'BILL456@YAHOO.COM'
RA, rA = key_generation_A_1()
klen = 100
RB, SB, xV, yV, ZA, ZB, x1, y1, x2, y2 = key_generation_B_1(IDA, IDB, RA, dB, PA, klen)
SA = key_generation_A_2(IDA, IDB, rA, RA, RB, SB, PB, klen)
'''