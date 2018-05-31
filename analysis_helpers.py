"""Helper functions for arraySpiker which are used to import, process, and analyse the spiked in data."""

from __future__ import print_function
import itertools
import matplotlib
matplotlib.use('agg') #To bypass X-server on headless linux server https://stackoverflow.com/questions/35737116/runtimeerror-invalid-display-variable
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas
import re
import seaborn as sns  # Produces heatmap of results which are useful for debugging
import datetime
import yaml  # pyYAML


def create_output_directory(directory):
    # Add date stamp to file name
    today = datetime.date.today()
    today = today.strftime('%d%b%Y')
    directory_name = "array_spiker_output_"
    directory = os.path.join(directory, directory_name + today)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def calculate_spiked_probes_combinations(spike_in_probes, n=3):
    """From a list of n probes calculate a unique permutation of three probes to spike to each sample on
    the array.  NOTE: As lexigraphical order is irrelevant we use itertools.combinations rather than
    itertools.permutations for this task"""
    spike_in_trios = list(itertools.combinations(spike_in_probes, n))
    return list(spike_in_trios)


def num_spiked_probes_combinations(spike_in_probes, n=3):
    """Number of unique combinations of trios for n probes i.e For 10 probes 120 unique combinations"""
    num_of_combinations = len(calculate_spiked_probes_combinations(spike_in_probes, n))
    return num_of_combinations


def parse_config_file():
    """Parses config.yaml file returning list of Spike In probes"""
    with open("config.yaml", 'r') as yaml_file:
        try:
            config = yaml.load(yaml_file)
            # Import spike in probe IDs
            spike_in_probes = config["spikeInProbes"]
        except yaml.YAMLError as exc:
            print(exc)
    return spike_in_probes


def parse_data_file(fe_file):
    """Parses Agilent Array Feature Extraction (FE) files returning Pandas dataframe of selected fields"""
    f = open(fe_file, "r")
    spike_in_probes = parse_config_file()
    d = []  # Initialises matrix to hold extracted lines.
    for line in f:
        for probe in spike_in_probes:
            if re.match("(.*)%s(.*)" % probe, line):
                fields = line.strip().split()
                # Extracted relevant fields - (0-based indexing)
                d.append({'FeatureNum': fields[1], 'ProbeName': fields[6], 'SystematicName': fields[7],
                          'gProcessedSignal': fields[13], 'rProcessedSignal': fields[14], 'gMedianSignal': fields[17],
                          'rMedianSignal': fields[18], 'gBGMedianSignal': fields[19], 'rBGMedianSignal': fields[20],
                          'gIsSaturated': fields[23], 'rIsSaturated': fields[24]})
    df = pandas.DataFrame(d)
    # Cast columns to int or float as appropriate:
    df[['gIsSaturated', 'rIsSaturated']] = df[['gIsSaturated', 'rIsSaturated']].astype(int)
    df[['gProcessedSignal', 'rProcessedSignal', 'gMedianSignal', 'rMedianSignal', 'gBGMedianSignal',
        'rBGMedianSignal']] = df[
        ['gProcessedSignal', 'rProcessedSignal', 'gMedianSignal', 'rMedianSignal', 'gBGMedianSignal',
         'rBGMedianSignal']].astype(float)
    # Add column identifying the file which the data was imported from:
    df['FE_filename'] = fe_file
    return df


# Function reiterates through all FE files for a run and aggregates the data into one dataframe:
def import_data(fe_files):
    first_import = True  # Set before for loop below
    for fe_file in fe_files:
        # On importing first set of data initialise dataframe, additional datasets are then appended to
        # to this dataframe:
        # TODO check if I need if statement to initialise df
        if first_import is True:
            df = parse_data_file(fe_file)
            first_import = False
        else:
            df2 = parse_data_file(fe_file)
            df = df.append(df2)
    return df


# The array has 3 replicates on the array for each probe - where the data is consistent between each replicate
# this function collapses the data into a single row, if the replicates disagree it raises an error message
# identifying the discrepancy.
def summarise_array_replicates(df, spike_in_probes):
    # Format data
    summarised_df = pandas.pivot_table(df, values=['gIsSaturated', 'rIsSaturated'],
                                       index=['ProbeName'],
                                       columns=['FE_filename'],
                                       aggfunc=np.sum)
    return summarised_df


def write_log(dataframe, prefix, directory_path):  # TODO get run ID from MOKA and add to log name
    """Save log file identified by date"""
    # Add date stamp to file name
    today = datetime.date.today()
    today = today.strftime('%d%b%Y')
    # Use prefix and timestamp to generate name for log file.
    log_file = "%s_%s_spikeInLog.txt" % (prefix, today)
    log_file_path = os.path.join(directory_path, log_file)
    dataframe.to_csv(log_file_path, header=True, index=True)
    return log_file_path


def make_pretty_label(x_label):  # TODO Make this function fail gracefully
    """Return shortened file name string to make it easier to read in tables and on plots."""
    pretty_label = os.path.basename(x_label)  # Extract basename
    pretty_label = os.path.splitext(pretty_label)[0]  # Remove file suffix
    # Split file name on "_", keep first and last 3 fields and create new label
    pretty_label = pretty_label.split("_")[0] + "_" + "_".join(pretty_label.split("_")[slice(-3, None)])
    return pretty_label


def heatmap_spike_ins(df, figure_name, directory_path):
    """Visualise results as heatmap to aid in debugging and testing:"""
    fig = sns.heatmap(df, annot=True, vmin=0, vmax=3, cbar=False,
                      # Custom colour map, 0=white, TODO
                      cmap=["White", "#fc9272", "#fc9272", "#2ca25f"], square=True, linewidths=.5)
    fig.set_yticklabels(fig.get_yticklabels(), rotation=0, fontsize=5)
    fig.set_xticklabels(fig.get_xticklabels(), rotation=90, fontsize=5)
    # plt.tick_params(labelsize=7)
    fig.xaxis.tick_top()
    # Pad margins so that markers don't get clipped by the axes
    # plt.margins(0.01)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(top=0.60)
    output_file_path = os.path.join(directory_path, figure_name)
    plt.savefig(output_file_path)
    plt.clf()


def plot_values(dataframe, figure_name, directory_path):
    """Plots red/green channels for all probes on the same axis"""
    fig, axarr = plt.subplots(2, sharex="all")
    plt.ylabel("Median Signal")
    axarr[0].scatter(dataframe['ProbeName'], dataframe['gMedianSignal'], color='green', marker='_')
    axarr[0].set_ylim([0, 70000])
    axarr[0].axhline(y=65527, alpha=0.5, dashes=[1, 1], color='grey')
    axarr[0].tick_params(axis='y', which='major', labelsize=6)
    axarr[1].scatter(dataframe['ProbeName'], dataframe['rMedianSignal'], color='red', marker='_')
    axarr[1].set_ylim([0, 70000])
    axarr[1].axhline(y=65527, alpha=0.5, dashes=[1, 1], color='grey')
    axarr[1].tick_params(axis='y', which='major', labelsize=6)
    plt.xticks(rotation='vertical')
    # Create space for x labels
    plt.subplots_adjust(bottom=0.30)
    plt.tick_params(axis='x', which='major', labelsize=6)
    plt.xlabel("Probe Names")
    output_file_path = os.path.join(directory_path, figure_name)
    plt.savefig(output_file_path, format='pdf')
    plt.clf()
