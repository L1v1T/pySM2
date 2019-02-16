
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