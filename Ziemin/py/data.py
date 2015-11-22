import numpy as np

column_names = [
        "user_id",
        "y",
        "first_week",
        "conv_count",
        "avg_conv_price",
        "first_day",
        "avg_conv_time",
        "views_count",
        "avg_view_price",
        "viewed_bought_count",
        "has_seen_ad",
        "country",
        "regist_day_of_year"
    ]

# reversed bindings
column_indexes = {column_names[i]:i for i in range(len(column_names))}

# currently used columns
curr_cols = [2,3,4,5,7,8,9,10,12]

# returns randomly shuffled features and results arrays in a consistent way
def shuffle(x_array, y_array):
    c = np.c_[x_array.reshape(len(x_array), -1), y_array.reshape(len(y_array), -1)]
    x_array2 = c[:, :x_array.size//len(x_array)].reshape(x_array.shape)
    y_array2 = c[:, x_array.size//len(x_array):].reshape(y_array.shape)

    np.random.shuffle(c)

    return x_array2, y_array2

# reads @features_csv file and saves:
# x_array.npy and y_array.npy files in out_dir
# usecols is a list of columns to be used as features
def prepare_input_files(features_csv, out_dir, usecols):

    x_array = np.loadtxt(features_csv, delimiter='|', usecols=usecols)
    y_array = np.loadtxt(features_csv, delimiter='|', usecols=[column_indexes["y"]])

    out_file_x = os.path.join(out_dir, "x_array")
    out_file_y = os.path.join(out_dir, "y_array")

    np.save(out_file_x, x_array)
    np.save(out_file_y, y_array)


# returns input arrays devided into two sets: training and test sets
# with size @ratio
# @return (x_train, y_train, x_test, y_test)
def devide(x_array, y_array, ratio):
    rows = len(x_array)
    train_rows = int(ratio * rows)

    x_train = x_array[:-train_rows]
    y_train = y_array[:-train_rows]
    x_test = x_array[train_rows:]
    y_test = y_array[train_rows:]

    return (x_train, y_train, x_test, y_test)
