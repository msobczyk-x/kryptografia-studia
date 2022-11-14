#Szyfr Cezara i afiniczny - szyfruj i deszyfruj
#Autor: Maciej Sobczyk
#python 3.10
import sys
import argparse

parser = argparse.ArgumentParser(description='Szyfr Cezara i afiniczny - szyfruj i deszyfruj', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-c', '--cezar', action='store_true', help='szyfruj Cezara')
parser.add_argument('-a', '--afiniczny', action='store_true', help='szyfruj afiniczny')

def caesar_encrypt(text):
    for i in text:
            


def file_read(plik):
    file = open(plik, "r")
    text = file.read()
    file.close()
    return text

def file_write(text, file):
    file = open(file, "w")
    file.write(text)
    file.close()
    
def read_key(fileName):
    key = file_read(fileName)
    a, b = key.split()
    return a,b



if __name__ == "__main__":
    