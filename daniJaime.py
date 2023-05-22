#!/usr/bin/python
import sys
import numpy as np

SPANISH_FREQ = [0.1177, 0.0222, 0.0400, 0.0551, 0.1255, 0.0069, 0.0187, 0.0070, 0.0625, 0.0049, 0.0001, 0.0497, 0.0315, 0.0671, 0.0463, 0.0610, 0.0276, 0.0070, 0.0687, 0.0798, 0.0463, 0.0393, 0.0090, 0.0001, 0.0022, 0.0090, 0.0052]
ENGLISH_FREQ = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.02, 0.061, 0.07, 0.002, 0.008, 0.04, 0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 0.063, 0.091, 0.028, 0.01, 0.023, 0.001, 0.02, 0.001] 
FRENCH_FREQ = [0.087, 0.0093, 0.0315, 0.0355, 0.1783, 0.0096, 0.0097, 0.0108, 0.0697, 0.0071, 0.0016, 0.0568, 0.0323, 0.0642, 0.0535, 0.0303, 0.0089, 0.0643, 0.0791, 0.0711, 0.0614, 0.0183, 0.0004, 0.0042, 0.0019, 0.0021]

SPANISH_ALPH = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

ENGLISH_ALPH = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

FRENCH_ALPH  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


# def guessKeyLength(ciphertext):
#     textSize = len(ciphertext)
#     coincidences = []
#     for i in range(1, 15):
#         count = 0
#         for j in range(textSize-i):
#             if ciphertext[j] == ciphertext[i+j]:
#                 count += 1
#         coincidences.append(count)
    
#     kl = coincidences.index(max(coincidences)) + 1
#     print(coincidences)
#     return kl

# def decrypt(cryptText, key, alph):
#     decryptedText = ""
#     cryptText = cryptText.lower()
#     key = key.lower()
#     keyLength = len(key)
#     for i, char in enumerate(cryptText):
#         if char.isalpha():
#             charIndex = key[i % keyLength]
#             pos = alph.index(charIndex)
#             decryptedChar = alph[(alph.index(char) - pos) % len(alph)]
#             decryptedText += decryptedChar
#         else:
#             decryptedText += char
#     return decryptedText.upper()

# def encrypt(plainText, key, alph):
#     encryptedText = ""
#     plainText = plainText.lower()
#     key = key.lower()
#     keyLength = len(key)
#     for i, char in enumerate(plainText):
#         if char.isalpha():
#             charIndex = key[i % keyLength]
#             pos = alph.index(charIndex)
#             encryptedChar = alph[(alph.index(char) + pos) % len(alph)]
#             encryptedText += encryptedChar
#         else:
#             encryptedText += char
#     return encryptedText.upper()


# def checkHash(plainText, refText):
#     # Calcular el hash SHA-256 del texto plano
#     plainTextHash = hashlib.sha256(plainText.encode()).hexdigest()
#     refHash = hashlib.sha256(refText.encode()).hexdigest()
#     # Comparar el hash calculado con el hash dado
#     if plainTextHash == refHash:
#         print("True")
#         return True
#     else:
#         return False


def guessKeyLength(ciphertext, alph):
    textSize = len(ciphertext)
    coincidences = []
    for kl in range(1, 16):
        sum_ic = 0
        for i in range(kl):
            freqs = getColFreqs(ciphertext, kl, i, alph)
            ic = np.sum(freqs * (freqs - 1)) / (textSize * (textSize - 1))
            sum_ic += ic
        avg_ic = sum_ic / kl
        coincidences.append(avg_ic)

    # print(coincidences)
    kl = coincidences.index(max(coincidences)) + 1
    return kl

def getColFreqs(ciphertext, kl, i, alph):
    #get char freq
    colSize = int(np.ceil(len(ciphertext) / kl))
    ciphertext = ciphertext.lower()


    freqs = np.zeros(len(alph))
    realColSize = colSize
    for j in range(colSize):
        try:
            letter = ciphertext[j*kl+i]
            pos = ord(letter) - ord('a')
            if (len(alph) == 27):
                if (pos >= 14):
                    pos +=1
                if (letter == "ñ"):
                    pos = 14
            freqs[pos] += 1
        except:
            #fuera de rango de colSize
            realColSize -= 1
    for j in range(len(freqs)):
        #print(freqs[j], realColSize)
        freqs[j] = freqs[j] / realColSize
    
    #print(freqs)
    return freqs

def getColChar(freqs, alph):
    #guess key chars
    alphLen = len(alph)
    results = np.zeros(alphLen)

    for des in range(alphLen):
        res = 0
        for i in range(alphLen):
            pos = (i+des) % alphLen
            res = res + (freqs[pos] * alph[i])
        results[des] = res
    
    #print(results)
    colChar = np.argmax(results)
    return colChar

def guessKey(ciphertext, kl, alph, alphLetters):

    key = []
    for i in range(kl):
        colFreqs = getColFreqs(ciphertext, kl, i, alph)
        key.append(alphLetters[getColChar(colFreqs, alph)])

    key = "".join(key)
    for i in range(kl):
        uniqueKey = key[:(i+1)]
        reps = key.count(uniqueKey)
        if (reps * len(uniqueKey) == kl):
            break

    return uniqueKey
    
def detectLanguage(ciphertext):
    ciphertext = ciphertext.lower()
    lang_freqs = [
        (SPANISH_ALPH, SPANISH_FREQ),
        (ENGLISH_ALPH, ENGLISH_FREQ),
        (FRENCH_ALPH, FRENCH_FREQ)
    ]
    lang_scores = []

    if "ñ" in ciphertext:
        langIndex = 0
    else:
        for lang, lang_alph_freq in lang_freqs:
            score = 0
            for i, char in enumerate(ciphertext):
                pos = ord(char) - ord('a')
                if (len(lang_alph_freq) == 27):
                    if (pos >= 14):
                        pos += 1
            score += abs(lang_alph_freq[pos] - (1 / len(ciphertext)))
            lang_scores.append(score)
        langIndex = np.argmax(lang_scores)
    
    langAlph, langFreq = lang_freqs[langIndex]
    return langFreq, langAlph


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Error on command arguments, not enough given")
    else:
    
        file = open(sys.argv[2], "r", encoding="UTF-8")
        inputText = file.read()


        langFreq, langAlph = detectLanguage(inputText)
        
        kl = guessKeyLength(inputText, langFreq)
        
        key = guessKey(inputText, kl, langFreq, langAlph)
        print(key)


