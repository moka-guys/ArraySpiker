from __future__ import print_function

"""Helper functions which reads and writes data from the MOKA LIMS for use with array_spiker.py"""

import sqlalchemy


def get_well_ids():
    """TODO Get IDs for the 3 spiked in probes assigned to each well from MOKA table ArrayLabelledDNA"""
    # Pseudocode - get ArrayLabelledDNA.code
    pass


def get_fe_file_name():
    """TODO Get & construct the FE extraction file name from ArrayID & Subarray fields in Moka table ArrayLabelling"""
    # Pseudocode - get ArrayLabelling.ArrayID, get ArrayLabelling.Subarray
    # Use create_sample_name() to construct FE file name
    pass


def write_results_to_moka():
    """TODO Write results to relevant fields in the Moka table ArrayLabelling"""
    # Pseudocode - upload results to ArrayLabelling
    pass


def subarray_id_translator(ref_string, direction=0):
    """
    Translates a subarray ID string between formats used in MOKA and Feature Extraction Filenames.
    By default function translates a subarray position from the format used in MOKA into that used to name the FE file.
    This allows the matching FE file to be imported for each record in MOKA.

        Col   C1      C2
    Row       ___________    __________
    R1      | 1       5 |   | 1_1   2_1 | Mapping the subarray positions between MOKA and the FE file.
    R2      | 2       6 |   | 1_2   2_2 | MOKA uses a sequential numbering system for the 8 arrays
    R3      | 3       7 | = | 1_3   2_3 | present on a slide, while the FE file name uses the  Column
    R4      | 4       8 |   | 1_4   2_4 | No. + the row number delimited by a _ .
             ___________     ___________
                Moka           FE File

    Direction    0    ----------->        To calculate Col_Row format position from a 1-8 sequential
                 1    <-----------        position set direction to 0, to reverse direction use 1.
    """
    subarray_id = None
    # Define dictionary to map the array position between MOKA and the feature extraction file formats:
    subarray_dict = {1: '1_1', 2: '1_2', 3: '1_3', 4: '1_4', 5: '2_1', 6: '2_2', 7: '2_3', 8: '2_4'}
    if direction == 0:
        # Return subarray position in FE file format from MOKA format
        subarray_id = subarray_dict[ref_string]
    elif direction == 1:
        # Return subarray position in MOKA format from FE format
        subarray_id = subarray_dict.keys()[subarray_dict.values().index(ref_string)]
    else:
        print("Unexpected input %s used as 'direction' in function mappArrayPosition - Use 0 or 1" % str(direction))
    return subarray_id


def create_sample_filename(dna_id, moka_subarray_id):
    """Generate the Feature Extraction file name from moka data fields"""
    subarray_id = subarray_id_translator(moka_subarray_id)  # Translate the subarray format-See subarray_id_translator()
    sample_name = "%s_S01_Guys121919_CGH_1100_Jul11_2_%s.txt" % (dna_id, subarray_id)
    # TODO specify "_S01_Guys121919_CGH_1100_Jul11_2_" in a config file to make it easier to change
    return sample_name

