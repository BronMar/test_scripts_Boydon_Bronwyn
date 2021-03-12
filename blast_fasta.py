# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 21:30:07 2021

@author: brony

This script parses .txt files in a folder named 'Proteins' and returns a 
Proteins.fasta with the file names as the identifiers. Then, it reopens that 
.fasta file to run a blast search on the contents and returns output.fasta 
with the file name, the name of the top BLASTP hit, and the E-value as the new
sequence identifier.   
"""


import os
import textwrap

# create folder path where protein .txt files are stored
pro_path = 'Proteins'

# create a .fasta file to store the protein sequences
pro_file = open('file_fasta.fasta', 'w+')

# add protein sequences from individual .txt files into .fasta
for protein in os.listdir(pro_path):
    # access each file in Proteins folder
    file = open(pro_path + '\\' + protein, 'r', encoding='utf-8-sig')
    # set > for .fasta format and use file name as identifier (for now)
    pro_file.write('>' + protein[0:-4] + '\n')
    # resize .txt file lines so that all can be seen in .fasta
    for line in file:
        # remove formatting from the txt file and set character width of 80
        line = line.strip()
        line = textwrap.fill(line, width = 80)
        pro_file.write(line + '\n')
    # close both files
    file.close()
pro_file.close()

# import tools for handling sequences, calling BLAST, and parsing BLAST
# outputs
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO


filename = 'file_fasta.fasta'

# open Protein.fasta file from previous step and create a new output file
with open(filename, 'r') as sequences, open('blast_fasta.fasta', 'w') as output:
    for seq in SeqIO.parse(sequences, 'fasta'):        
        # run a blastp query
        result_handle = NCBIWWW.qblast('blastp', 'nr', seq.seq, alignments=1)
        blast_record = NCBIXML.read(result_handle)  
        # record required outputs from blast query
        best = blast_record.alignments[0]
        if 'gb' in best.title:
            start = best.title.index('gb')
        else: start = 0
        title = ' ' + (str(best.title[start:start+60]))
        title = title.replace('\n', '')
        title = title.replace('>', '')
        seq.description += title
        SeqIO.write(seq, output, 'fasta')
        
sequences.close()    
output.close()