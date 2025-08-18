#!/usr/bin/env python

## Clean3pAdapteronShortDemuxReads.py
## Ludovic Dutoit, 2022, email dutoit.ludovic@gmail.com for questions
##To clean the output of process_radtags (Stacks, Catchen et al.) This script is a quick solution to remove the second barcode on the first read or the first barcode on the reverse read.
## It is not barcode specific. It is simply looking for a few random bases trailing the second restriction cutsite before the end of the sequence.
## The files have to be cleaned from adapters before using this script.
## In this case, THE ENZYME ON BOTH SIDE IS THE SAME (i.e. GBS protocol, Elshire et al. 2011), it would have to be adapted for different enzyymes on 3' of forward or reverse.
# INPUT files, typically output of process radtags. Files have to be gzipped.
# OUTPUT files are not gzipped, it is a new folder with all the sequence files in the input folder but cleaned of trailing barcodes
# Parameters lines 16-20, to adapt


import gzip,re,os, argparse


##PARAMETERS TO ADAPT




#parser
parser = argparse.ArgumentParser() # add the parser
parser.add_argument("input_folder",help="Folder with all the gzipped output files of process_radtags") # add the parser
parser.add_argument("cleaned_folder", help=" output folder",type=str)
parser.add_argument("-e","--enzyme_cutsite", help="Enzyme cutsite (3' of both F and R reabd (GBS protocol)", type=str,default="TGCA")
parser.add_argument("-m","--max_barcode_length",help="Maximum length of barcode in the dataset",  type=int,default=8) 
args = parser.parse_args()

#input_folder="samples_all" # demultiplexed folder with output of process_radtags
#cleaned_folder="samples_all_cleaned" # clean folder for output
#enzyme_cutsite="TGCA" #pst1 # in my case, same enzyme for F and R reads.
#max_barcode_length=8 # Maximum length of barcode to look for.#



#Initialise a bunch of counts
n_matches=0
n_reads=0
total_length=0 # in bp
total_length_matches=0 #in bp
n_files=0

#Find all gzip files in input folder
files = [args.input_folder+"/"+file for file in os.listdir(args.input_folder) if file.endswith("gz")]

#If output folder does not exist, make it

if not os.path.exists(args.cleaned_folder):
		os.mkdir(args.cleaned_folder)

# For each gzip file
for file in files:
	n_files+=1
	print(file,n_files,"out of",len(files))
	original=gzip.open(file,"rt")
	output=open(args.cleaned_folder+"/"+os.path.basename(file)[:-3],"w") # not gzip output
	# the lines below loop record by record
	while True:
		line1 = original.readline() # @ ID line
		line2 = original.readline() #  sequence line ATGGG
		line3 = original.readline() # +
		line4 = original.readline() # Phred quality line
		if not line1 or not line2 or not line3 or not line4: break
		#print(line1)
		n_reads+=1
		total_length+=len(line2.strip())
		 # look for cutsite + at least one trailing bases or a max of args.max_barcode_length before the end of the read
		match=re.findall(args.enzyme_cutsite+"[ATGC]{1,"+str(args.max_barcode_length)+"}$",line2)
		if match: # There is a match
			n_matches+=1
			length_to_remove = len(match[0]) # figure out how much to remove
			total_length_matches+=length_to_remove 
			#remove it but not the enzyme cutsie
			#line2=args.enzyme_cutsite="TGCA"
			line2=line2[0:len(line2)-(length_to_remove)+len(args.enzyme_cutsite)-1]+"\n" # remove the bases from the seq
			line4=line2[0:len(line4)-(length_to_remove)+len(args.enzyme_cutsite)-1]+"\n" # remove the bases from the qual line
		output.write(line1+line2+line3+line4) # write the modified or unmodified line to output
	output.close()

#summary
print("removed patterns",n_matches, "times out of", n_reads," for a total of", (total_length_matches/total_length)*100,"percent of bases")
