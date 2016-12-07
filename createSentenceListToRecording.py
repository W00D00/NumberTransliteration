# -*- coding: utf-8 -*-

import codecs
import pickle
import re
import itertools


print("process starts...")

# open the pickle file and load it's content
pcikleFileName = r"output\numberTransliterationUsedNumbers_1_1000000.pckl"
pcikleFile = open(pcikleFileName, 'rb')
transliteration_usedNumbers = pickle.load(pcikleFile)
pcikleFile.close()

# collect the numbers
usedNumbers = []
for number in sorted(transliteration_usedNumbers, key=lambda k: (len(k), k)):
    if number not in usedNumbers:
        usedNumbers.append(number)

usedNumberCnt = len(usedNumbers)

# open the file which contains the sentences
inputFilePath = r"..\base_retail_sentences\\Retailbiancomondatok_v1.txt"
inputFileWithSentences = codecs.open(inputFilePath, mode='r', encoding='utf-8')

# create a collection from file line by line
inputFileLines = inputFileWithSentences.readlines()
inputFileLineCnt = len(inputFileLines)

# patterns to sentence filling
numberPattern = re.compile('<PRICE>')
unitPattern = re.compile(" *forint\w*[,.↗]")
unitReplace = "→"
sentenceConcatenatePattern = "{} || {}"

# versioning the output file
outputFileVersion = "v2"

# open a new output file
outputFileNameToOriginalOrder = r"output\Retail_sentences_in_original_order_to_recording_{}.txt".format(outputFileVersion)
outputFileToOriginalOrder = codecs.open(outputFileNameToOriginalOrder, mode="w", encoding="utf-8")

outputFileNameToSelected = r"output\Retail_sentences_selected_to_recording_{}.txt".format(outputFileVersion)
outputFileToSelected = codecs.open(outputFileNameToSelected, mode="w", encoding="utf-8")


# numbers to filling
numbersTurned = False


def get_number():
    global numbersTurned
    global usedNumberCnt
    cnt = 1
    for number in itertools.cycle(usedNumbers):
        if cnt == usedNumberCnt:
            numbersTurned = True
            cnt = 1
        cnt += 1
        yield number

# generator to numbers
numbers = get_number()

# lines from file
linesTurned = False


def get_line():
    global linesTurned
    global inputFileLineCnt
    cnt = 0
    for origLine in itertools.cycle(inputFileLines):
        if cnt == inputFileLineCnt:
            linesTurned = True
            cnt = 0
        cnt += 1
        yield cnt, origLine

lines = get_line()

# containers for output files
modifiedLinesInOriginalOrder = {}
modifiedLinesSelected = {'withNumber': [], 'withoutNumber': {}}


def store_modifiedLine(table, number, line):
    if number:
        if number not in table:
            table[number] = [line]
        else:
            table[number].append(line)
    else:
        table.append(line)

# configs
usedAllNumbers = True

# main loop through all the lines and fill all numbers into them
for lineNumber, originalLine in get_line():
    foundNumbers = numberPattern.findall(originalLine)
    if foundNumbers:
        modifiedLineWithUnit = numberPattern.sub(lambda L: '{:0,d}'.format(int(next(numbers))), originalLine)
        modifiedLineWithoutUnit = re.sub(unitPattern, unitReplace, modifiedLineWithUnit)
        modifiedLineConcatenated = sentenceConcatenatePattern.format(modifiedLineWithoutUnit.rstrip(), modifiedLineWithUnit.strip())
        store_modifiedLine(modifiedLinesInOriginalOrder, lineNumber, modifiedLineWithoutUnit)
        store_modifiedLine(modifiedLinesInOriginalOrder, lineNumber, modifiedLineWithUnit)
        store_modifiedLine(modifiedLinesSelected['withNumber'], None, modifiedLineConcatenated)
    else:
        if not linesTurned:
            store_modifiedLine(modifiedLinesInOriginalOrder, lineNumber, originalLine)
            store_modifiedLine(modifiedLinesSelected['withoutNumber'], lineNumber, originalLine)
    if linesTurned and not usedAllNumbers or linesTurned and numbersTurned:
        break


# write out the original order version
for number, lines in sorted(modifiedLinesInOriginalOrder.items()):
    for line in lines:
        outputFileToOriginalOrder.write(line)

# write out selected version
lineIdx = 1
for number, lines in sorted(modifiedLinesSelected['withoutNumber'].items()):
    for line in lines:
        outputFileToSelected.write(line)
outputFileToSelected.write("Termékek, árak:\r\n\r\n")
for line in modifiedLinesSelected['withNumber']:
    outputFileToSelected.write("{}.\t{}\r\n\r\n".format(lineIdx, line))
    lineIdx += 1

# close the output file
outputFileToOriginalOrder.close()
outputFileToSelected.close()

print("process ends.")
