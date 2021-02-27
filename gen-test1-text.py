#
# Project 1 - generate cipher text for Test 1
#
import random
import os
import json
import random
from random import randrange
import string
import numpy as np

LETTERS = ' abcdefghijklmnopqrstuvwxyz'
letter_key_values = {" ":0,"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,
"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26}
letter_key = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
L = 500;


def main():

    #Load 5 plaintext from dictionary1 for test1
    fname = "plaintext_dictionary_test1.txt"
    test1_text = load_dict(fname)
    #print(test1_text)

    #Enter length of key
    t = int(input("Enter length of key: "))
    if t<4: t=4
    if t>20: t=20

    #Enter Plain Text to encrypt
    u_txt = int(input("Enter Test Text 1 to encrypt (1-5): "))
    if u_txt<1: t=1
    if u_txt>5: t=5

    #Generate key based on test1 scheduling alogitm
    key = generate_random_key_test1(t);

    #Encrypt selected Plain Text
    myKey = key
    myMessage= test1_text[u_txt]
    translated = encryptMessage(myKey, myMessage)

    print("RESULTS:")
    print("Plain Text")
    print(u_txt)
    print(test1_text[u_txt])
    print()
    print("Cipher Text:")
    print(translated)
    print()


def generate_random_key_test1(t):
    #default random key
    letters=string.ascii_lowercase
    key = ''.join(random.choice(LETTERS) for i in range(t));
    #compute key
    #scheduling algorithm will compute “j(i) = (i mod t) + 1”
    #the key k can be written as k[1],...,k[t],
    #    where each k[j] is in {0,..,26}, for j=1,..,t
    key2 = ""
    for i in range(t):
        #print(i)
        j = (i % t) + 1
        #print(j)
        #num = letter_key.find(j)
        #num = letter_key.find(key[j])
        #print(num)
    print("Key:")
    print(key)
    return key;


def load_dict(fname):
    #fname1 = "plaintext_dictionary_test1.txt"
    #fname2 = "word_dictionary_test2.txt"
    dict1_array = []
    with open(fname) as f:
        for line in f:
            if line != "\n":
                if line[:19] != "Candidate plaintext":
                #dict1_array.append(line)
                    dict1_array.append(line.rstrip('\n'))
                    #print(line.rstrip('\n'))
        #print(dict1_array)
    return dict1_array


# Next 3 modules used from:
# https://www.nostarch.com/crackingcodes (BSD Licensed)
def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')

def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')

def translateMessage(key, message, mode):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.lower()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.lower())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS.
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # Add if encrypting.
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # Subtract if decrypting.

            num %= len(LETTERS) # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            else:
                #pjc - added else logic for spaces
                translated.append(LETTERS[num].lower())


            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)

    return ''.join(translated)




# the main() function.
if __name__ == '__main__':
    main()
