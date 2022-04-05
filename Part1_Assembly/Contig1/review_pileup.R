#setwd("R:\\mmiller\\Seq\\BAC_annotation\\Code\\190-173-19\\Contig1_draft_220203-TEST")

inputfile="BWA-MEM_Alignment/5clones-220203.MANUAL_EDIT.pileup"
outputfile="BWA-MEM_Alignment/5clones-220203.MANUAL_EDIT.pileup_with_status.txt"
MHCY.start = 106161 #1st occurance of GGLTR7-int 

input.table = read.delim(inputfile, head=F, sep="\t")

status = c()

for (i in 1:nrow(input.table)){
	temp.cov=input.table$V4[i]
	
	if(temp.cov >=3){
		base.str = input.table$V5[i]
		base.str = gsub("\\^]","",base.str)
		base.str = gsub("\\$","",base.str)
		if(base.str == paste(rep(".",temp.cov),collapse="")){
			status[i]="KEEP"
		}else if(nchar(base.str) ==temp.cov){
			temp.bases = unlist(strsplit(base.str,split=""))

			base.count = table(temp.bases)
			base.percent = base.count / temp.cov
			majority = base.count[base.percent > 0.5]
			if(length(majority) == 0){
				if(input.table$V2[i] < MHCY.start){
					#no consensus to change
					status[i]="KEEP_NOR"
				}else{
					#no consensus to change
					status[i]="KEEP"
				}#end else
			}else{
				if (names(majority) == "."){
					status[i]="KEEP"
				}else{					
					base.count = table(temp.bases)
					base.percent = base.count / temp.cov
					majority = base.count[base.percent > 0.5]

					if (names(majority) == "*"){
						if(input.table$V2[i] < MHCY.start){
							#no consensus to change
							status[i]="NOR_DEL"
						}else{
							#no consensus to change
							status[i]="DEL"
						}#end else
					}else{
						print("Define alternate seq")
						print(input.table[i,])
						stop()
					}
				}#end else
			}#end else
		}else{		
			ins.reg_obj = gregexpr("(\\+\\d+\\w+)",base.str)
			insertions = unlist(regmatches(base.str, ins.reg_obj))
			
			del.reg_obj = gregexpr("(-\\d+\\w+)",base.str)
			deletions = unlist(regmatches(base.str, del.reg_obj))
			
			if(length(insertions) > 0.5 * temp.cov){
				insert_table = table(insertions)
				max_insert = insert_table[insert_table==max(insert_table)]
				if(max_insert > 0.5 * temp.cov){
					status[i]=names(max_insert)
				}else if(input.table$V2[i] < MHCY.start){
					#no consensus to change
					status[i]="KEEP_NOR"
				}else{
					#no consensus to change
					status[i]="KEEP"
				}#end else
			}else if(length(deletions) > 0.5 * temp.cov){
				del_table = table(deletions)
				max_del = del_table[del_table == max(del_table)]
				if(max_del > 0.5 * temp.cov){
					status[i]=names(max_del)
				}else if(input.table$V2[i] < MHCY.start){
					#no consensus to change
					status[i]="KEEP_NOR"
				}else{
					#no consensus to change
					status[i]="KEEP"
				}#end else
			}else{
				print("###Check if I should keep following example:###")
				print(input.table[i,])
				#print to see if I can visually check examples
				if(input.table$V2[i] < MHCY.start){
					#no consensus to change
					status[i]="KEEP_NOR"
				}else{
					#no consensus to change
					status[i]="KEEP"
				}#end else			
			}#end else
		}#end else
	}else{
		status[i]="LowCov"
	}#end else
	
}#end def for (i in 1:nrow(input.table))

colnames(input.table)=c("seq","pos","ref","cov","base","qual")
output.table = data.frame(input.table, status)

write.table(output.table, outputfile, quote=F, sep="\t", row.names=F)