import os
from cryptography.fernet import Fernet

key = b'Q41f4xES76aa3N_LktPfTDHpoCpHtmBDHYiY0XbOF7w='

fernet = Fernet(key)

def encrypt(textin):
    out = fernet.encrypt(textin.encode())
    return out.decode()


def decrypt(textin):
	out = fernet.decrypt(textin.encode())
	return out.decode()

import os
os.system("clear")

print("Kentel enc-dec system")
print("1>Encrypt")
print("2>Decrypt")
print("0>exit")
print("=====================")

type_part = input("Type>")
if int(type_part) == 0:
	exit()

elif int(type_part)==1:
	os.system("clear")
	print("Kentel enc-dec system ")
	print("======================")
	value = input("enterVal:")
	print(encrypt(value))
elif int(type_part) == 2:
	os.system("clear")
	print("Kentel enc-dec system")
	print("=====================")
	VALUE = input("enterVal:")
	print(decrypt(VALUE))

while int(type_part) !=0 or int(type_part) !=1 or int(type_part) !=2:
	
	print("Unknown Command")
	type_part = input("Type>")


