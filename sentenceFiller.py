# -*- coding: utf-8 -*-

import sys
import csv
import codecs
import re
import os

# DEBUGPRINT = sys.argv[2]
DEBUGPRINT = True


def debugPrint(*arg):
    if DEBUGPRINT:
        print(*arg)


def csvOpener(csvFilePath):
    file = codecs.open(csvFilePath, 'r', encoding='utf-8-sig')
    obj = csv.reader(file)
    debugPrint('The "{}" file is opened.'.format(csvFilePath))
    return file, obj


def newFile():
    f = codecs.open(os.path.join(os.path.dirname(sys.argv[0]), 'output\sentenceCollection.txt'), 'w', encoding='utf-8')
    return f


def cFormat(sentencePattern, *data):
    return sentencePattern % data


def namedFormat(sentencePattern, *data):
    cnt = 0
    while sentencePattern.find("<") > -1:
        placeHolders = re.findall("<[^>]+>", sentencePattern)
        sentencePattern = sentencePattern.replace(placeHolders[0], data[cnt])
        cnt += 1
    return sentencePattern


csvFile, csvFileObj = csvOpener(sys.argv[1])

outputFile = newFile()


sentencePattern = None
placeHolderType = None

for row in csvFileObj:
    debugPrint(len(row), row)
    if row[0] != "" and row[1] == "":
        sentencePattern = row[0]
        if re.search("<[^>]+>", sentencePattern):
            placeHolderType = "named"
            continue
        elif re.search("%s", sentencePattern):
            placeHolderType = "cformat"
            continue
        else:
            placeHolderType = "no"

    if row[0] == "":
        sentencePattern = None
        placeHolderType = None
        continue

    if placeHolderType == "named":
        sentence = namedFormat(sentencePattern, *row)
    elif placeHolderType == "cformat":
        sentence = cFormat(sentencePattern, *row)
    elif placeHolderType == "no":
        sentence = sentencePattern

    debugPrint(sentence)
    outputFile.write('{}\n'.format(sentence))

outputFile.close()
