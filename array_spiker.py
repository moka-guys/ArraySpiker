#!/usr/bin/env python

"""
This script parses an Feature Extraction File produced by an Agilent Array, identifies the presence
of any spiked-in probes, and compares the unique combination of spiked-in probes for each sample to
those expected from the sample sheet.  Any mismatches are flagged to the user. See Readme.md for full
description.
See project requirement doc - https://github.com/moka-guys/project_requirements/tree/master/180111_array_spike_in
"""

from __future__ import print_function
import argparse
import datetime
import itertools
import matplotlib
matplotlib.use('agg') #To bypass X-server on headless linux server https://stackoverflow.com/questions/35737116/runtimeerror-invalid-display-variable
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas
import re
import seaborn as sns  # Produces heatmap of results which are useful for debugging
import yaml  # pyYAML
from analysis_helpers import *
from moka_helpers import *

""" 
Import Arguments from command line
"""
parser = argparse.ArgumentParser(
    description='Detect spiked-in probes from Agilent CGH FE extraction files and summarise results')
parser.add_argument('-file', '-f',
                    nargs='+',
                    help='Import single or multiple Agilent Feature Extraction files',
                    required=True)
parser.add_argument('-output_dir', '-o',
                    type=str,
                    help='File path to output directory',
                    required=True)
parser.add_argument('-spike_in_info', '-s',
                    type=str,
                    help='Optional file providing experimental design info which is used rather than MOKA. '
                         'Useful for testing or running script in a standalone mode.  Requires comma-delimited '
                         'file with 3 fields, ProbeName plus gSpike and rSpike where 0 or 1 indicates whether' 
                         'a spike should be expected on that channel',
                     required=False)
args = parser.parse_args()

"""
Get user specified arguments from commandline
"""

# User specified FE Files - List of strings as multiple FE files may relate to a single run.
testFiles = args.file

# User specified output directory for results/logs to be saved to. Directory will be created if it does not exist.
output_path = args.output_dir

# Flag to indicate whether this QC step has been passed.
QC_passed = False

# Create output directory in user specified directory for saving results:
output_directory = create_output_directory(output_path)

# Load a list of all spike in probes available from config.yaml file:
spike_in_probes = parse_config_file()

df = import_data(testFiles)
#df['label'] = df['FE_filename'].apply(make_pretty_label)
df['FE_filename'] = df['FE_filename'].apply(make_pretty_label)

# Save output to log file and print location to screen:
output_location = write_log(df, "verbose_results", output_directory)

print("Output saved in: %s" % output_location)


summarised_df = summarise_array_replicates(df, spike_in_probes)
# Sort so that log/visualizations will show probes in same order each time
summarised_df = summarised_df.sort_index(axis=1, level=1)

# Save heatmap showing probes present in each sample:
heatmap_spike_ins(summarised_df, "results_heatmap", output_directory)

# Save plot of intensities to aid in troubleshooting:
plot_values(df, "results_plot.pdf",output_directory)

write_log(summarised_df, "summary", output_directory)

# Function compares the expected/detected probes in each sample highlighting mismatches or situations
# where a probe failed.

# TODO Finish and create function for below code:

if args.spike_in_info is not None:  # If file has been passed as argument do not query Moka database
    # Read in expected spike in profile:
    expected_df = pandas.read_csv(args.spike_in_info)
    # Function to logically test whether spike ins/sample sheet match:
        # Compare summarised_df to expected_df
    # Are 3 spike in probes detected for each sample:
    # Throw error
    # Do the spike in probes detected match the sample sheet:
    # Throw error

    # Write out log file recording results:
    # Function to import the 3 probes added to each sample from MOKA:
else:
    # Pseudocode - obtain this info from Moka using moka_helpers.py functions
    # Pseudocode - create expected_df as above
    pass

