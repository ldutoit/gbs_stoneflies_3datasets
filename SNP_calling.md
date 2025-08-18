

I used the RAD_snakemake pipeline:

```
git clone https://github.com/ldutoit/RAD_snakemake.git
```

Then, within ach of threee different folders, I ran the three datasets.



## OG9739-458159104 

```
#/nesi/nobackup/uoo03737/ludo/stoneflies/RAD_snakemake
```

config file:
```
mode: "refmap" # "denovo" or "refmap"
raw_fastq: # single-end currently not supported
  forward: "../../OG9739-458159104/AAHCWL7M5-9739-P1-00-01_S1_L001_R1_001.fastq.gz"
  reverse: "../../OG9739-458159104/AAHCWL7M5-9739-P1-00-01_S1_L001_R2_001.fastq.gz"
cutadapt:
  adapter: "AGATCGGAAGAGC" # Sequence of the adapter
  length: "50" # Mininimum length for refmap, common length for denovo
  minimum_phred: "25"  # Changed '=' to ':'
genome: # only needed for refmap mode
  ref: "stoneflygenomeassemblyv1.fasta"
vcf_filtering:
  parameters: "--max-missing 0.8 --maf 0.0001" # vcftools arguments, passed at once
```

## OG9759-460919822

```
##/nesi/nobackup/uoo03737/ludo//OG9757_stoneflies
```
config.yaml
```

mode: "refmap" # "denovo" or "refmap"
raw_fastq: # single-end currently not supported
  forward: "../OG9759-460919822/AAH7VNHM5-9759-P1-00-01_S1_L001_R2_001.fastq.gz"
  reverse: "../OG9759-460919822/AAH7VNHM5-9759-P1-00-01_S1_L001_R2_001.fastq.gz"
cutadapt:
  adapter: "AGATCGGAAGAGC" # Sequence of the adapter
  length: "50" # Mininimum length for refmap, common length for denovo
  minimum_phred: "25"  # Changed '=' to ':'
genome: # only needed for refmap mode
  ref: "stoneflygenomeassemblyv1.fasta"
vcf_filtering:
  parameters: "--max-missing 0.8 --maf 0.0001" # vcftools arguments, passed at once
[ludovic.dutoit@login03 OG9757_stoneflies]$ 
```

## angus_stoneflies

```
#/nesi/nobackup/uoo03737/ludo/angus_stoneflies
```

```
mode: "refmap" # "denovo" or "refmap"
raw_fastq: # single-end currently not supported
  forward: "../angus_source_files/AAFL27TM5-8834-P1-00-01_S1_L001_R1_001.fastq.gz"
  reverse: "../angus_source_files/AAFL27TM5-8834-P1-00-01_S1_L001_R2_001.fastq.gz"
cutadapt:
  adapter: "AGATCGGAAGAGC" # Sequence of the adapter
  length: "50" # Mininimum length for refmap, common length for denovo
  minimum_phred: "25"  # Changed '=' to ':'
genome: # only needed for refmap mode
  ref: "stoneflygenomeassemblyv1.fasta"
vcf_filtering:
  parameters: "--max-missing 0.8 --maf 0.0001" # vcftools arguments, passed at once
```


I realised I need to trim the 3p' adapter:

```
mv samples samples_before_trimming
python Clean3pAdapteronShortDemuxReads.py samples_before_trimming samples
module load cutadapt FastQC BWA SAMtools Stacks snakemake
snakemake --dag filtered.recode.vcf | dot -Tsvg > dag.svg # create the graph of rules 
snakemake --cores all filtered.recode.vcf
```

I did the vcf filtering manually at the end:

```
vcftools --vcf output_SNPcalling/populations.snps.vcf --max-missing 0.8 --maf 0.0001 --recode --out filtered
vcftools --vcf filtered.recode.vcf --missing-indv
```

6 samples with "no" data past mapping (failing ref_map):

```
Bay_09_25
Opo_11
Opo_9
Rob_E14
Tho_S17
Tho_S22
```



