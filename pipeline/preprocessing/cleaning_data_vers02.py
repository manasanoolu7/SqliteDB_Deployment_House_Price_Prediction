import pandas as pd
import numpy as np
import missingno as msno
import re

url = "https://raw.githubusercontent.com/adamflasse/dataCleaning/main/updated_1.csv"
df = pd.read_csv(url)


# Define functions for data preprocessing tasks

def general_clean(df):
    """Remove duplicates and unnecessary columns"""

    # Drop duplicates
    df.drop_duplicates(subset=['price', 'area', 'rooms_number'], inplace=True)

    # Delete postcode and house_is
    df.drop(
        [
            "postcode",
            "house_is",
            "region",
            'building_state',
            'swimming_pool_has'
        ],
        axis=1,
        inplace=True,
    )

    """Handling with Missing values"""

    # Replace Not Specified by np.nan
    df.replace("Not specified", np.nan, inplace=True)

    """Replace True and False by numerical values"""

    df.replace([True, "True", False, "False"], [1, 1, 0, 0], inplace=True)

    """Cleaning PRICE column: removing anomalies and outliers"""

    # Delete price rows with anomalies (extreme, mistaken values, e.g. 123456789)
    df.drop(df[df["price"] > 20000000].index, inplace=True)
    df.drop(df[df["price"] == 12345678].index, inplace=True)

    # Remove price outliers
    index_price = df[(df["price"] < 10000)].index
    df.drop(index_price, inplace=True)

    # Remove anomalies based on price and area features
    index_area_price = df[(df["area"] > 1000) & (df["price"] < 200000)].index
    df.drop(index_area_price, inplace=True)

    # Remove anomalies based on price and room features
    index_rooms_price = df[(df["rooms_number"] < 4) & (df["price"] > 1000000)].index
    df.drop(index_rooms_price, inplace=True)

    """Cleaning AREA column"""

    # Remove area outliers
    index_area = df[(df["area"] < 5)].index
    df.drop(index_area, inplace=True)

    """Cleaning ROOMS_NUMBER column"""

    # Replace room_number values that are == to area by NaN
    df.loc[(df.rooms_number == df.area), "rooms_number"] = np.nan

    """Cleaning PROPERTY_SUBTYPE column"""

    # Formatting values
    df["property_subtype"] = df["property_subtype"].str.lower()
    df["property_subtype"].replace(to_replace="-", value="_", regex=True, inplace=True)

    "Reduce property_subtype groups"

    # Reduce number of property_subtypes by grouping lower frequencied ones into "other" category
    # ("ground_floor" acted as threshold). This is done to reduce noise in the model
    df["property_subtype"] = df["property_subtype"].replace(
        [
            "exceptional_property",
            "flat_studio",
            "mansion",
            "town_house",
            "loft",
            "country_cottage",
            "service_flat",
            "bungalow",
            "farmhouse",
            "triplex",
            "other_property",
            "manor_house",
            "chalet",
            "castle",
            "kot",
            "penthouse",
            "duplex",
            "mixed_use_building",
            "villa",
            "apartment_block",
            "ground_floor"
        ],
        "OTHERS",
    )
    df["property_subtype"].replace({"apartment": "APARTMENT", "house": "HOUSE"}, inplace=True)

    # change column names with proper ones

    df = df.rename(
        columns={
            "property_subtype": "property_type",
            "kitchen_has": "equipped_kitchen",
            "facades_number": "facades_number",
            "rooms_number": "rooms_number",
        }
    )

    df.columns = df.columns.str.replace(' ', '')

    """Leave dataframe ready for next step"""
    # Reset index after dropping
    df = df.reset_index(drop=True)
    return df


def remove_na_all(df):
    # Remove all observations containing missing values
    df.dropna(axis=0, inplace=True)
    return df


def remove_nas_above30perc(df):
    # Remove observations containing more than 30% of missing values.
    # Missing values will be imputed
    df.dropna(axis=0, thresh=8, inplace=True)
    return df


def preprocessing(df):

    # Use sklearn libraries to create dummy variables to make one-hot encoder for our categorical values
    from sklearn.preprocessing import OneHotEncoder
    import category_encoders as ce

    ohe = ce.OneHotEncoder(handle_unknown="ignore", use_cat_names=True)
    df_ohe = ohe.fit_transform(df)
    return df_ohe


