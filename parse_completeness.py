import sys

# Input and output file paths
input_file = sys.argv[1]
output_file = sys.argv[2]

# Initialize variables
marker_lineage_column = 'Marker lineage'
bin_id_column = 'Bin Id'
cyanobacteria_bins = []

# Open the file and parse the contents
with open(input_file, 'r') as f:
    lines = f.readlines()

    # Flag to indicate if we are in the table section
    in_table = False

    for line in lines:
        # Detect the start of the table by looking for the header or a specific pattern
        if 'Bin Id' in line and 'Marker lineage' in line:
            in_table = True
            continue
        
        if in_table:
            # Split the line into columns
            columns = line.split()
            if len(columns) < 2:
                continue
            
            # Extract the Bin Id and Marker lineage
            bin_id = columns[0]
            marker_lineage = columns[1]

            # Check if the Marker lineage contains 'p__Cyanobacteria'. Replace it with any other desired organism
            if 'p__Cyanobacteria' in marker_lineage:
                cyanobacteria_bins.append(bin_id)

# Write the selected bins to the output file
with open(output_file, 'w') as f:
    for bin_id in cyanobacteria_bins:
        f.write(f"results/metabat/bins/{bin_id}.fa\n")

print(f"Identified bins for p__Cyanobacteria: {cyanobacteria_bins}")

