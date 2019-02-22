from SM2_Encryption import *

def Enc_Interface(M, PB):
	M = M_to_bits(M)
	PB = PB
	Encryption(M)
	return C

def Dec_Interface(C, dB):
	Decryption(C)
	return M_

### test Enc_Interface() and Dec_Interface() ###
'''
M = '101001010110001010000000000000000000001010101010101010'
PB = Point(115, 48)
dB = 121
print('M ', M)
C = Enc_Interface(M, PB)
print('C ', C)
print('M_', Dec_Interface(C, dB))
'''