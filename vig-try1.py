# Vigenere Cipher (Polyalphabetic Substitution Cipher)
# https://www.nostarch.com/crackingcodes (BSD Licensed)
# pjc - 2/20 - modified to generate sample encryption text for project 1

#import pyperclip

import random, sys, fileinput


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    # This text can be copy/pasted from https://invpy.com/vigenereCipher.py:

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

    #pjc - loop through each plaintext from file1
    for i in test1_text:
         #print(i)
         myMessage = i

         if myMode == 'encrypt':
             translated = encryptMessage(myKey, myMessage)
         elif myMode == 'decrypt':
             translated = decryptMessage(myKey, myMessage)

         print('Original message:')
         print(myMessage)
         print('%sed message:' % (myMode.title()))
         print(translated)
         #pyperclip.copy(translated)
         print()
         #print('The message has been copied to the clipboard.')

#This function loads the 2 dictionary files
def load_dict(fname):
    fname1 = "plaintext_dictionary_test1.txt"
    fname2 = "word_dictionary_test2.txt"
    dict1_array = []
    dict2_array = []
    with open(fname1) as f:
        for line in f:
            if line != "\n":
                #dict1_array.append(line)
                dict1_array.append(line.rstrip('\n'))
        #print(dict1_array)
    with open(fname2) as f:
        for line in f:
            #dict2_array.append(line)
            dict2_array.append(line.rstrip('\n'))
        #print(dict2_array)
    return dict1_array

def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
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
