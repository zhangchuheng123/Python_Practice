# Description

This is a simple code for DEC (Data Encryption Standard) 
is a kind of symmetry block cipher standarded by NIST 
many years ago. It enciphers using a 8-byte data block 
and a 64-bit key (though only 56 bits contribute to 
security). DES is weak due to short key size and later 
replaced by AES().

The code is a simple DES encipher and decipher script 
for illustration. 
The cipher and decipher use ECB mode and PAD_PKCS5.

The usage is 

```python
from des import Des

# a 8-bit key
key = b'Eightbit'
# the text or data to be enciphered
plain_text = b'sona si latine loqueris '

des = Des(key)
code = des.encrypt(plain_text)
text = des.decrypt(code)

```