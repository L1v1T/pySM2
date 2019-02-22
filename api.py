from Interface import *
from SM2_ECG import key_pair_generation

# 初始化椭圆曲线参数 #
def SM2_init(filename = ''):
    if filename == '':
        config.default_config()
    else:
        parameters = config.read_config_file(filename)
        config.set_parameters(parameters)

# 产生密钥对 #
def SM2_key_pair_gen():
    pk_file = 'public_key'
    sk_file = 'private_key'
    param = config.get_parameters()
    key_pair = key_pair_generation(param)
    print("私钥： " + str(key_pair[0]))
    print("公钥： ")
    print(key_pair[1])
    sk = param
    sk['private key'] = key_pair[0]
    pk = param
    pk['public key'] = bytes_to_str(point_to_bytes(key_pair[1]))

    fo = open(sk_file, "w", encoding = 'utf-8')
    fo.write(str(sk))
    fo.close()
    fo = open(pk_file, "wb")
    fo.write(bytes(str(pk), encoding = 'utf-8'))
    fo.close()
### test key_pair_gen ###
#SM2_init()
#SM2_key_pair_gen()

# 读取公钥文件 #
def SM2_read_public_key(filename):
    parameters = config.read_config_file(filename)
    config.set_parameters(parameters)
    a = config.get_a()
    b = config.get_b()
    return bytes_to_point(a, b, str_to_bytes(parameters['public key']))

# 读取私钥文件 #
def SM2_read_private_key(filename):
    parameters = config.read_config_file(filename)
    config.set_parameters(parameters)
    return parameters['private key']

# 加密文件 #
def SM2_encrypt_file(in_file, public_key_file, out_file = ''):
    # 读公钥
    pk = SM2_read_public_key(public_key_file)
    # 读文件内容
    fo = open(in_file, "ab+")
    fl = fo.tell()
    fo.seek(0, 0)
    m = fo.read(fl)
    fo.close()
    # 加密内容
    c = Enc_Interface(m, pk)
    # 写入输出文件
    if out_file == '':
        out_file = in_file + '.sm2'
    else:
        out_file += '.sm2'
    fo = open(out_file, "wb")
    fo.write(c)
    fo.close()

# 解密文件 #
def SM2_decrypt_file(in_file, private_key_file, out_file = ''):
    # 读私钥
    sk = SM2_read_private_key(private_key_file)
    # 读文件内容
    sl = len(in_file)
    if in_file[sl-3 : sl] != '.sm2':
        print("错误：不正确的文件后缀名（应为'.sm2'）")
        return False
    fo = open(in_file, "ab+")
    fl = fo.tell()
    fo.seek(0, 0)
    c = fo.read(fl)
    fo.close()
    # 解密内容
    m = Dec_Interface(c, sk)
    # 写入输出文件
    if out_file == '':
        out_file = in_file[0 : sl - 3]
    fo = open(out_file, "wb")
    fo.write(m)
    fo.close()
    return True

# 加密字符串 #
def SM2_encrypt_str(data, public_key_file):
    # 读公钥
    pk = SM2_read_public_key(public_key_file)
    return Enc_Interface(data, pk)

# 解密字符串 #
def SM2_decrypt_str(data, private_key_file):
    sk = SM2_read_private_key(private_key_file)
    return Dec_Interface(data, sk)

### test encrypt_str ###
SM2_init()
SM2_key_pair_gen()
c = SM2_encrypt_str("hello world", "public_key")
print("密文：" + c)
m = SM2_decrypt_str(c, "private_key")
print("解密结果： " + m)