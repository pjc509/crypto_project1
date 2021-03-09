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
import time

#constants
IN_LENGTH = 500
KEY_LENGTH = 25
UPPER = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = " abcdefghijklmnopqrstuvwxyz"


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
    kps = load_dict(fname)
    #print(test1_text)

    kp1 = kps[1]
    kp2 = kps[2]
    kp3 = kps[3]
    kp4 = kps[4]
    kp5 = kps[5]


    #Load words from dictionary2 for test2
    fname = "word_dictionary_test2.txt"
    dict2_text = load_dict(fname)
    dictionary = load_dict(fname)
    #print(test2_text)

    #Pick type of cipher text to generate
    print("Generate Plain text based on Test1 or Test2")
    t_type = int(input("1-Test1, 2-Test2: "))
    if t_type<1: t=1
    if t_type>2: t=1

    #Enter Plain Text to encrypt
    u_txt =1
    if t_type == 1:
        u_txt = int(input("Enter Test Text 1 to encrypt (1-5): "))
        if u_txt<1: u_txt=1
        if u_txt>5: u_txt=5

    #Enter length of key
    t = int(input("Enter length of key(4-20): "))
    if t<4: t=4
    if t>20: t=20

    #Enter type of scheduling alorithm
    print("Type of scheduling alorithm(only 1 works)")
    t_algo = int(input("1-random, 2-test1, 3-test2, 4-with random: "))
    if t_algo<1: t=1
    if t_algo>4: t=4

    #Generate key based on test1 scheduling alogitm
    key = generate_random_key_test1(t,t_algo);
    #key = generate_key(t,t_algo)

    #Encrypt selected Plain Text
    myKey = key
    myMessage= test1_text[u_txt]
    if t_type == 1:
        myMessage= test1_text[u_txt]
    if t_type ==2:
        test2_text = generate_text2(dict2_text)
        myMessage = test2_text
    translated = encryptMessage(myKey, myMessage)
    print("Plain Text:")
    print(myMessage)
    print()
    #print("Cipher Text:")
    #print(translated)
    #print()
    print("Start Decrypt efforts: ")
    print()

    #Joel -  add main logic
    #Here's our driver code
    kp = myMessage

    confidence = 0
    #x = str(input("Insert key: "))
    #ret = encrypt(kp.upper(), x.upper())
    ret = encrypt(kp.upper(), myKey.upper())

    #start timer
    t_start = time.time()

    #print ("returned ciphertext is: \n" + ret)
    prob_KP = iterateKPs(ret.upper(), confidence, kps)
    answer = ""
    if prob_KP[0] == 0:
        answer = kp1
    if prob_KP[0] == 1:
        answer = kp2
    if prob_KP[0] == 2:
        answer = kp3
    if prob_KP[0] == 3:
        answer = kp4
    if prob_KP[0] == 4:
        answer = kp5

    confidence = prob_KP[1]


    #Start looking at the dictionary/begin case 2 analysis. Right now it has a few large words. I think a better approach may be to pick words with as many different chars as possible
    bigwords = ["intuitiveness", "faultlessly", "hermeneutics", "unconvertible", "photocompose"]

    minWordKeys = []
    for word in bigwords:
        minWordKeys.append(findPossibileWords(word.upper(), ret.upper()))

    keyGuess = getCommonality(minWordKeys)

    decryption = forceDict(ret, keyGuess, dictionary)

    #we should test to set these at accurate measures. these are just guesses.
    #if the confidence is higher than 5, we have likely found a known plaintext. We can also return that answer and break before processing the case 2 stuff.  
    if confidence > 5:
        print("Probable known plaintext is case " + str(prob_KP[0]+1) + ". The confidence level is " + str(prob_KP[1]))
        print("That plaintext is: " + answer)

    elif decryption[1] > 40:
        print("We are guessing this is a case two text, and our decryption guess is: \n")
        print(decryption[0])
    elif (decryption[1] < 25 and confidence > 2 ):
        print("We aren't really sure on this one, we are guessing a known plaintext, " + str(prob_KP[0]+1))
        print(answer)
    else:
        print("You won this round, we don't know. In an attempt to salvage some credit, here are our guesses:")
        print("maybe known plaintext " + str(prob_KP[0]+1) + "or a case two text decrypted as follows: ")
        print(decryption[0])


    t_end = time.time()
    print('time: ')
    print(t_end - t_start)

    #print("NO MATCH")

#This function can be used to encrypt a plain-text with a random non-repeating key based on an input key
def encrypt(string, key):
    index_done = []
    index_cipher = []
    string_ciphered = ""
    i = 0

    print("Your key is " + key + " of length " + str(len(key)))

    # generate a randon keystream based on shifts from the given key and save into an array (index_cipher)
    while len(index_cipher) < len(string):
        key_index = key[random.randint(0, len(key)-1)]
        #print("Key index " + str(key_index))

        rand_fromKey = UPPER.find(key_index)
        #print("rand_fromKey: " + str(rand_fromKey))
        index_cipher.append(rand_fromKey)

    #print("The keystream, based on \'" + key + "\' is: \n")
    #print(index_cipher)
    
    # turn the input string into an array of numerical values. Using all caps ("UPPER") 
    while i < len(string):
        index = UPPER.find(string[i])
        index_done.append((index + index_cipher[i]) % len(UPPER))
        i=i+1
    
    for character in index_done:
        string_ciphered+=UPPER[character]

    return string_ciphered

