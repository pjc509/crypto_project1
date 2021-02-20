# Vigenere Cipher (Polyalphabetic Substitution Cipher)
# https://www.nostarch.com/crackingcodes (BSD Licensed)
# pjc - 2/20 - modified to generate sample encryption text for project 1

#import pyperclip

import random, sys, fileinput
import numpy as np

#LETTERS = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS = ' abcdefghijklmnopqrstuvwxyz'

def main():
    # This text can be copy/pasted from https://invpy.com/vigenereCipher.py:

    #TEST 1 - CREATE CIPHER TEXT for 5 PLAIN TEXT in FILE1
    #pjc - load 5 plaintext for test1
    fname = "plaintext_dictionary_test1.txt"
    test1_text = load_dict(fname)

    #pjc - set key for now, build logic to generate key to match
    #      proposed scheduling alorithm
    myKey = 'abcdefghij'

    #pjc - create sample cipher text for each plaintext
    myMode = 'encrypt' # Set to either 'encrypt' or 'decrypt'.

    #pjc - add logic to encryp each test1 plaintext
    #      need to add logic to strip out extra values

    print('Key:')
    print(myKey)
    print('Mode:')
    print(myMode)

    print("***** TEST 1 *****")
    #pjc - loop through each plaintext from file1
    ccount = 0
    for i in test1_text:
         ccount = ccount + 1
         if ccount == 3:
             ccount = 1
             myMessage = i
             if myMode == 'encrypt':
                 translated = encryptMessage(myKey, myMessage)
             elif myMode == 'decrypt':
                 translated = decryptMessage(myKey, myMessage)
             print('Original message:')
             print(myMessage)
             print('%sed message:' % (myMode.title()))
             print(translated)
             print()

    #TEST 2 - GENERATE CIPHER TEXT for L=500 and v=40
    fname = "word_dictionary_test2.txt"
    dict2_words = load_dict(fname)
    #print("Dictionary 2 words:")
    #print(dict2_words)

    #pick 40 words randomly
    #test2_text = ['word'] * 40
    #print(test2_text)
    text_ran = np.random.randint(low=1, high=40, size=(40,))
    print(text_ran)

    test2_text = ""
    t2space = " "
    for i in text_ran:
        #print(i)
        test2_text += dict2_words[i]
        test2_text += t2space

    #print(test2_text)
    print()
    print("***** TEST 2 *****")
    myMessage = test2_text
    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('Test 2 Plaintext message:')
    print(myMessage)
    print()
    print('%sed message:' % (myMode.title()))
    print(translated)
    print()






#This function loads the 2 dictionary files
def load_dict(fname):
    #fname1 = "plaintext_dictionary_test1.txt"
    #fname2 = "word_dictionary_test2.txt"
    dict1_array = []
    #dict2_array = []
    with open(fname) as f:
        for line in f:
            if line != "\n":
                #dict1_array.append(line)
                dict1_array.append(line.rstrip('\n'))
        #print(dict1_array)
    return dict1_array

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

            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)

    return ''.join(translated)


# If vigenereCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
