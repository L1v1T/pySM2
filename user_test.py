#coding=utf-8
import api

pkname = "public_key"
skname = "private_key"

param = input('输入参数文件路径（空路径使用默认参数）：')
api.SM2_init(param)

while True:
    generate_keys = input("是否需要生成密钥对（y/n)：")
    if generate_keys == 'y' or generate_keys == 'Y':
        api.SM2_key_pair_gen()
        print("密钥对生成完毕")
        break
    elif generate_keys == 'n' or generate_keys == 'N':
        break
    else:
        print("请输入 y 或 n")
        continue

q = False
result = ''
while not q:
    data = ''
    while True:
        sf = input("输入 s 加/解密字符串， 输入 f 加/解密文件， 输入 q 退出:")
        if sf == 'q':
            q = True
            break
        elif sf == 's':
            data = input("输入字符串内容（不输入表示使用上次计算结果作为输入）：")
            if data == '':
                data = result
            break
        elif sf == 'f':
            data = input("输入文件路径：")
            break       
        else:
            print("错误的参数，请重新输入")
            continue
    if q:
        break
    while True:
        ed = input("输入 e 进行加密， 输入 d 进行解密， 输入 q 退出：")
        if ed == 'q':
            q = True
            break
        elif ed == 'e':
            api.SM2_read_public_key(pkname)
            if sf == 's':
                result = api.SM2_encrypt_str(str(data), pkname)
                print("加密结果：" + result)
            else:
                api.SM2_encrypt_file(data, pkname)
                print("加密完毕")
            break
        elif ed == 'd':
            api.SM2_read_private_key(skname)
            if sf == 's':
                result = api.SM2_decrypt_str(str(data), skname)
                print("解密结果：" + result)
            else:
                api.SM2_decrypt_file(data, skname)
                print("解密完毕")
            break
        else:
            print("错误的参数，请重新输入")
            continue