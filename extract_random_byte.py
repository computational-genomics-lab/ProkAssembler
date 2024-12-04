import random
import os
from Bio import SeqIO

def extract_random_reads(input_file, output_file, target_size):
    records = list(SeqIO.parse(input_file, 'fastq'))
    total_size = sum(len(record) for record in records)
    
    if total_size <= target_size:
        # The entire file fits within the target size, copy the input file to the output file
        with open(output_file, 'w') as out_f:
            SeqIO.write(records, out_f, 'fastq')
        return
    
    selected_records = []
    selected_size = 0
    while selected_size < target_size:
        record = random.choice(records)
        selected_records.append(record)
        selected_size += len(record)
        records.remove(record)  # Remove the selected record to avoid duplicates
    
    with open(output_file, 'w') as out_f:
        SeqIO.write(selected_records, out_f, 'fastq')

# Set paths and parameters
input_file = 'input.fastq'       # Path to input FASTQ file
output_file = 'output.fastq'     # Path to output FASTQ file
target_size = 1024 * 1024 * 10   # Target size in bytes (e.g., 10 MB)

# Call the function to extract randomly based on file size and save to a new FASTQ file
extract_random_reads(input_file, output_file, target_size)

