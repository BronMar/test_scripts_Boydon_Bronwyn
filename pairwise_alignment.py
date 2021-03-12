# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 21:58:23 2021

@author: brony
"""

# pairwise alignment for two sequences

from Bio import SeqIO
from Bio import Align
from Bio.Align import substitution_matrices

# import sequences from blast_fasta.fasta file
sequences = SeqIO.parse('blast_fasta.fasta', 'fasta')
seq1 = next(sequences)
seq2 = next(sequences)

# use biopython pairwise aligner with settings to replicate EMBOSS needle
aligner = Align.PairwiseAligner()
aligner.open_gap_score = -15
aligner.extend_gap_score = -0.5
aligner.substitution_matrix = substitution_matrices.load('BLOSUM62')

# align sequences and use first alignment for visualisation
alignments = aligner.align(seq1.seq, seq2.seq)
alignment = alignments[0]

# calculate statistics for alignment
a = str(alignment)
length = len(a)/3
length = int(length)
identity = a.count('|')/length
gaps = a.count('-')/length

# write statistics to alignment file
output = open('pairwise_alignment.txt', 'w')
output.write('Length: ' + '\t' + str(length) + '\n')
output.write('Identity: ' + '\t' + '{:.1%}'.format(identity) + '\n')
output.write('Gaps: ' + '\t' + '\t' + '{:.1%}'.format(gaps) + '\n')
output.write('Score: ' + '\t' + '\t' + str(alignments.score) + '\n')
output.write('\n')

# reformat alignment to write to file
for x in range(int(length/50)):
    star = 50*x
    end = 50*(x+1)
    output.write('seq_1' + '\t' + a[star:end] + '\n' + 
                 '\t' + a[length+star:length+end] + '\n' + 
                 'seq_2' + '\t' + a[2*length+star:2*length+end] + '\n')
    output.write('\n')
output.close()



