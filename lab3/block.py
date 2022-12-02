# Szyfr blokowy EBC i CBC
# Autor: Maciej Sobczyk
# Python 3.10

from PIL import Image 
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
filename = "plain.bmp" 
filename_out = "plain_encrypted_cbc"
filename_out_ecb = "plain_encrypted_ebc"  
format = "BMP" 

 
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()



# AES requires that plaintexts be a multiple of 16, so we have to pad the data 
def pad(data): 
    return data + b"\x00"*(16-len(data)%16)  
 
     
def process_image(filename): 
    # Opens image and converts it to RGB format for PIL
    key = md5(filename).encode('utf-8')
    im = Image.open(filename) 
    data = im.tobytes()  
 
    # Since we will pad the data to satisfy AES's multiple-of-16 requirement, we will store the original data length and "unpad" it later. 
    original = len(data)  
 
    # Encrypts using desired AES mode (we'll set it to ECB by default) 
    newcbc = aes_cbc_encrypt(key, data)[:original]
    newecb = aes_ecb_encrypt(key, data)[:original]
    imecb = Image.new(im.mode, im.size)
    imecb.putdata(newecb)
    # Create a new PIL Image object and save the old image data into the new image. 
    im2 = Image.new(im.mode, im.size) 
    im2.putdata(newcbc) 
    imecb.save(filename_out+"."+format, format) 
    #Save image 
    im2.save(filename_out_ecb+"."+format, format) 
 
def aes_ecb_encrypt(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(data) 

def aes_cbc_encrypt(key, data):
    iv = b"aaaabbbbccccdddd"
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(data) 


process_image(filename) 

    
