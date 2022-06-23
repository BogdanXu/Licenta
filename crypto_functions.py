from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def OFB_encrypt(plaintext, key):
    
    if isinstance(plaintext,str):
        plaintext = bytes(plaintext, 'utf-8')
    if isinstance(key, str):
        key = bytes(key, 'utf-8')
    print("Size of plaintext in bytes: ", len(plaintext))
    cipher = AES.new(key, AES.MODE_OFB)
    ct_bytes = cipher.encrypt(plaintext)
    print("Size of ciphertext in bytes: ", len(ct_bytes))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    print("Size of ciphertext in bytes in base64: ", len(ct))
    result = (iv, ct)
    return result

def OFB_decrypt(result, key):

    if isinstance(key, str):
        key = bytes(key, 'utf-8')
    iv = b64decode(result[0])
    ct = b64decode(result[1])
    print(iv, " ", ct)
    cipher = AES.new(key, AES.MODE_OFB, iv = iv)
    pt = cipher.decrypt(ct)
    #print("Decrypted:", pt)
    return pt


