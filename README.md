# SqliteDB_Deployment_House_Price_Prediction
House Prediction using SQLite Database with Heroku Deployment

## Introduction

A real estate company 'ImmoEliza' wants a Machine Learning model to make predictions on the Belgium's real estate price. Therefore, we have to create a database to store the data of ImmoEliza site by scraping and process the data to predict the price. 

## Mission

We have to scape 'Immoeliza' real estate site to get required data and process it by cleaning, analysing and modeling. We also have to create an API (Application Programming Interface') to connect our application with the cloud to make use of it to know the predictions of the sales in Belgium. API generally used to take new input data and return the price. We have used DOCKER to wrap the API and deployeed by HEROKU.

### The input:
```json
{
    "area": int,
    "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms-number": int,
    "zip-code": int,
    "garden": Optional[bool],
    "equipped-kitchen": Optional[bool],
    "furnished": Opional[bool],
    "terrace": Optional[bool],
    "facades-number": Optional[int]
}
```

Area, property-type, rooms-number and zip-code are required(mandatory) in order to run the application

### The output:
if data is provided correctly:
```json
{
    "prediction": [float],
}
```
if data is not provided correctly:
```json
{
    "error": Optional[str]
}
```


### File structure:

    .
    ├── ...
    ├── docker                    
    │   ├── Dockerfile                           
    ├── pipeline   
    |   ├── database
    |       ├── csv_to_SQLite_conversion_01.py
    |       ├── csv_to_SQLite_conversion_02.py
    |       ├── DB_creation_csv_loading_01.py
    |       ├── immo_data.db
    │   ├── model
    │       ├── model.py
    │       ├── model.pkl
    |       ├── immo
    |       ├── immo_data.db
    |       ├── model_db.pkl
    │       ├── ready_to_model_df.csv
    │   ├── predict
    │       ├── prediction.py
    │   ├── preprocessing 
    │       ├── cleaning_data_vers02.py
    |       ├── ready_to_model_df.csv
    │       │── test-dataframe.csv
    ├── Procfile
    ├── app.py
    ├── docker-compose.yaml
    ├── requirements.txt
    ├── README.md
    


## Docker File

#### image creation
docker build -f docker/Dockerfile . -t image_name:tag_name

#### docker run
docker run -it image_name:tag_name


## Heroku 

### Run
You can access the application on this [Link](https://sqlite-api.herokuapp.com/).
- Home: "/"
- Predict page: "/predict":
* GET: Returns the data format you need to input
* POST: Returns the predicted price or error message in case of error

To run it on your local machine:
- Clone the project
- Install the requirements for this project by running:
```bash
pip install -r requirements.txt
```
- Then run file:
```bash
app.py
```
- Test it using [Postman](https://www.postman.com/)

