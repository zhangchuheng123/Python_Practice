from des import Des
from Crypto.Cipher import DES

key = b'Eightbit'
plain_text = b'sona si latine loqueris '

des = Des(key)
code = des.encrypt(plain_text)
print(code)
text = des.decrypt(code)
print(text)

des = DES.new(key, DES.MODE_ECB)
code = des.encrypt(plain_text + b''.join(b'\x08' for i in range(0, 8)))
print(code)
text = des.decrypt(code)
print(text)
