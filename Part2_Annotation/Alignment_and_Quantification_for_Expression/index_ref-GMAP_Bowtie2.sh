#!/bin/bash

combinedRef=truncated_galGal5_with_AllContigs.fa
refID=galGalCust

#reference folder
gmap_build -d $refID -D . -c chrM $combinedRef

#reference common beginning of .bt2 files
bowtie2-build $combinedRef $refID