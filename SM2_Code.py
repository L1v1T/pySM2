import math
# 4.2.1 整数到字节串的转换
'''
input：非负整数x，以及字节串的目标长度k  
output：长度为k的字节串M
'''
def int_to_bytes(x, k):
	#print("--- 整数到字节串的转换 ---")
	#temp = x
	#i = k - 1
	M = []
	for i in range(0, k):
		M.append(x >> (i*8) & 0xff)
	M.reverse()
	'''
	M = ''
	while (i >= 0):
		a = temp // (2**(8*i))
		M = M + str(a)
		temp = temp - a * (2**(8*i))
		i = i - 1
	'''
	return M
#''' 
### test int_to_bytes ###
#print(int_to_bytes(255,5))   #[0, 0, 0, 0, 255]
#'''

# 4.2.2 字节串到整数
'''
input：长度为k的字节串M
output：整数x
'''
def bytes_to_int(M):
	#print("--- 字节串到整数的转换 ---")
	#k = int(len(M))
	#i = 0
	x = 0
	for b in M:
		x = x * 256 + int(b)
	'''
	while (i < k):
		x = x + int( M[k-i-1:k-i] ) * (2**(8*i)) 
		i = i + 1
	'''
	return x
'''
### test bytes_to_int ###
print(bytes_to_int('0020'))   # 257
'''

# 4.2.3 比特串到字节串
'''
intput：长度为m的比特串s
output：长度为k的字节串M，其中k=m/8(上整)
'''
def bits_to_bytes(s):
	#print("--- 比特串到字节串的转换 ---")
	if s[0:2] == '0b':
		s = s.replace('0b', '')
		m = len(s)
		k = math.ceil(m/8)
		M = []
		for i in range(0, k):
			temp = ''
			j = 0
			while j < 8:
				if(8*i+j >= m):
					#M.append(s >> 0 & 0xff)
					temp = temp + '0'
				else:
					#M.append(s >> (i*8) & 0xff)
					temp = temp + s[m-(8*i+j)-1:m-(8*i+j)]
					#print(i , "-", j, "-", m-(8*i+j)-1, "-", temp)
				j = j + 1
			temp = temp[::-1]
			M.append(temp)
			#M = M + temp
	else:
		print("*** ERROR: 输入必须为比特串 *** function：bits_to_bytes(s) ***")
		return -1;
	return M
'''
### test bits_to_bytes ###
'''
#print(bits_to_bytes('0b100011111101'))

#'''

# 4.2.4 字节串到比特串
'''
input：长度为k的字节串M
output：长度为m的比特串s，其中m=8k
'''
def bytes_to_bits(M):
	#print("--- 字节串到比特串的转换 ---")
	k = len(M)
	m = 8*k
	temp = ''
	s = 0
	M.reverse()
	for i in M:
		s = s*256 + i
	s = bin(s)
	return s
### test bytes_to_bits ###
#print(bytes_to_bits([2,2])) 

# 判断素数 #
def isPrime(n):    
	if n <= 1:
		return False
	i = 2
	while i*i <= n: 
		if n % i == 0:  
			return False
		i += 1
	return True

# 判断是否为2的幂
def is_Power_of_two(n):
	if n>0:
		if (n&(n-1))==0 :
			return True
	return False
#if is_Power_of_two(45):
#	print('true')

# 4.2.5 域元素到字节串
'''
input：Fq中的元素a，模数q
output：长度l=t/8（取上整）的字节串S，其中t=lb(q)(取上整)
'''
def ele_to_bytes(a):
	#print("--- 域元素到字节串的转换 ---")
	S = []

	# q为奇素数
	if (a>=0 and a<=q-1):
		t = math.ceil(math.log(q,2))
		l = math.ceil(t/8)
		S = int_to_bytes(a, l)
	else:
		print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：ele_to_bytes(a) ***")
		return -1;
	
	return S

