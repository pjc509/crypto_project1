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
import itertools, re

LETTERS = ' abcdefghijklmnopqrstuvwxyz'
NONLETTERS_PATTERN = re.compile('[^A-Z]')
NUM_MOST_FREQ_LETTERS = 4 # Attempt this many letters per subkey.
MAX_KEY_LENGTH = 20 # Will not attempt keys longer than this.

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

    #test repeat sequence in calculated key
    calc_key = decryptMessage(test1_text[u_txt], translated)
    print("Decrypted key:")
    print(calc_key)
    print("key:")
    print(key)
    zzz = principal_period(calc_key)
    print("match_key:")
    print(zzz)

def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i]

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

def findRepeatSequencesSpacings(message):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message:
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message:
    seqSpacings = {} # Keys are sequences, values are lists of int spacings.
    for seqLen in range(4, 20):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq:
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message:
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # Initialize a blank list.

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence:
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings

def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the ciphertext. repeatedSeqSpacings has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    # (See getMostCommonFactors() for a description of seqFactors.)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # (See getMostCommonFactors() for a description of factorsByCount.)
    factorsByCount = getMostCommonFactors(seqFactors)

    # Now we extract the factor counts from factorsByCount and
    # put them in allLikelyKeyLengths so that they are easier to
    # use later:
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths

def getUsefulFactors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1 and not 1. For example,
    # getUsefulFactors(144) returns [2, 3, 4, 6, 8, 9, 12, 16]

    if num < 2:
        return [] # Numbers less than 2 have no useful factors.

    factors = [] # The list of factors found.

    # When finding factors, you only need to check the integers up to
    # MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1): # Don't test 1: it's not useful.
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # Remove duplicate factors.

def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors:
    factorCounts = {} # Key is a factor, value is how often it occurs.

    # seqFactors keys are sequences, values are lists of factors of the
    # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them:
    factorsByCount = []
    for factor in factorCounts:
        # Exclude factors larger than MAX_KEY_LENGTH:
        if factor <= MAX_KEY_LENGTH:
            # factorsByCount is a list of tuples: (factor, factorCount)
            # factorsByCount has a value like: [(3, 497), (2, 487), ...]
            factorsByCount.append( (factor, factorCounts[factor]) )

    # Sort the list by the factor count:
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount

def getItemAtIndexOne(items):
    return items[1]



# the main() function.
if __name__ == '__main__':
    main()
