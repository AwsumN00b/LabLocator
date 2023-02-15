import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# import file data into a pandas dataframe
def import_data(filename):
    data = pd.read_csv(filename)
    return data


# function to parse unique bssids in each scan
def transform_aplist(data):
    locations = data['Location']
    ap_list = data['AP List'].values.tolist()

    ap_list_split = [i.split('|') for i in ap_list]

    bssid_list = []
    for room in ap_list_split:
        bssid_list.append(get_bssid_list(room))

    bssid_columns = get_unique_bssids(bssid_list)

    zipped_data = list(zip(locations, bssid_list))

    return create_dataframe(zipped_data, bssid_columns)


def create_dataframe(data, columns):

    ap_visibility = []
    for room in data:
        ap_dict = {access_point: 1 for access_point in room[1]}
        ap_visibility.append(ap_dict)

        for access_point in columns:
            if access_point not in ap_dict:
                ap_dict[access_point] = 0

    d = []
    # compile rooms and visible access points to dataframe
    for i in range(len(ap_visibility)):
        room = pd.Series({'Room': data[i][0]})
        aps = pd.Series(ap_visibility[i])
        d.append(pd.concat([room, aps]))

    df = pd.DataFrame(d, columns=['Room'] + columns)

    df.to_csv("ml_data.csv")    # output data to csv -- for testing

    return df


def get_unique_bssids(bssid_list):
    merged_list = []
    for i in bssid_list:
        merged_list += i

    return list(set(merged_list))


def get_bssid_list(room):
    room = [entry.split(';')[1] for entry in room if entry != '']
    return room


def knn_prediction(data):
    data_dropped = data.drop('Room', axis=1)

    df_feat = pd.DataFrame(data_dropped, columns=data.columns[1:])

    X = df_feat
    y = data['Room']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=139)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    return knn


def predict_scan(model):
    data = pd.read_csv("ml_data.csv")
    data = data.drop('Room', axis=1).loc[0]

    # print(data)
    # data =

    # p = model.predict(data)


if __name__ == "__main__":
    imported_data = import_data("output_scan.csv")
    ml_data = transform_aplist(imported_data)

    model = knn_prediction(ml_data)
    predict_scan(model)
