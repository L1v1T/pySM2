import hashlib
import math
from random import randint
from SM2_ECG import *
from Integer import inverse
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

def PRG_function(a, b):
	return randint(a, b)

def Signature(M, dA, PA):
	a = config.get_a()
	a = bytes_to_bits(ele_to_bytes(a))
	b = config.get_b()
	b = bytes_to_bits(ele_to_bytes(b))
	n = config.get_n()
	Gx = config.get_Gx()
	Gx_ = bytes_to_bits(ele_to_bytes(Gx))
	Gy = config.get_Gy()
	Gy_ = bytes_to_bits(ele_to_bytes(Gy))
	ID = dA
	ID = bytes_to_bits(ele_to_bytes(ID))
	ENTL = int_to_bytes(len(ID), 2)
	ENTL = bytes_to_bits(ENTL)
	xA = bytes_to_bits(ele_to_bytes(PA.x))
	yA = bytes_to_bits(ele_to_bytes(PA.y))
	Z = hash_function(ENTL+ID+a+b+Gx_+Gy_+xA+yA)
	# A1：置M=ZA ∥ M
	M_ = Z + M
	# A2：计算e = Hv(M)，按本文本第1部分4.2.3和4.2.2给出的细节将e的数据类型转换为整数
	e = hash_function(M_)
	e = bytes_to_int(bits_to_bytes(e))
	r = 0
	k = 0
	while(r==0 or r+k==n):
		# A3：用随机数发生器产生随机数k ∈[1,n-1]
		k = PRG_function(1, n-1)
		# A4：计算椭圆曲线点(x1,y1)=[k]G，按本文本第1部分4.2.7给出的细节将x1的数据类型转换为整 数
		x1 = ECG_k_point(k, Point(Gx, Gy)).x
		x1 = bytes_to_int(ele_to_bytes(x1))
		# A5：计算r=(e+x1) modn，若r=0或r+k=n则返回A3
		r = (e+x1)%n
	# A6：计算s = ((1 + dA)−1 ·(k−r·dA)) modn，若s=0则返回A3
	s = ( inverse(1+dA, n)*(k-r*dA) ) % n	
	# A7：按本文本第1部分4.2.1给出的细节将r、s的数据类型转换为字节串，消息M 的签名为(r,s)。
	#Sig = Point(int_to_bytes(r, math.ceil(n/256)), int_to_bytes(s, math.ceil(n/256)))
	#Sig = Point(int_to_bytes(r, math.ceil(math.log(n, 2)/8)), int_to_bytes(s, math.ceil(math.log(n, 2)/8)))
	r = int_to_bytes(r, math.ceil(math.log(n, 2)/8))
	s = int_to_bytes(s, math.ceil(math.log(n, 2)/8))
	Sig = r
	for i in s:
		Sig.append(i)
	return Sig

def Verification(M, Sig, dA, PA):
	a = config.get_a()
	a = bytes_to_bits(ele_to_bytes(a))
	b = config.get_b()
	b = bytes_to_bits(ele_to_bytes(b))
	n = config.get_n()
	Gx = config.get_Gx()
	Gx_ = bytes_to_bits(ele_to_bytes(Gx))
	Gy = config.get_Gy()
	Gy_ = bytes_to_bits(ele_to_bytes(Gy))
	ID = dA
	ID = bytes_to_bits(ele_to_bytes(ID))
	ENTL = int_to_bytes(len(ID), 2)
	ENTL = bytes_to_bits(ENTL)
	xA = bytes_to_bits(ele_to_bytes(PA.x))
	yA = bytes_to_bits(ele_to_bytes(PA.y))
	Z = hash_function(ENTL+ID+a+b+Gx_+Gy_+xA+yA)
	r = Sig[0:int(len(Sig)/2)]
	s = Sig[int(len(Sig)/2): len(Sig)]
	r = bytes_to_int(r)
	s = bytes_to_int(s)
	if(r<1 or r>n-1 or s<1 or s>n-1):
		print("wrong signature: r,s wrong range")
		return False
	M_ = Z + M
	e = hash_function(M_)
	e = bytes_to_int(bits_to_bytes(e))
	t = (r + s) % n
	if(t == 0):
		print("wrong signature : t is 0")
		return False

	x1 = ECG_ele_add( ECG_k_point(s, Point(Gx, Gy)), ECG_k_point(t, PA) ).x
	R = (e + x1) % n
	if R!=r:
		print("wrong signature: R unequal r")
		return False
	print("true signature")
	return True

'''
### test Signature ###
config.default_config()
#dA = 121
#Gx = config.get_Gx()
#Gy = config.get_Gy()
#PA = ECG_k_point(dA, Point(Gx,Gy))
parameters = config.get_parameters()
key = key_pair_generation(parameters)
dA = key[0]
PA = key[1]
M = '100'
Sig = Signature(M, dA, PA)
print(Sig)

### test Verification ###
Verification(M, Sig, dA, PA)

#print('ECG_k_point(2, PA)', ECG_k_point(2, Point(2,2)))
#print('ECG_ele_add( ECG_k_point(1, PA), ECG_k_point(2, PA) )', ECG_k_point(4, ECG_k_point(2, Point(2,2))))
#print('ECG_k_point(3, PA)', ECG_k_point(8, Point(2,2)))	
'''