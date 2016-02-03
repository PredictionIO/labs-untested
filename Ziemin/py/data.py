import os
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.decomposition import PCA, TruncatedSVD, IncrementalPCA, RandomizedPCA

# these is the odering of the columns or groups of columns in relevant features 
# table from SQL database
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
        "country",      # a string
        "regist_day_of_year"
        "utm_source",   # many 0,1 columns
        "utm_campaign", # many 0,1 columns
        "utm_medium",   # many 0,1 columns
        "utm_content"   # many 0,1 columns
    ]

# reversed bindings
column_indexes = {column_names[i]:i for i in range(len(column_names))}

# currently used columns
curr_cols = [2,3,4,5,7,8,9,10,12]
curr_index = {column_names[curr_cols[i]]:i for i in range(len(curr_cols))}

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

# prepares one hot encoded features for some column from features SQL table
# columns: country, utm_source, utm_medium
# assumes that input file is sorted by user_id
def prepare_categorical_features(features_csv, out_dir):
    # currently in encodes utm_medium
    # modify usecols and output path name to one_hot_encode different column
    array = np.loadtxt(features_csv, delimiter='|', usecols=[15], dtype=np.str_)

    le = LabelEncoder()
    col = le.fit_transform(array.T)
    columns = np.array([col]).T

    enc = OneHotEncoder()
    encoded = enc.fit_transform(columns).toarray()
    np.save(os.path.join(out_dir, "utm_medium"), encoded)
    print(encoded.shape)

# reads npy array, reduces its dimensions with SVD/PCA and saves it to the destination
def reduce_data(features, out_dir, dim=10, first_column=True):
    array = np.load(features)
    subarray = array
    if not first_column:
        subarray = array[:, 1:]

    ipca = IncrementalPCA(n_components=dim, copy=False, batch_size=500000)
    ipca.fit_transform(subarray)
    new_array = subarray
    # when it cannot fit into memory do it incrementally like below
    # new_array_1 = tsvd.fit_transform(subarray[:1500000, :])
    # new_array_2 = tsvd.fit_transform(subarray[1500000:3400000, :])
    # new_array_3 = tsvd.fit_transform(subarray[3400000:, :])
    # new_array = np.vstack([new_array_1, new_array_2, new_array_3])
    if not first_column:
        new_array = np.c_[array[:, 0], new_array]

    assert new_array.shape[0] == array.shape[0]
    np.save(os.path.join(out_dir, os.path.basename(features) + "_pca"), new_array)


# prepares one hot encoded features related to items user bought
# columns: user_id, personality, style, theme, category
def prepare_items_features(user_items_csv, out_dir):
    array = np.loadtxt(user_items_csv, delimiter='|',
            dtype=np.dtype(np.uint64))

    le = LabelEncoder()
    col1 = le.fit_transform(array[:, 1].T)
    col2 = le.fit_transform(array[:, 2].T)
    col3 = le.fit_transform(array[:, 3].T)
    col4 = le.fit_transform(array[:, 4].T)

    columns = np.array([col1, col2, col3, col4]).T
    enc = OneHotEncoder()
    print(array[:10])
    encoded = np.c_[array[:, 0], enc.fit_transform(columns).toarray()]
    print(encoded[:10])
    print(encoded.shape)

    user_id = encoded[0][0]
    rows = []
    current = np.zeros(encoded.shape[1]-1)
    for i in range(encoded.shape[0]):
        if encoded[i][0] != user_id:
            rows.append(np.concatenate([[user_id], current]))
            user_id = encoded[i][0]
            current = np.zeros(encoded.shape[1]-1)
        else:
            current = np.sum([current, encoded[i, 1:]], axis=0)
    rows.append(np.concatenate([[user_id], current]))

    array = np.array(rows)
    print(array.shape)

    # let's serialize array
    np.save(os.path.join(out_dir, "user_items"), array)


# this function creates X array from:
# - the original features.csv files
# - an array of # *.npy arrays (features_npy) - reduced binary features to lower dimension
# - user_items.npy array as created above
# Then it concatenates all the features and serializes the array to out_dir
def concatenate_features(features_csv, features_npys, user_items_npy, out_dir):
    x_array = np.loadtxt(features_csv, delimiter='|', usecols=[0]+curr_cols)
    for f in features_npys:
        arr = np.load(f)
        assert arr.shape[0] == x_array.shape[0]
        x_array = np.c_[x_array, arr]

    # now concatenate user items
    # this array is longer, therefore we have to add dummy vector for every
    # nonexistent user in this array
    user_items = np.load(user_items_npy)
    width = user_items.shape[1] - 1
    u_it = 0
    items_array = []
    for i in range(x_array.shape[0]):
        if u_it >= user_items.shape[0] or x_array[i, 0] != user_items[u_it, 0]:
            items_array.append(np.zeros(width))
        else:
            items_array.append(user_items[u_it, 1:])
            u_it += 1

    assert u_it == user_items.shape[0]
    items_array = np.array(items_array)

    x_array = np.c_[x_array[:, 1:], items_array]
    print(x_array.shape)
    # save without user_id column
    np.save(os.path.join(out_dir, "X"), x_array)

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
