#!/usr/bin/env python

"""
Script generates simulated test files for use in development. Given a single feature extraction file
and list of spike in probes it generates an in silico test set of files simulating expected data, including
instances where multiple probes fail.
"""

import argparse
from analysis_helpers import *

'''This script uses a template to generate test files for arraySpiker so that a range of scenarios and edge cases
can be tested'''

"""Import Arguments from command line"""
parser = argparse.ArgumentParser(
    description='Generate test data FE files for testing array_spiker.py')
parser.add_argument('-file', '-f', type=str, help='Import template file containing outline Feature Extraction data')
parser.add_argument('-output_dir', '-o', type=str, help='File path to output directory')
parser.add_argument('-create_template', action='store_true', help='Create template file from given FE file')

args = parser.parse_args()

filename = args.file


def down_sample_fe_file(fe_file):
    """Downsamples the provided file to provide a minimal user example of a Feature Extraction file for use
     in testing.It does this by only including lines in the file which correspond to spike in probes listed in the
     provide config.yaml file."""
    # Parse config.yaml file for all probes available to 'spike into' samples:
    spike_in_probes = parse_config_file()
    # Read in user selected Feature Extraction file which will form the template for all generated test files.
    df = pandas.read_csv(fe_file, sep='\t', skiprows=9, header=0)  # Skip 9 rows of comments, use line 10 as header.
    # Only keep lines that relate to Spike In probes
    df = df[df['ProbeName'].isin(spike_in_probes)]
    # Sort dataframe by 'ProbeName' to aid interpretation of results
    df = df.sort_values(by=['ProbeName'])
    return df


def generate_test_files(df):
    """"Takes a dataframe from downSampleFEfile() and generates a range of test data for array_spiker.py. It does this
    by replacing"""

    # Set IsSaturated flags to false
    df['gIsSaturated'] = 0
    df['rIsSaturated'] = 0

    # Generate files a correctly run sample:

    # Generate files simulating failure of one or more replicates on the array:

    # Generate files simulating failure of one or more probes:

    # Save generated files:
    return df


print(generate_test_files(down_sample_fe_file(filename)))

print(generate_test_files(down_sample_fe_file("./test_files/258503010103_S01_Guys121919_CGH_1100_Jul11_2_1_3.txt")))
