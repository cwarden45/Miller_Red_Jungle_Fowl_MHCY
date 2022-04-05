import sys
import re
import os

rgSam = "BWA-MEM_Alignment/5clones-220203.MANUAL_EDIT.sam"
bwaRef= "../Contig1_draft_201118b/Contig1-9changes_201118.fa"
pileup = "BWA-MEM_Alignment/5clones-220203.MANUAL_EDIT.pileup"

command = "samtools mpileup -f "+ bwaRef + " " + rgSam + " > " + pileup
os.system(command)
