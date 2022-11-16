#Szyfr Cezara i afiniczny - szyfruj i deszyfruj
#Autor: Maciej Sobczyk
#python 3.10
import sys
import argparse

parser = argparse.ArgumentParser(description='Caesar, affine cipher - encrypt, decrypt', formatter_class=argparse.ArgumentDefaultsHelpFormatter)


affine_a_coprime = [1,3,5,7,9,11,15,17,19,21,23,25]



parser.add_argument('-e', '--encrypt', action="store_true", help='encrypt file (pass a plain text file)')
parser.add_argument('-d', '--decrypt', action="store_true", help='decrypt file (pass a encrypted file)' )
parser.add_argument('-c', '--caesar', action="store_true", help='type of cipher - Caesar', default=False)
parser.add_argument('-a', '--affine',  action="store_true", help='type of cipher - Affine (known key)', default=False)
parser.add_argument('-j', action="store_true", help='known-plaintext attack (pass a known-plaintext file)')
parser.add_argument('-k', action="store_true", help='brute-force attack', default=False)


def caesar_encrypt(text, shift):
    result = ""
    
    for i in range(len(text)):
        char = text[i]
        
        # If space, add space
        if char.isspace():
            result += char
        # Encrypt uppercase characters
        elif (char.isupper()):
            result += chr((ord(char) + shift - 65) % 26 + 65)
 
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + shift - 97) % 26 + 97)
 
    return result

def caesar_decrypt(text, shift):
    result = ""

    for i in range(len(text)):
        char = text[i]
        # If space, add space
        if char.isspace():
            result += char
        # Encrypt uppercase characters
        elif (char.isupper()):
            result += chr((ord(char) - shift - 65) % 26 + 65)
 
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) - shift - 97) % 26 + 97)
 
    return result

def affine_decrypt(text, a, b):
    result = ""
    a_inverse = affine_decrypt_helper_inverse(a)
    if a_inverse is None:
        a_inverse = 1
    for i in range(len(text)):
        char = text[i]
        
        # If space, add space
        if char.isspace():
            result += char
        # Decrypt uppercase characters
        elif (char.isupper()):
            result += chr((a_inverse * (ord(char) - 65 - b)) % 26 + 65)
        # Decrypt lowercase characters
        else:
            result += chr((a_inverse * (ord(char) - 97 - b)) % 26 + 97)
            
    return result

def affine_decrypt_helper_inverse(a):
    for i in range(26):
        if (a * i) % 26 == 1:
            return i
    return None
        
def affine_encrypt(text, a, b):
    result = ""

    for i in range(len(text)):
        char = text[i]
        # If space, add space
        if char.isspace():
            result += char
        # Encrypt uppercase characters
        elif (char.isupper()):
            result += chr((a * (ord(char) - 65) + b) % 26 + 65)
        # Encrypt lowercase characters
        else:
            result += chr((a * (ord(char) - 97) + b) % 26 + 97)
 
    return result

# Read file
def file_read(plik):
    file = open(plik, "r")
    text = file.read()
    file.close()
    return text

# Write file
def file_write(text, file):
    file = open(file, "w")
    file.write(text)
    file.close()

# Read key from file, for affine cipher, returns a and b
def read_key(fileName):
    key = file_read(fileName)
    if key is None:
        print("Wrong key file")
        sys.exit()
    elif len(key) == 3:
        a, b = key.split()
        return int(a) ,int(b)
    else:
        return int(key), 0



if __name__ == "__main__":
    args = parser.parse_args()

    if (args.encrypt):
        text = file_read("plain.txt")
        if (args.caesar):
            print("Caesar cipher - encrypt")
            a, b = read_key("key.txt")
            if b != 0:
                text = caesar_encrypt(text, b)
            else:
                text = caesar_encrypt(text, a)
        if (args.affine):
            print("Affine cipher - encrypt")
            a, b = read_key("key.txt")
            text = affine_encrypt(text, int(a), int(b))
        file_write(text, "crypto.txt")
        print("Encrypted text: ", text)
        print("Encrypted text saved to crypto.txt")

    
    elif (args.decrypt):
        result = ""
        text = file_read("crypto.txt")
        if (args.caesar):
            print("Caesar cipher - decrypt")
            a,b = read_key("key.txt")
            if b != 0:
                result = caesar_decrypt(text, b)
            else:
                result = caesar_decrypt(text, a)
        if (args.affine):
            print("Affine cipher - decrypt")
            a, b = read_key("key.txt")
            result = affine_decrypt(text, a, b)
            
        file_write(result, "decrypt.txt")
        print("Decrypted text: ", result)
        print("Decrypted text saved to decrypt.txt")
        
    elif (args.k):
        result = ""
        print("Brute-force attack")
        text = file_read("crypto.txt")
        if (args.caesar):
            for i in range(1,26):
                decrypted_text = caesar_decrypt(text, i)
                print("Decrypted text: ", decrypted_text)
                result += "\nShift: " + str(i) + " // Decrypted text:" + decrypted_text
        if (args.affine):
            for i in affine_a_coprime:
                for j in range(0,26):
                    decrypted_text = affine_decrypt(text, i, j)
                    print("Decrypted text: ", decrypted_text)
                    result += "\nA: " + str(i) + " B: " + str(j) + " // Decrypted text:" + decrypted_text
        print("Decrypted text saved to decrypt.txt")
        file_write(result, "decrypt.txt")
        
    elif (args.j):
        
        if (args.caesar):
            print("Caesar cipher - known-plaintext attack")
            text = file_read("crypto.txt")
            known_text = file_read("extra.txt")
            for i in range(1,26):
                decrypted_text = caesar_decrypt(text, i)
                if known_text in decrypted_text:
                    print("Decrypted text: ", decrypted_text)
                    print("Shift: ", i)
                    file_write(str(i), "key-new.txt")
                    break
                
        if (args.affine):
            print("Affine cipher - known-plaintext attack")
            text = file_read("crypto.txt")
            known_text = file_read("extra.txt")
            for a in range(1,26):
                for b in range(1,26):
                    decrypted_text = affine_decrypt(text, a, b)
                    if known_text in decrypted_text:
                        print("Decrypted text: ", decrypted_text)
                        print("A: ", a)
                        print("B: ", b)
                        file_write(str(a) + " " + str(b), "key-new.txt")
                        break
            
            
        
    else:
        print("No arguments passed, try -h for help")
        exit()
        
        