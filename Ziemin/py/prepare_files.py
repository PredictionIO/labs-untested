#!/usr/bin/python

import numpy as np
import sys
import os

# features columns:
#  0: user_id
#  1: y
#  2: first_week
#  3: conv_count
#  4: avg_conv_price
#  5: first_day
#  6: avg_conv_time
#  7: views_count
#  8: avg_view_price
#  9: viewed_bought_count
# 10: has_seen_ad
# 11: country
# 12: regist_day_of_year

# Takes dumped features table csv file and the directory to return output:
# x_array.npy - array of features
# y_array.npy - array of results
if __name__ == "__main__":
    in_file = sys.argv[1]
    out_dir = sys.argv[2]
    # choosing used features
    # no avg_conv_time for now
    x_array = np.loadtxt(in_file, delimiter='|', usecols=[2,3,4,5,7,8,9,10,12])
    y_array = np.loadtxt(in_file, delimiter='|', usecols=[1])

    out_file_x = os.path.join(out_dir, "x_array")
    out_file_y = os.path.join(out_dir, "y_array")

    np.save(out_file_x, x_array)
    np.save(out_file_y, y_array)
