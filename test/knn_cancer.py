import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
from KNN import Knn, KnnClassifier
from sklearn.metrics import accuracy_score

#RUN

#metodo per prepare i dati
def prep():
    data = 'data/cancer.txt'

    df = pd.read_csv(data, header=None)

    col_names = ['Id', 'Clump_thickness', 'Uniformity_Cell_Size', 'Uniformity_Cell_Shape', 'Marginal_Adhesion', 
                'Single_Epithelial_Cell_Size', 'Bare_Nuclei', 'Bland_Chromatin', 'Normal_Nucleoli', 'Mitoses', 'Class']

    df.columns = col_names

    # converto
    df['Bare_Nuclei'] = pd.to_numeric(df['Bare_Nuclei'], errors='coerce')

    df = df.drop(['Id'], axis=1)
    X = df.drop(['Class'], axis=1)

    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


    #Cambio in NULL con valori presi dalla mediana della colonna
    for df1 in [X_train, X_test]:
        for col in X_train.columns:
            col_median=X_train[col].median()
            df1[col].fillna(col_median, inplace=True)

    X_train = X_train.to_numpy()
    X_test=X_test.to_numpy()
    y_train=y_train.to_numpy()
    y_test=y_test.to_numpy()

    return X_train, X_test, y_train, y_test

#########################################################################################
X_train, X_test, y_train, y_test = prep()       
engine = create_engine("postgresql://postgres:0698@localhost:5432/classification")
c = KnnClassifier(3)
c.clear(engine)
c.fit(X_train, y_train,engine)
a=c.predict(X_test, engine)
accuracy = accuracy_score(y_test, a) 
print('VEC accuracy: ',accuracy)
#########################################################################################
engine = create_engine("postgresql://postgres:0698@localhost:5432/classification")
c = Knn(3)
c.clear(engine)
c.fit(X_train, y_train, engine)
a=c.predict(X_test, engine)
accuracy = accuracy_score(y_test, a) 
print('COO accuracy: ',accuracy)
#########################################################################################
from sklearn.neighbors import KNeighborsClassifier
c = KNeighborsClassifier(3)
c.fit(X_train, y_train)
a=c.predict(X_test)
accuracy = accuracy_score(y_test, a) 
print('scikit-learn accuracy: ',accuracy)