# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 22:21:26 2016

@author: iszirtes
"""

from docx import Document

inputDocPath = r'..\base_retail_sentences\\Retailbiancomondatok_v1.docx'
inputDoc = Document(inputDocPath)

outputDocPath = r'..\base_retail_sentences\\Retailbiancomondatok_v11.docx'
outputDoc = Document()

for elm in inputDoc._element:    
    outputDoc._element.append(elm)    

outputDoc.save(outputDocPath)
