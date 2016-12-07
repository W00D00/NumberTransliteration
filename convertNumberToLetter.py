# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 16:03:05 2016

@author: iszirtes
"""
import codecs
import pickle
from libs.numbersToLetters import NumberToLetter
from i18n.transliterationData_HU import dataTable

DEBUG = False

print("process starts...")
N2L = NumberToLetter(dataTable)
numberFrom = 1
numberTo = 1000000
numberStep = 1
numberType = 'cardinal'
usedFilenames = {}
usedNumbers = {}

print("collect transliterations...")
outFile = codecs.open(r"output\numberTransliterationResult_{}_{}.txt".format(numberFrom, numberTo), mode='w', encoding="utf-8")
for n in range(numberFrom, numberTo, numberStep):
    # debug print
    if DEBUG and n == 19001:
        print("debug point:", n)
    N2L.set_number(str(n), numberType)
    number = N2L.get_number()
    transliteration = N2L.get_transliterations(join=True)
    filenames = N2L.get_filenames()
    fileNameContents = N2L.get_fileNameContents()
    result = "number:\t{}\ttransliteration:\t{}\tfilename:\t{}\tcontent:\t{}".format(number, transliteration, filenames, fileNameContents)
    outFile.write("{}\n".format(result))
    print(result)
    for fn, fnc in zip(filenames, fileNameContents):
        storeNumber = False
        if fn not in usedFilenames:
            usedFilenames[fn] = (fnc, [number])
            if number not in usedNumbers:
                storeNumber = True
        else:
            usedFilenames[fn][1].append(number)

        if storeNumber:
            if number not in usedNumbers:
                usedNumbers[number] = [(fn, fnc) for fn, fnc in zip(filenames, fileNameContents)]
            else:
                usedNumbers[number]
outFile.close()

print("write out the pcikle file...")
pcikleFileFileName1 = r"output\numberTransliterationUsedFilenames_{}_{}.pckl".format(numberFrom, numberTo)
pcikleFile1 = open(pcikleFileFileName1, 'wb')
pickle.dump(usedFilenames, pcikleFile1)
pcikleFile1.close()

pcikleFileName2 = r"output\numberTransliterationUsedNumbers_{}_{}.pckl".format(numberFrom, numberTo)
pcikleFile2 = open(pcikleFileName2, 'wb')
pickle.dump(usedNumbers, pcikleFile2)
pcikleFile2.close()

print("verify the data of the pcikle files...")
pcikleFile1 = open(pcikleFileFileName1, 'rb')
transliteration_usedFilenames = pickle.load(pcikleFile1)
pcikleFile1.close()

pcikleFile2 = open(pcikleFileName2, 'rb')
transliteration_usedNumbers = pickle.load(pcikleFile2)
pcikleFile2.close()

usedFilenames = list(transliteration_usedFilenames.keys())
for number, l in transliteration_usedNumbers.items():
    for t in l:
        if t[0] in usedFilenames:
            usedFilenames.remove(t[0])
        assert t[0] in transliteration_usedFilenames, t[0]

assert not usedFilenames, usedFilenames

print("write out the recording files...")
outFile = codecs.open(r"output\numberTransliterationFileNameListToRecring.txt", mode='w', encoding="utf-8")
for fn, t in sorted(transliteration_usedFilenames.items()):
    # 1-c	egy	['1']
    outFile.write("{}\t{}\t{}\n".format(fn, t[0], t[1]))
outFile.close()

outFile = codecs.open(r"output\numberTransliterationNumberListToRecring.txt", mode='w', encoding="utf-8")
filenames = []
for number in sorted(transliteration_usedNumbers, key=lambda k: (len(k), k)):
    for t in transliteration_usedNumbers[number]:
        if t[0] not in filenames:
            filenames.append(t[0])
            # 1	1-c	egy
            outFile.write("{}\t{}\t{}\n".format(number, t[0], t[1]))
outFile.close()

outFile = codecs.open(r"output\numberTransliterationFileNamerListToCutting.txt", mode='w', encoding="utf-8")
for fn, t in sorted(transliteration_usedFilenames.items()):
    # 1-c	egy	['1']
    # t[1] = ['100000', '100001']
    # t[1] -ből csak az kell ami benne van transliteration_usedNumbers ebben
    s1 = set(t[1])
    s2 = set(transliteration_usedNumbers.keys())
    s3 = s1 & s2
    s4 = sorted(list(s3))
    outFile.write("{}\t{}\t{}\n".format(fn, t[0], s4))
outFile.close()

print("process ends.")
