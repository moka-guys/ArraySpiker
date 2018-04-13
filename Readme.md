# arraySpiker v 1.0

## What does this script do?
Script ensures that any possible sample swaps are detected from Array CGH data and flagged for further investigation by Clinical Scientists. This is accomplished using a unique combination of 3 'spiked-in' probes which identify each sample. This App compares the detected 'spiked-in' probes to those expected on the sample sheet and raises a flag if there is a mismatch. Additionally the script throws an error if more or less than 3 probes are detected in a sample as this may indicate a sample switch, contamination, or that one or more spike in probes have failed.

Additionally the script has a number of functions which maybe useful when initially developing spike in protocols.  For example:
* Combinatorics function that calculates all unique trio combinations of x probes.
* Given a single feature extraction file and list of spike in probes a function that generates an in silico test set of files simulating real world data including cases where probes fail, array replicates fail, or where there is cross-contamination of samples.    

## What are typical use cases for this script?
The script is run during the analysis of Agilent CGH Array results.  It compares the expected prescence of spiked in probes to that detected, flagging any mismatch to the user.

## What data are required for this script to run?

## What does this script output?

## How does this script work?

## What are the limitations of this script

## This script was made by Viapath Genome Informatics


