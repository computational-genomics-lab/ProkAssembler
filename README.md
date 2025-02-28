# Genome-assembly-Pipelines
ProkAssembly
Snakemake pipeline for improved microbial genome assembly

# Requirements
To run the pipeline the following Software/package/tool are the pre-requisites:

- Python 3
- Snakemake
- Flye v.2.9.2
- Metabat v.2.12.1
- Medaka v.1.7.3
- Polypolish v.3
- Spades v3.13.1
- CheckM v.1.2.2
- Busco v.5.4.6
  
# Quick Start

```batch
git clone https://github.com/computational-genomics-lab/ProkAssembly.git
cd ProkAssembly

# Prepare Long reads, one file per sample. 
#If multiple samples:
cat sample1.fastq sample2.fastq ... > merged_sample.fastq

# Prepare Short reads, one pair of file per sample. 
#If multiple samples:
cat sample1_R1.fastq sample2_R1.fastq ... > merged_sample_R1.fastq
cat sample1_R2.fastq sample2_R2.fastq ... > merged_sample_R2.fastq

#Prepare a configuration (config.yaml) file as given.
``` 

  
  # Configuration file
A config.yaml file has been included in the ProkAssembly directory. It has the following format :
```batch
#Provide the path of your working directory. Example path is given below.
# un comment workdir and put proper values in the path. In case, the workdir is not provided
# the script will start from the github base directory
#workdir: "/home/[PATH_TO_ASSEMBLY_WORKFLOW]/assembly_pipeline"

#Provide the path of the filtered long reads.
# Note: In case multiple fastq files are there, concatenate them to make a single file
#Example path : "/home/[PATH]/highQuality-reads.fastq"
filtered_long_reads: "/[COMPLETE_PATH_TO_THE_FILE]"

#Provide the path of the filtered paired end short reads.
#Example:
#R1: "/home/XXX/283R1.fastq"
#R2: "/home/xxx/283R2.fastq"
filtered_short_reads:
R1: "/[COMPLETE_PATH]"
R2: "/[COMPLETE_PATH]"

#Mention number of threads to use
threads: 40

#Give the desired organism dataset from Busco database for genome quality assesment.
#Example: One can choose from the commandline `busco --list-datasets`
#busco_lineage : cyanobacteria_odb10    
busco_lineage: "Preferred busco dataset"

```
# Test dataset
A test dataset containing a pair of ONT and Illumina sequencing data  is available in the repository https://doi.org/10.5281/zenodo.14869645. 

# Run workflow
```batch
snakemake --snakefile Master_pipeline --core 40
```
# Included Programs
**'Nocon assembly'** pipeline for pure reads (contamination ≤1%)

**'Lowcon assembly'** pipeline for pure reads with minor contamination (contamination >1-≤7%)

**'Highcon assembly'** pipeline for reads with high contamination (uniculture and contamination >7%)

**'HighconHetero assembly'** pipeline for reads with high contamination and heterogeneity (multi-strain and contamination >7%)

‘Nocon assembly’, ‘Lowcon assembly’, ‘Highcon assembly’, ‘HighconHetero assembly’ are four different genome assembly pipelines developed by our group using Snakemake program. Each pipeline is standardized for a specific read category. Read categorization can be performed using 'Master_pipeline' which detects contamination and heterogeneity for individual readset. Depending on the contamination and heterogeneity value, it will automatically execute a particular downstream assembly pipeline for producing a high quality genome assembly.

![Flowchart of the Process](https://github.com/computational-genomics-lab/ProkAssembly/blob/main/fig1a.jpg?raw=true)


# Detailed description of the pipelines:

**Nocon assembly and Lowcon assembly pipelines:**

Nocon assembly and Lowcon assembly pipeline generate a draft assembly without and with meta option respectively using Flye from filtered long reads. The path of the .fastq files containing the respective long reads may be provided in the config file (config.yaml).
Metabat segregates the contigs of the assembly into separate bins based on their divergence.
Subsequently, CheckM reports the lineages of the bins produced.
A python script, “parse_completeness.py” allow the selection of the bins for any particular organism for further processing in the subsequent pipeline. Name of the desired organism can be taken from CheckM database (eg. p__Cyanobacteria) and written in the parse_completeness.py script.
The next step involves the correction of the selected contigs with long reads using Medaka.
Polishing of the corrected assembly using short Illumina reads (path provided in config file) will be performed by Polypolish.
Finally, the polished assembly undergoes CheckM and Busco quality check, which reports completeness, contamination and strain heterogeneity of the final assembly.

**Highcon assembly and HighconHetero assembly pipelines:**

The hybrid assembly pipelines Highcon assembly and HighconHetero assembly, that include both short and long reads, are developed using Spades with and without meta option respectively. 
Binning of the draft hybrid assembly is performed with Metabat to separate contamination from the original genome.
The pipelines are further extended to include CheckM analysis, which assesses completeness, contamination, strain heterogeneity, and lineage specificity of different bins produced.
The bin containing the genome of interest will be screened using a python script “parse_completeness.py”. Name of the desired organism can be taken from CheckM database (eg. p__Cyanobacteria) and written in the parse_completeness.py script.
Busco assessment of the genome assembly in the selected bin will be reported.


