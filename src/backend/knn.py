import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

print("modules imported successfully...")

def make_prediction():
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
    make_prediction()
