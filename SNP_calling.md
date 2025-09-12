# SNP Calling.md 

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

I realised I need to trim the 3p' adapter:

```
mv samples samples_before_trimming
python Clean3pAdapteronShortDemuxReads.py samples_before_trimming samples
module load cutadapt FastQC BWA SAMtools Stacks snakemake
snakemake --dag filtered.recode.vcf | dot -Tsvg > dag.svg # create the graph of rules 
snakemake --cores all filtered.recode.vcf
```

Two individuals ended up with over 95% missing data:

```
vcftools --max-missing 0.8 --vcf  output_SNPcalling/populations.snps.vcf --remove-indv Sy169 --remove-indv Sy96 --recode --out filtered_31

```
19690 SNPs for 31 individuals, might be a reflection of a relativelty tight geographic dataset?

```
mv filtered_31.recode.vcf  OG9739_stoneflies_19690SNPs_31inds_maxmissing08.snps.vcf
gzip OG9739_stoneflies_19690SNPs_31inds_maxmissing08.snps.vcf
```


## OG9759-460919822
** This one does not do the 3p adapters **
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


```
module load cutadapt FastQC BWA SAMtools Stacks snakemake
snakemake --dag filtered.recode.vcf | dot -Tsvg > dag.svg # create the graph of rules 
snakemake --cores all filtered.recode.vcf
```
65k SNPs for 95 insidividual.

3 individuals with more than 80% missing data:

```
Awa_780m_LW_30.11_female_C2     65262   0       57247   0.877187
PLC_249.6       65262   0       57824   0.886029
PLC_92.3        65262   0       64495   0.988247
```
```
vcftools --vcf output_SNPcalling/populations.snps.vcf --max-missing 0.8  --recode --out filtered --remove-indv Awa_780m_LW_30.11_female_C2  --remove-indv PLC_249.6  --remove-indv PLC_92.3
```

```
mv filtered.recode.vcf  OG9759_stoneflies_73118SNPs_92inds_maxmissing08.snps.vcf
gzip OG9759_stoneflies_73118SNPs_92inds_maxmissing08.snps.vcf
```
73118 SNPs for 02k indivudals

## angus_stoneflies

DONE SEPARAELY BY ANGUS
