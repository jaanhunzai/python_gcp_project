import requests
from datetime import datetime
import os
import sys
from google.cloud import bigquery
import json

PROJECT_ID = os.getenv("GCP_PROJECT")
print(PROJECT_ID)
BQ_DATASET = "test_dataset"
BQ_TABLE =  "test_users"
#mgr-application:test_dataset.test_users
BQ = bigquery.Client()
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/jaanhunzai_512/google_key.json"

headers = {}
params = {'limit': '10'}



def pull_users(baseURL, endpoint):
    o_response = requests.get(baseURL + endpoint, headers=headers, params=params)
    #print(o_response)
    return (o_response.json())


def parse_user_to_rows(users_json):
    user_as_table_rows = []
    for user in users_json[:5]:
        user_as_table_rows.append({"user_id": user["id"], "userName": user["name"], "email": user["email"]})
    return user_as_table_rows


def insert_in_biqquery_table(rows):
    table = BQ.dataset(BQ_DATASET).table(BQ_TABLE)
    print("table:", table)

    errors = BQ.insert_rows_json(table, rows)

    if errors != []:
        raise BigQueryError(errors)



def steaming_data (request):
    base_url = 'http://jsonplaceholder.typicode.com/'
    endpoints = 'users'
    try:
        jsonUsers = pull_users(base_url, endpoints)
        #print("jsonUsers....:", jsonUsers)
    except Exception:
        "Problem in Getting data from API"

    try:
        cleaned_user_data = parse_user_to_rows(jsonUsers)
        print("cleaned_user_data...", cleaned_user_data)
    except Exception:
        "Problem in Parsing RECORDS"

    try:
        insert_in_biqquery_table(cleaned_user_data)
    except Exception:
        print("Problem with BQ")
    return "Done"

class BigQueryError(Exception):
    '''Exception raised whenever a BigQuery error happened'''

    def __init__(self, errors):
        super().__init__(self._format(errors))
        self.errors = errors

    def _format(self, errors):
        err = []
        for error in errors:
            err.extend(error['errors'])
        return json.dumps(err)