#given a known plaintext and a ciphered string, find the key for 'length' chars
def forceKey(kp, c_string, length):
    index_kp = []
    index_c = []
    index_key = []

    if length > len(kp) or length > len(c_string):
        print("breaking, text is smaller than key length")
    else:
        i = 0
        while i  < length:
            index_kp.append(UPPER.find(kp[i]))
            index_c.append(UPPER.find(c_string[i]))
            index_key.append((((26 + index_c[i]) - index_kp[i]) % 27) + 1)
            i+=1
    #print("cipher text was " + c_string + " looking for " + kp + ". Returning:")
    #print(index_key)
    return index_key

#Checks all plaintexts to look for something that resembles a key. return the index of the KP and update the confidence value to the delta between the index sizes.
def iterateKPs(c_string, confidence, kps):
    kp1 = kps[1]
    kp2 = kps[2]
    kp3 = kps[3]
    kp4 = kps[4]
    kp5 = kps[5]
    list = [kp1, kp2, kp3, kp4, kp5]
    counts =[]

    #go through each known plaintext and get the first part of the key (3x the max key length, assuming that plaintext
    for item in list:
        result_key = forceKey(item.upper(), c_string.upper(), KEY_LENGTH*3)
        values = []
        counter = 0
        #count the number of unique values in the resulting key.  If the count is > the keylength, we know it cannot be the key
        #(but for the random values).  For the test code, I don't use this though.
        for value in result_key:
            if value not in values:
                counter+=1
                values.append(value)
        counts.append(counter)
    

    #Find the comparative index lengths to determine confidence.  A large gap indicates higher confidence.
    counts_copy = counts
    m1 = sorted(counts_copy)[0]
    m2 = sorted(counts_copy)[1]
    confidence = int(m2)-int(m1)
    #The ciphertext is most likely from the plaintext where the key has the least entropy. e.g. if the key is "MARY", each shift can only be by one of 4 values.  
    #The minimum count finds this reliably until the key is the length of the alphabet.  At that point we would need to add some features. 
    return counts.index(min(counts)), confidence

#find the minimum number of characters needed to create a key for the word.  Return that value and the key.
def findPossibileWords(word, ciphertext):
    keyspace = 99
    keySequence = []
    cipher_copy = ciphertext

    while len(cipher_copy) >= len(word):
        key_index = forceKey(word, cipher_copy, len(word))
        if len(set((key_index))) < keyspace:
            keyspace = len(set(key_index))
            keySequence = key_index
        cipher_copy = cipher_copy[1:]
        #print(cipher_copy)
        #print("keyspace: " + str(keyspace))

    return keySequence, keyspace

# we can fine tune this, but I assume that for 500 chars over 40 words in the dictionary, we will have at least 3/5 of the words I picked. (**I haven't mathed this**)
def getCommonality(word_index_info):
    threeIndex = []
    jointIndex = []
    ordered = []
    #right now I am just taking the three words with the smallest keyspace. alternatively we could look for overlap.
    for item in word_index_info:
        ordered.append(item[1])
    ordered.sort()
    
    i = 0
    while i < 3:
        for item in word_index_info:
            if item[1] == ordered[i]:
                threeIndex.append(item[0])
        i+=1

    jointIndex = threeIndex[0] + threeIndex[1] + threeIndex[2]
    jointIndex = list(set(jointIndex))

    print("my key guess is ")
    print(jointIndex)
    return jointIndex

def forceDict(cipher_text, key_guess, dictionary):
    found_counter = 0
    i = 0
    decrypted = ""
    while i < len(cipher_text):
        flow_control = 0
        for word in dictionary:
            if testWord(word, cipher_text[i:(i+len(word)+1)], key_guess): 
                decrypted+=(word + " ")
                found_counter += 1
                i+=(len(word)+1)
                flow_control = 1
        if flow_control == 0:
            decrypted+=cipher_text[i]
            i+=1

    return decrypted, found_counter

