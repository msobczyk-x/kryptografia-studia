# Szyfr blokowy EBC i CBC
# Autor: Maciej Sobczyk
# Python 3.10

#open file
with open('plain.bmp', "rb") as f:
    data = bytearray(f.read()) 

import random
#manipulate data

for i in range(54, len(data), 8):
    for j in range(0, 4):
        data[i+j] = data[i+j] ^ 256 % random.randint(1, 255)

#save file
with open('encrypted.bmp', "wb") as f:
    f.write(data)
    

    
