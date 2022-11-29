# Szyfr XOR
# Autor: Maciej Sobczyk
# python 3.10

import argparse
from itertools import zip_longest

parser = argparse.ArgumentParser(
    description="Xor encryption", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    "-e", "--encrypt", action="store_true", help="encrypt file (pass a plain text file)"
)

parser.add_argument(
    "-p", "--prepare", action="store_true", help="prepare orig.txt", default=False
)

parser.add_argument("-k", action="store_true", help="brute-force attack", default=False)

# xor cipher

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


# Prepare text to encrypt
def prepare_text(text):
    preparedtext = ""
    final = ""

    # delete enter or tab and change to lower case
    for i in text:
        if i.isalpha() or i == " ":
            if i.isupper():
                preparedtext += i.lower()
            else:
                preparedtext += i
            # change text to 64 char in line
    #add end of line to the end of text
    for i in range(len(preparedtext)):
        prepare_text = preparedtext[i]
        if i != 0:
            if i % 64 == 0:
                prepare_text = "\n" + preparedtext[i]
        final += prepare_text
    # if dont have 64 char in line add space
    if final[-65] == "\n":
        return final
    else:
        while final[-65] != "\n":
            final += " "
    return final

# Read key from file
def read_key():
    key = file_read("key.txt")
    return key.split("\n")[0]

# Encrypt text with key
def encrypt_xor(text, key):
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted

# Decrypt text with key
def decrypt_xor(text, key):
    decrypted = ""
    for i in range(len(text)):
        decrypted += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return decrypted

# Assign score to letters with most frequent letters in english
def score_assign(output_string):
    string_score = 0
    #https://en.wikipedia.org/wiki/Etaoin_shrdlu
    freq = [" ", "e", "t", "a", "o", "i", "n", "s", "h", "r", "d", "l", "u"]
    for letter in output_string:
        if letter in freq:
            string_score += 1
    return string_score

# Check all possible keys and find the best one
def check_possible_keys(encoded_array):
    last_score = 0
    greatest_score = 0
    # Xor strings with all possible keys and determine score 
    for n in range(128):  # 128 ASCII characters
        xord_str = [byte ^ n for byte in encoded_array]
        xord_ascii = ("").join([chr(b) for b in xord_str])
        last_score = score_assign(xord_ascii)
        if last_score > greatest_score:
            greatest_score = last_score
            key = n
    return key

# Find key 
# Make an array of encrypted text
# Check all possible keys for every char in array and picking best one
def find_key(text):
    key_length = 64
    key_blocks = []
    key = []
    # Divide text into 64 char blocks
    for i in range(0, len(text), key_length):
        key_blocks.append(text[i : i + key_length])
    
    # Transpose blocks
    single_encrypted_blocks = [list(filter(None, i)) for i in zip_longest(*key_blocks)]
    for block in single_encrypted_blocks:
        key_n = check_possible_keys(block)
        key.append(key_n)
    str_key = "".join([chr(c) for c in key])
    return str_key

# Main
if __name__ == "__main__":
    args = parser.parse_args()

    if args.prepare:
        orig = file_read("orig.txt")
        file_write(prepare_text(orig), "plain.txt")
        print("Prepared successfully !")

    elif args.encrypt:
        plain = file_read("plain.txt")
        key = read_key()
        encrypted = encrypt_xor(plain, key)
        with open("crypto.txt", "wb") as f:
            f.write(encrypted.encode())
        print("Encrypted successfully !")

    elif args.k:
        print("Cryptanalysis started...")
        with open("crypto.txt", "rb") as f:
            crypto = f.read()
        key = find_key(crypto)
        file_write(decrypt_xor(crypto.decode(), key), "decrypt.txt")
        print("Key: ", key)
        print("Decrypted successfully !")

    else:
        print("No arguments passed, try -h for help")
        exit()
