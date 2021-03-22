from google.cloud import storage
import pandas as pd
import datetime
import json
import csv
import os
from io import BytesIO


PROJECT_ID = os.getenv("GCP_PROJECT")
PREFIX = "gs://"

time = datetime.datetime.now().strftime("%HH%MM%SS")

source_bucket_name = "raw-zone-bucket"
source_object_name = "agb.csv"

distination_bucket_name = "clean-zone-bucket"
distination_object_name = "Ingest:"+time


storage_client = storage.Client()

def extract()->pd.DataFrame:

    source_bucket = storage_client.bucket(source_bucket_name)
    source_object = source_bucket.blob(source_object_name)

    csv_content = source_object.download_as_string()

    print("here CSV content", csv_content)
    df = pd.read_csv(BytesIO(csv_content))

    print(df)
    return df


def transform(df:pd.DataFrame)->pd.DataFrame:
    df = df.nlargest(5, ['Temp'])
    return df

def load(df):

    distination_bucket = storage_client.bucket(distination_bucket_name)

    copyed_blob_name = distination_bucket.blob(distination_object_name).upload_from_string(df.to_csv(), 'text/csv')
    print(copyed_blob_name)



def copy_blobs_in_gcp_storage(source_bucket_name):

    """
    - get the blob from bucket and copy with new name in another bucket
    - we will use cloud schedule to trigger this function to copy the date
    - for example we want to trigger this function every minutes we will use corn [*****]
    """

    # extract file and convert in dataframe
    extracted_df = extract()

    # transform the df
    transformed_df = transform (extracted_df)

    # the function loads clean csv content as csv file in clean-zone-bucket
    load(transformed_df)


    return "Function executed sucessfully!"