df = general_clean(df)
df = remove_nas_above30perc(df)
df = preprocessing(df)

# Impute missing values with means (remember that we have no observations with more than 2 missing values)

from sklearn.impute import SimpleImputer

imputer = SimpleImputer(missing_values=np.NaN, strategy="mean")

df["terrace"] = imputer.fit_transform(df["terrace"].values.reshape(-1, 1))[:, 0]
df["equipped_kitchen"] = imputer.fit_transform(
    df["equipped_kitchen"].values.reshape(-1, 1)
)[:, 0]
df["rooms_number"] = imputer.fit_transform(df["rooms_number"].values.reshape(-1, 1))[
                     :, 0
                     ]
df["garden"] = imputer.fit_transform(df["garden"].values.reshape(-1, 1))[:, 0]
df["furnished"] = imputer.fit_transform(df["furnished"].values.reshape(-1, 1))[:, 0]

# df.info()

processed_csv = df.to_csv("ready_to_model_df.csv")


# the function converts the portcode to province
def define_province(x):
    # x is zipcode of the property
    if ((x >= 1000) & (x < 1299)):
        return 'Brussels_Capital_Region'
    elif ((x >= 1300) & (x < 1499)):
        return 'Walloon_Brabant'
    elif (((x >= 1500) & (x < 1999)) | ((x >= 3000) & (x < 3499))):
        return 'Flemish_Brabant'
    elif ((x >= 2000) & (x < 2999)):
        return 'Antwerp'
    elif ((x >= 3500) & (x < 3999)):
        return 'Limburg'
    elif ((x >= 4000) & (x < 4999)):
        return 'Liège'
    elif ((x >= 5000) & (x < 5999)):
        return 'Namur'
    elif (((x >= 6000) & (x < 6599)) | ((x >= 7000) & (x < 7999))):
        return 'Hainaut'
    elif ((x >= 6600) & (x < 6999)):
        return 'Luxembourg'
    elif ((x >= 8000) & (x < 8999)):
        return 'West Flanders'
    elif ((x >= 9000) & (x < 9999)):
        return 'East Flanders'
    elif (x > 10000):
        return 'more'


def preprocess(new_house_df):
    # this fuction should take the input (new house info) 
    # and  return preprocessed input which is ready to make prediction in the model

    mandatory_columns = ['property_type_HOUSE', 'property_type_OTHERS',
                         'property_type_APARTMENT', 'rooms_number', 'area',
                         'province_Brussels_Capital_Region', 'province_Liège',
                         'province_Walloon_Brabant', 'province_West_Flanders',
                         'province_Flemish_Brabant', 'province_Luxembourg', 'province_Antwerp',
                         'province_East_Flanders', 'province_Hainaut', 'province_Limburg',
                         'province_Namur']
    mandatory = ["area", "property_type", "rooms_number", "zip_code"]
    for m in mandatory:

        if m not in new_house_df.columns:
            return "error"
    if new_house_df["property_type"].values[0] not in ["APARTMENT", "HOUSE", "OTHERS"]:

        return "error"
    if (new_house_df["zip_code"].values[0] >= 1000) and (new_house_df["zip_code"].values[0] < 9999):
        prop_province = define_province(new_house_df["zip_code"].values[0])
        new_house_df["province"] = prop_province
        new_house_df = new_house_df.drop(columns=["zip_code"])

        # deal with the columns (one-hot-encoder)
        new_house_df = preprocessing(new_house_df)
        #print(new_house_df.columns)
        for item in [item for item in mandatory_columns if item not in new_house_df.columns]:
            new_house_df[item] = 0

        new_house_df = new_house_df[mandatory_columns]
        new_house_df = new_house_df.filter(items=['property_type_HOUSE', 'property_type_OTHERS',
                                                  'property_type_APARTMENT', 'rooms_number', 'area',
                                                  'province_Brussels_Capital_Region', 'province_Liège',
                                                  'province_Walloon_Brabant', 'province_West_Flanders',
                                                  'province_Flemish_Brabant', 'province_Luxembourg', 'province_Antwerp',
                                                  'province_East_Flanders', 'province_Hainaut', 'province_Limburg',
                                                  'province_Namur'])
        #print(new_house_df)
        return new_house_df
    else:
        return "error"
