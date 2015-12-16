#!/usr/bin/python

import numpy as np
import sys
import os
from data import *

# Arguments
# in_dir
# out_dir
if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    features_csv = os.path.join(in_dir, "categorical_features.csv")
    utm_medium = os.path.join(in_dir, "utm_medium_pca.npy")
    utm_source = os.path.join(in_dir, "utm_source_pca.npy")
    user_items = os.path.join(in_dir, "user_items_pca.npy")

    concatenate_features(features_csv, [utm_medium, utm_source], user_items, out_dir)
