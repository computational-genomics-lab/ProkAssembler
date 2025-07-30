#!/bin/bash

# Exit on any error
set -e

echo ">>> Creating Conda environment from environment.yaml"
conda env create -f environment.yaml

# Activate conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate prok-pipeline-env

echo ">>> Cloning Polypolish from GitHub"
git clone https://github.com/rrwick/Polypolish.git
cd Polypolish
#install cargo for polypolish
sudo apt install cargo
echo ">>> Building Polypolish using cargo"
cargo build --release

#echo ">>> Copying binaries to /usr/local/bin (requires sudo)"
#sudo cp target/release/polypolish /usr/local/bin/
#sudo cp polypolish_insert_filter.py /usr/local/bin/
#chmod +x /usr/local/bin/polypolish_insert_filter.py

echo ">>> Installation complete!"
echo "To activate the environment in future sessions, run:"
echo "conda activate prok-pipeline-env"
