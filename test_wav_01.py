# -*- coding: utf-8 -*-

import winsound


inputFilePath1 = r"c:\Users\iszirtes\Google Drive\AutomatizálHang\recording_zsuzsa_20160928\cut_numbers\1x-t.wav"
inputFilePath2 = r"c:\Users\iszirtes\Google Drive\AutomatizálHang\Zsuzsa_Recording_20160928\cut_numbers\x1g1-c.wav"
outputFilePath = r"c:\Users\iszirtes\Google Drive\AutomatizálHang\Zsuzsa_Recording_20160928\cut_numbers\audioFinal.wav"

outputfile = open(outputFilePath, 'wb')

audio1 = open(inputFilePath1, 'rb').read()
outputfile.write(audio1)

audio2 = open(inputFilePath2, 'rb').read()
outputfile.write(audio2)

outputfile.close()

winsound.PlaySound(outputFilePath, winsound.SND_FILENAME)
