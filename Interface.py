from SM2_Encryption import *
import config
from Integer import *

def Enc_Interface(M, PB):
	
	q, fx, a, b, n, Gx, Gy = config.get_parameters()
	M = M_to_bits(M)
	PB = PB
	C = Encryption(M, PB)
	return C

def Dec_Interface(C, dB):
	M_ = Decryption(C, dB)
	return bits_to_M(M_)

'''
### test Enc_Interface() and Dec_Interface() ###
parameters = {  'q' : 211, 
                'f(x)' : polynomial_zero(), 
                'a' : 0, 
                'b' : 207, 
                'n' : 211, 
                'Gx' : 2, 
                'Gy' : 2
                }
config.set_parameters(parameters)
M = ['aa', 's']
PB = Point(115, 48)
dB = 121
print('M ', M)
C = Enc_Interface(M, PB)
print('C ', C)
print('M_', Dec_Interface(C, dB))
'''