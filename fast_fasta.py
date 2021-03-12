# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 20:59:29 2021

@author: brony

This code takes .txt files containing protein sequences from a folder and 
turns them into a .fasta file called Proteins.fasta with the filename as the
identifier

"""

import os
import textwrap
import pandas as pd


# create folder path where protein .txt files are stored
pro_path = 'Proteins'

# create a .fasta file to store the protein sequences
pro_file = open('fast_fasta.fasta', 'w+')
info = pd.read_csv('protein_information.csv')
i = 0

# add protein sequences from individual .txt files into .fasta
for protein in os.listdir(pro_path):
    # access each file in Proteins folder
    file = open(pro_path + '\\' + protein, 'r', encoding='utf-8-sig')
    # set > for .fasta format and use file name as identifier (for now)
    description = info.iloc[i,:].to_string(header = False, index = False)
    i += 1
    description = description.replace('\n', ' ')
    description = description.replace('  ', '')
    pro_file.write('>' + protein[0:-4] + ' ' + description + '\n')
    # resize .txt file lines so that all can be seen in .fasta
    for line in file:
        # remove formatting from the txt file and set character width of 80
        line = line.strip()
        line = textwrap.fill(line, width = 80)
        pro_file.write(line + '\n')
    # close both files
    file.close()
pro_file.close()

# NOTE: rerunning the script will overwrite existing Proteins.fasta files


