import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import itertools


# import file data into a pandas dataframe
def import_data(filename):
    # due to aplist being separated by commas, chosen delimiter is '|'
    data = pd.read_csv(filename, sep='|')
    return data


# function to parse unique bssids in each scan
def transform_aplist(df):
    location = df['Location']
    ap_list = df['AP List'].values.tolist()

    connection_points = []
    for i in ap_list:
        test = i.split("interface name: wlan0") # access points list is structured a bit strange
        test = [i.split(',') for i in test if "eduroam" in i or "DCU-Guest-WiFi" in i]

        i = 0
        while i < len(test):
            test[i] = [p.strip(' BSSID: ') for p in test[i] if "BSSID" in p]
            i += 1

        test = [i[0] for i in test]

        connection_points.append(test)

    concat_results(location, connection_points)


# squash everything together
def concat_results(loc, connections):
    loc_set = list(set(loc))
    loc_set = [[i] for i in loc_set]

    zipped = list(zip(loc, connections))

    # nested for loop action
    for room in loc_set:
        for i in zipped:
            if i[0] == room[0]:
                room.append(i[1])

    final = []

    # merge the mul
    for i in loc_set:
        final.append(list(set(list(itertools.chain.from_iterable(i[1:])))))

    dataframe_prep(loc_set, final)


# convert transformed data to dataframe?
def dataframe_prep(l, f):
    # room column
    # column for each access point


    pass


def make_prediction(data):
    df = pd.read_csv('labs_dummy.csv', index_col=0)
    print("csv read...")

    df_dropped = df.drop('LOCATION', axis=1)

    scaler = StandardScaler()
    scaler.fit(df_dropped)
    scaled_features = scaler.transform(df_dropped)

    df_feat = pd.DataFrame(scaled_features, columns=df.columns[:-1])

    print("train test split....")
    X = df_feat
    y = df['LOCATION']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=191)

    print("knn...")
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    predictions = knn.predict(X_test)

    print(predictions)


if __name__ == "__main__":
    # make_prediction()
    data = import_data("output_scan.csv")
    transform_aplist(data)