def ele_to_bytes_2m(a):
	#print("--- 域元素到字节串的转换 ---")
	S = []
	
	# q为2的幂
	if type(a)==str and a[0:2] == '0b':
		m = math.log(q, 2)
		if len(a)-2 == m:
			S = bits_to_bytes(a)
		else:
			print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_bytes(a, q)")
			return -1;
	else:
		print("*** ERROR: 输入必须为比特串 *** function：ele_to_bytes(a, q) ***")
		return -1;
	
	return S
'''
def ele_to_bytes(a, q):
	#print("--- 域元素到字节串的转换 ---")
	S = []
	if (isPrime(q) and q%2 ==1):   # q为奇素数
		if (a>=0 and a<=q-1):
			t = math.ceil(math.log(q,2))
			l = math.ceil(t/8)
			S = int_to_bytes(a, l)
		else:
			print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：ele_to_bytes(a, q) ***")
			return -1;
	elif is_Power_of_two(q):    # q为2的幂
		if type(a)==str and a[0:2] == '0b':
			m = math.log(q, 2)
			if len(a)-2 == m:
				S = bits_to_bytes(a)
			else:
				print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_bytes(a, q)")
				return -1;
		else:
			print("*** ERROR: 输入必须为比特串 *** function：ele_to_bytes(a, q) ***")
			return -1;
	else:
		print("*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_bytes(a, q) ***")
		return -1;
	return S
'''
### test ele_to_bytes ###
#print(ele_to_bytes(256, 257))
#print(ele_to_bytes('0b101101010', 512))

# 4.2.6 字节串到域元素
'''
input：基域Fq的类型（模数q），长度为l=t/8（取上整）的字节串S，其中t=lb(q)(取上整)
output：Fq中的元素a
'''
def bytes_to_ele(q, S):
	a = ''
	if (isPrime(q) and q%2 ==1):   # q为奇素数
		a = 0
		t = math.ceil(math.log(q,2))
		l = math.ceil(t/8)
		a = bytes_to_int(S)
		if not (a>=0 and a<=q-1):
			print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：bytes_to_ele(q, S) ***")
			return -1;
	elif is_Power_of_two(q):    # q为2的幂
		m = math.log(q, 2)
		a = bytes_to_bits(S)
		if not len(a)-2 == m:
			print("*** ERROR: 域元素必须为长度为m的比特串 *** function：bytes_to_ele(q, S)")
			return -1;
	else:
		print("*** ERROR: q不满足奇素数或2的幂 *** function：bytes_to_ele(q, S) ***")
		return -1;
	return a
### test bytes_to_ele(q, S) ###
#print(bytes_to_ele(257, '20'))
#print(bytes_to_ele(256, [232]))

# 4.2.7 域元素到整数
'''
input：域Fq中的元素a，模数q
output：整数x
'''
def ele_to_int(a):
	#print("--- 域元素到字节串的转换 ---")
	x = 0
	 # q为奇素数
	x = a
	return x

def ele_to_int_2m(a):
	#print("--- 域元素到字节串的转换 ---")
	x = 0
	# q为2的幂
	if type(a)==str and a[0:2] == '0b':
		m = math.log(q, 2)
		if len(a)-2 == m:
			a = a.replace('0b', '')
			for i in a:
				x = x * 2 + int(i)
		else:
			print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_int(a, q)")
			return -1;
	else:
		print("*** ERROR: 输入必须为比特串 *** function：ele_to_int(a, q) ***")
		return -1;
	return x
'''
def ele_to_int(a, q):
	#print("--- 域元素到字节串的转换 ---")
	x = 0
	if (isPrime(q) and q%2 ==1):   # q为奇素数
		x = a
	elif is_Power_of_two(q):    # q为2的幂
		if type(a)==str and a[0:2] == '0b':
			m = math.log(q, 2)
			if len(a)-2 == m:
				a = a.replace('0b', '')
				for i in a:
					x = x * 2 + int(i)
			else:
				print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_int(a, q)")
				return -1;
		else:
			print("*** ERROR: 输入必须为比特串 *** function：ele_to_int(a, q) ***")
			return -1;
	else:
		print("*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_int(a, q) ***")
		return -1;
	return x
'''
### test ele_to_int ###
#print(ele_to_int(256, 257))
#print(ele_to_int('0b1011', 16))