#This does a character by character analyis to see if the word can be formed from the probable key
def testWord(word, cipher_text, key_guess):
    validity_array = []
    i = 0
    word=word.upper()+" "
    if len(word) > len(cipher_text):
       #word=word[0:len(cipher_text)] #this doesn't appear to be working, instead we will just give up on partial words for now
       return False
    while i < (len(word)-1):
        reqValue = ((UPPER.find(cipher_text[i]) - UPPER.find(word[i])) % 27) 
        #print("cipher " + cipher_text[i]+ "and the word character " + word[i] + " looking for " + str(reqValue))
        #the best case is that the chars line up directly with a possible key value (no random injected characters. If they line up, add a 1 to the array.
        if reqValue in key_guess:
            validity_array.append(1)
        #This is a test case for dealing with randomness. Right now it doesn't work, as it lets way too many words in.
        #elif (i+1 < len(word)) and (((UPPER.find(cipher_text[i+1]) - UPPER.find(word[i])) % 27) in key_guess):
        #    validity_array.append(1)
        else:
            validity_array.append(0)
        i+=1
    
    #We can look at how many valid chars we have and how many invalid chars we have. Not clear to me what the right number is here.
    if (len(word) - sum(validity_array)) > 1:
        return False
    else:
        return True




#pjc - reminder is mine code

def principal_period(s):
    i = (s+s).find(s, 1, -1)
    if i > 0: print("match")
    return None if i == -1 else s[:i]

def repetitions(s):
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))


def repeats(string):
    for x in range(1, len(string)):
        substring = string[:x]

        if substring * (len(string)//len(substring))+(substring[:len(string)%len(substring)]) == string:
            print("match")
            print(substring)
            return substring

    print("no match")
    return None

def run_test2(translated, dict2_words):
    #look at first 19 char of cipher text
    trial_text2 = translated[:19]
    #build array of possible plain text - first iteration of 40
    key_array_ct = 0
    t2space = " "
    length = len(dict2_words)
    for i in range(length):
    #for i in (2,40):
        test_txt = dict2_words[1] + t2space
        test_txt += dict2_words[i]
        if len(test_txt) < 20:
            test_txt += t2space
            if i < 39:
                test_txt += dict2_words[i+1]
            else:
                test_txt += dict2_words[1]
        test_txt = test_txt[:19]
        print(i)
        print(test_txt)
        calc_key = decryptMessage(test_txt, trial_text2)
        #first test - determine if exact key match
        match_key = principal_period(calc_key)
        #match_key2 = principal_period(calc_key[:18])
        print(calc_key)
        #matches = repetitions(calc_key)
        #freq_key = findRepeatSequencesSpacings(calc_key)
        #print(freq_key)
        freq_key2 = kasiskiExamination(calc_key)
        print(freq_key2)
        match_likely = 0
        length2 = len(freq_key2)
        if length2 > key_array_ct:
            if key_array_ct != 0:
                print("likely key")
                match_likely = 1
            key_array_ct = length2
        key2_size = 0
        for ii in range(length2):
            if freq_key2[ii] > key2_size:
                key2_size = freq_key2[ii]
        if key2_size > 9: print("likely not correct key")
        match_key2 = repeats(calc_key)
        key2_size2 = len(calc_key)
        if match_key2 != None:
            bb = len(match_key2)
            if match_likely == 0:
                if bb < key2_size or bb == key2_size2:
                    match_key2 = None
        if match_key != None:
            print("MATCH")
            plain_text = decryptMessage(match_key, translated)
            print("match_key:")
            print(match_key)
            return plain_text
        if match_key2 != None:
            print("MATCH")
            plain_text = decryptMessage(match_key2, translated)
            print("match_key:")
            print(match_key2)
            return plain_text
    return 0

def run_test1(test1_text, translated):
    length = len(test1_text)
    for i in range(length):
        calc_key = decryptMessage(test1_text[i], translated)
        match_key = principal_period(calc_key)
        if match_key != None:
            #print("MATCH")
            print("match to Plain Text:")
            print(i)
            print("match_key:")
            print(match_key)
            #print("matching plain text:")
            #print(test1_text[i])
            #t_end = time.time()
            #print('time: ')
            #print(t_end - t_start)
            return test1_text[i]
    return 0

def generate_text2(dict2_words):
    #fname = "word_dictionary_test2.txt"
    #dict2_words = load_dict(fname)
    #print("Dictionary 2 words:")
    #print(dict2_words)

    #pick words randomly
    #test2_text = ['word'] * 40
    #print(test2_text)
    text_ran = np.random.randint(low=1, high=40, size=(60,))
    #print(text_ran)

    t2space = " "
    #test2_text = ""
    test2_text = dict2_words[1] + t2space
    word_ct = 0
    for i in text_ran:
        #print(i)
        text_len = len(test2_text)
        if text_len < 500:
            #fix first 1 word for testing - to limit looping
            if i == 0:
                test2_text += dict2_words[1]
            else:
                test2_text += dict2_words[i]
            test2_text += t2space
            word_ct += 1

    text_len = len(test2_text)
    test2_text = test2_text[:500]
    #print(text_len)
    #print(word_ct)
    #print(test2_text)
    #print()
    return test2_text;

def generate_random_key_test1(t,t_type):
    #default random key
    letters=string.ascii_lowercase
    key = ''.join(random.choice(LETTERS) for i in range(t));

    #random key
    if t_type == 1:
        letters=string.ascii_lowercase
        key = ''.join(random.choice(LETTERS) for i in range(t));

    if t_type == 2:
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
