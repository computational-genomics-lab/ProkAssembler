# Genome-assembly-Pipelines
ProkAssembly
Snakemake pipeline for improved microbial genome assembly

*For latest version*
```batch
git clone https://github.com/computational-genomics-lab/ProkAssembly.git

```
# Requirements
To run the pipeline Software/package/tool required to install:

- Python 3
- Snakemake
- Flye v.2.9.2
- Metabat v.2.12.1
- Medaka v.1.7.3
- Polypolish v.3
- Spades v3.13.1
- CheckM v.1.2.2
- Busco v.5.4.6
# Quick Usage
```batch
snakemake --snakefile 'Master_pipeline' --core 40
```
**'Nocon assembly'** pipeline for pure reads (contamination ≤1%)

**'Lowcon assembly'** pipeline for pure reads with minor contamination (contamination >1-≤7%)

**'Highcon assembly'** pipeline for reads with high contamination (uniculture and contamination >7%)

**'HighconHetero assembly'** pipeline for reads with high contamination and heterogeneity (multi-strain and contamination >7%)

‘Nocon assembly’, ‘Lowcon assembly’, ‘Highcon assembly’, ‘HighconHetero assembly’ are four different genome assembly pipelines developed by our group using Snakemake program. Each pipeline is standardized for a specific read category. Read categorization can be performed using 'Master_pipeline' which detects contamination and heterogeneity for individual readset. Depending on the contamination and heterogeneity value, it will automatically execute a particular downstream assembly pipeline for producing a high quality genome assembly.

![Flowchart of the Process](https://github.com/computational-genomics-lab/ProkAssembly/blob/main/fig1a.jpg?raw=true)

# Configuration file
A config.yaml file has been included in the ProkAssembly directory. It has the following format :
```batch
filtered_long_reads: "/home/sutripa/Benchmarking/Inhouse_data/268/highQuality-reads.fastq"
#Mention number of threads to use
threads: 40
#Provide the path of the filtered paired end short reads. Example path is given below for R1 and R2
filtered_short_reads:
  R1: "/home/sutripa/Benchmarking/Inhouse_data/268/268I_R1.fastq"
  R2: "/home/sutripa/Benchmarking/Inhouse_data/268/268I_R2.fastq"
#Give the organism name from Busco database for genome quality assesment, Example organism is given below.    
busco_lineage: cyanobacteria_odb10
```
# Detailed description of the pipelines:

**Nocon assembly and Lowcon assembly pipelines:**

Nocon assembly and Lowcon assembly pipeline generate a draft assembly without meta and with meta option, respectively using Flye from filtered long reads. The path of the .fastq files containing the respective long reads may be provided in the config file (config.yaml).
Metabat segregates the contigs of the assembly into separate bins based on their divergence.
Subsequently, CheckM reports the lineage of the bins produced.
A python script, “parse_completeness.py” allow the selection of the bins for any particular organism for further processing in the subsequent pipeline. Name of the desired organism can be taken from CheckM database (eg. p__Cyanobacteria) and written in the parse_completeness.py script.
The next step involves the correction of the selected contigs with long reads using Medaka.
Polishing of the corrected assembly using short Illumina reads (path provided in config file) will be performed by Polypolish.
Finally, the polished assembly undergoes CheckM and Busco quality check, which reports completeness, contamination and strain heterogeneity of the final assembly.

**Highcon assembly and HighconHetero assembly pipelines:**

The hybrid assembly pipelines Highcon assembly and HighconHetero assembly, that include both short and long reads, are developed using Spades with meta and without meta option respectively. 
Binning of the draft hybrid assembly is performed with Metabat to separate contamination from the original genome.
The pipelines are further extended to include CheckM analysis, which assesses completeness, contamination, strain heterogeneity, and lineage specificity of different bins produced.
The bin containing the genome of interest will be screened using a python script “parse_completeness.py”. Name of the desired organism can be taken from CheckM database (eg. p__Cyanobacteria) and written in the parse_completeness.py script.
Busco assessment of the genome assembly in the selected bin will be reported.


