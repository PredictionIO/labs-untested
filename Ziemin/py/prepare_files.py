#!/usr/bin/python

import numpy as np
import sys
import os
from data import *

# Takes dumped features table csv file and the directory to return output:
# x_array.npy - array of features
# y_array.npy - array of results
if __name__ == "__main__":
    in_file = sys.argv[1]
    out_dir = sys.argv[2]
    # prepare_input_files(in_file, out_dir, curr_cols)
    # prepare_items_features(in_file, out_dir)
    # prepare_categorical_features(in_file, out_dir)
    reduce_data(in_file, out_dir)

    ## reduce user_items
    # reduce_data(in_file, out_dir, first_column=False)
