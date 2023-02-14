import pandas as pd
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
    df = pd.DataFrame(columns=['Room'] + columns)

    f = []
    for room in data:
        d = {i: 1 for i in room[1]}
        f.append(d)
        for i in columns:
            if i not in d:
                d[i] = 0

    for i in range(len(f)):
        room = pd.Series({'Room': data[i][0]})
        aps = pd.Series(f[i])
        df.loc[i] = pd.concat([room, aps])

    grouped_df = df.groupby(['Room'], axis=0, as_index=False).max()

    grouped_df.to_csv("ml_data.csv") # output data to csv
    return grouped_df


def get_unique_bssids(bssid_list):
    merged_list = []
    for i in bssid_list:
        merged_list += i

    return list(set(merged_list))


def get_bssid_list(room):
    room = [entry.split(';')[1] for entry in room if entry != '']
    return room


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
    imported_data = import_data("output_scan.csv")
    ml_data = transform_aplist(imported_data)

