import pandas as pd
import numpy as np

from pipeline.database.DB_creation_csv_loading_01 import read_immo_table, load_csv_df

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
    RidgeCV,
    LassoCV,
    ElasticNetCV,
)
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score

import pickle

## CALL THE TABLE FROM THE DATABASE ##
db_data = load_csv_df()

df_HELP = read_immo_table()
# print(df_HELP)
df = pd.DataFrame(df_HELP)

df_mandatory = df.filter(items=['property_type_HOUSE', 'property_type_OTHERS',
                                'property_type_APARTMENT', 'rooms_number', 'area',
                                'province_Brussels_Capital_Region', 'province_Liège', "price",
                                'province_Walloon_Brabant', 'province_West_Flanders',
                                'province_Flemish_Brabant', 'province_Luxembourg', 'province_Antwerp',
                                'province_East_Flanders', 'province_Hainaut', 'province_Limburg',
                                'province_Namur'])

X = df_mandatory.drop("price", axis=1)
y = df_mandatory["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=41, test_size=0.2)

regressor = LinearRegression()
regressor.fit(X_train, y_train)
pickle.dump(regressor, open('pipeline//model//model_db.pkl', 'wb'))
