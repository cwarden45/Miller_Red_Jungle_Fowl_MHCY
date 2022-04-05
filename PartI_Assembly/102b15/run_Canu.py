import os
import sys

canu = "/opt/canu-1.5/Linux-amd64/bin/canu"

prefix = "BAC_102b15_subreads"
fq = "BAC_102b15_LENGTH_FILTERED_subreads.fq"

spec_file = "VM.spec"

command = canu + " -p " + prefix + "_canu -d " + prefix + " genomeSize=100k -s "+spec_file+" -pacbio-raw " + fq
os.system(command)