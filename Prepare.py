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


def M_to_bits(input):
	M = ''
	if (type(input) == type('a')):
		for i in input:
			temp = int.from_bytes(i.encode('ascii'), byteorder='big', signed=True)
			temp = int_to_bytes(temp, 1)
			temp = remove_0b_at_beginning(bytes_to_bits(temp))
			temp = padding_0_to_length(temp, 8)
			M = M + temp
	if(type(input) == type([])):
		for i in input:
			if (type(i) == type('a')):
				for j in i:
					temp = int.from_bytes(i.encode('ascii'), byteorder='big', signed=True)
					temp = int_to_bytes(temp, 1)
					temp = remove_0b_at_beginning(bytes_to_bits(temp))
					temp = padding_0_to_length(temp, 8)
					M = M + temp
			elif (type(i) == type(0)):
				M = remove_0b_at_beginning(bytes_to_bits(input))
				M = padding_0_to_length(M, 8*math.ceil(len(M)/8))
			else:
				print('*** ERROR: 字节串中类型不为str或者int *** function：M_to_bits(input) ***')
	return M
### test M_to_bits ###
#print(M_to_bits(['aa', 's']))

def bits_to_M(M):
	output = []
	M = '0b'+M
	M = bits_to_bytes(M)
	output = bytes_to_str(M)
	return output
### test bits_to_M ###
#print(bits_to_M('011000010110000101110011'))