# 4.2.8 点到字符串
'''
input：椭圆曲线上的点P=(xp,yp)，且P!=Q
output：字节串S。
			若选用未压缩表示形式或混合表示形式，则输出字节串长度为2l+1；
			若选用压 缩表示形式，则输出字节串长度为l+1。
			（l=lb(q)/8(取上整)）
'''
def point_to_bytes(x, y):
	print('x', x)
	S = []
	PC = []
	# a. 将域元素x转换成长度为l的字节串X
	X = ele_to_bytes(x)
	print('字节串X', X)
	'''
	##### b. 压缩表示形式 #####
	# b.1 计算比特y1
	temp = ele_to_bytes(y)
	y1_temp = bytes_to_bits(temp)#[math.ceil(math.log(q,2)/8)*8-1:math.ceil(math.log(q,2)/8)*8]
	y1 = y1_temp[len(y1_temp)-1:len(y1_temp)]
	#print('y1', y1)
	# b.2 若y1=0，则令PC=02；若y1=1，则令PC=03
	if y1 == '0':
		PC = '02'
	elif y1 == '1':
		PC = '03'
	else:
		print('ERROR')
	# b.3 字节串S=PC||X
	S.append(PC)
	for i in X:
		S.append(i)
	'''
	'''
	##### c. 未压缩表示形式 #####
	# c.1 将域元素y转换成长度为l的字节串Y
	Y = ele_to_bytes(y)
	# c.2 令PC=04
	PC = '04'
	# c.3 字节串S=PC||X||Y
	S.append(PC)
	for m in X:
		S.append(m)
	for n in Y:
		S.append(n)
	'''
	##### d. 混合表示形式 #####
	# d.1 将域元素y转换成长度为l的字节串Y
	Y = ele_to_bytes(y)
	# d.2 计算比特y1
	y1_temp = bytes_to_bits(Y)#[math.ceil(math.log(q,2)/8)*8-1:math.ceil(math.log(q,2)/8)*8]
	y1 = y1_temp[len(y1_temp)-1:len(y1_temp)]
	# d.3 若y1=0，则令PC=06；若y1=1，则令PC=07
	if y1 == '0':
		PC = '06'
	elif y1 == '1':
		PC = '07'
	else:
		print('ERROR')
	# d.4 字节串S=PC||X||Y
	S.append(PC)
	for m in X:
		S.append(m)
	for n in Y:
		S.append(n)
	return S
### test point_to_bytes
q = 1024
print(point_to_bytes(256, 256))


# 4.2.9 字符串到点
'''
input：定义Fq上椭圆曲线的域元素a、b，字节串S
output：椭圆曲线上的点P=(xp,yp)，且P!=Q
'''
def bytes_to_point(a, b, S):
	l = math.ceil(math.lb(q)/8)
	PC = []
	X = []
	Y = []
	# a. 
	if len(S) == 2*l+1: #为压缩表示形式或者混合表示形式
		PC = S[0]
		for i in range(1,l):
			X.append(S[i])
		for i in range(l+1, 2l):
			Y.append(s[i])
	elif len(S) == l+1: #压缩表示形式
		PC = S[0]
		for i in range(1,l):
			X.append(S[i])
	else:
		print('ERROR')
	# b. 将X转换成与元素x
	x = bytes_to_ele(X)
	##### c. 压缩表示形式 #####
	y1 = ''
	# c.1 and c.2
	if PC == '02':
		y1 = '0'
	elif PC == '03':
		y1 = '1'
	else:
		print('ERROR in bytes_to_point')
	# c.3
	##### d. 未压缩表示形式 #####
	if PC == '04':
		y = bytes_to_ele(Y)
	else:
		print('ERROR in bytes_to_point')
	##### e. 混合表示形式 #####
	# e.1
	# e.2 执行e.2.1或e.2.2
	# # e.2.1
	# # e.2.2
	# f. 
	# g. 
	return