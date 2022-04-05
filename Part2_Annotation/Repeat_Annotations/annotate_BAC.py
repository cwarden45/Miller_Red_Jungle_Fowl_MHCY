import os
import sys
import re

seqID = "Contig1"
refSeq = "../Contig1.fasta"

#RepeatMasker
repeatDir = "RepeatMasker/"
command = "mkdir " + repeatDir
os.system(command)

command = "/opt/RepeatMasker-open-4-0-6/RepeatMasker -species chicken -gff -dir "+repeatDir+" " + refSeq
os.system(command)
#maskedRef = repeatDir + seqID + ".fa.masked"

#TRF
matchWeight = 2
mismatchPenality = 7
indelPenality = 7
matchProb = 80
indelProb = 10
minScore = 50
maxPeriod = 500

trfDir = "TRF/"
command = "mkdir " + trfDir
os.system(command)

command = "/opt/trf409.linux64 " + refSeq + " "+str(matchWeight)+" "+str(mismatchPenality)+" "+str(indelPenality)+" "+str(matchProb)+" "+str(indelProb)+" "+str(minScore)+" "+str(maxPeriod)+" -d -m"
os.system(command)

command = "mv " + re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".dat " + trfDir +re.sub("../","",refSeq)+ "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".dat"
os.system(command)

doubleMaskedFA=re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".mask"
command = "mv " +doubleMaskedFA + " "+ trfDir +doubleMaskedFA
os.system(command)

command = "mv " + re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".1.html " + trfDir +re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".1.html"
os.system(command)

command = "mv " + re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".1.txt.html " + trfDir +re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".1.txt.html"
os.system(command)

command = "mv " + re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".2.html " + trfDir +re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".2.html"
os.system(command)

command = "mv " + re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".2.txt.html " + trfDir +re.sub("../","",refSeq) + "."+str(matchWeight)+"."+str(mismatchPenality)+"."+str(indelPenality)+"."+str(matchProb)+"."+str(indelProb)+"."+str(minScore)+"."+str(maxPeriod)+".2.txt.html"
os.system(command)