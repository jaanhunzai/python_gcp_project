import pandas as pd
import pandas_gbq
import os
import json

PROJECT_ID = os.getenv("GCP_PROJECT")
print(PROJECT_ID)
BQ_DATASET = "test_dataset"
BQ_TABLE = "bitCoinData2020"


# params = {}


def extract(baseURL: str) -> pd.DataFrame:
    """
    - the function extract data from given baseURL
    - convert the json data into pandas dataframe
    - for simplicity, i picked only top 5 records as DF
    :param baseURL:
    :return: df
    """
    df = pd.read_json(baseURL)
    # print(df.head(5))
    return df.head(5)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    - function transform the extracted data from baseURL. The following transformation has been made on the dataset:
    - Changes the data type from object to datetime64 for columns which represent date and time such ** time_period_start *, * time_period_end ** etc.
    - Standard deviation is comouted for the price columns to get insight about variation of prices for the certain period of time
    - The computed standard deviation is added as column price_volatility_std*
    - The day_of_week, month and year have been extracted from time_period_start column and columns are added to data frame. These columns are import for data analysis based on day, month, or year. Data scientist can can group_by data using month to get insight about price_volatility_std monthlywise or daywise.
    :param df:
    :return: df
    """
    # Change the following columns data type to datetime
    df["time_period_start"] = pd.to_datetime(df["time_period_start"])
    df["time_period_end"] = pd.to_datetime(df["time_period_end"])
    df["time_open"] = pd.to_datetime(df["time_open"])
    df["time_close"] = pd.to_datetime(df["time_close"])

    # compute standard deviation from price columns
    df["price_volatility_std"] = df[["price_open", "price_high", "price_low", "price_close"]].std(axis=1,

                                                                                                skipna=True)
    #extract day,month and year from column and added as new columns
    df['month'] = df['time_period_start'].dt.month
    df['day_of_week'] = df['time_period_start'].dt.day
    df['year'] = df['time_period_start'].dt.year

    return df


def load_into_BQ(df: pd.DataFrame):
    """
    - The function loads the transformed data frame in the BigQuery table. The function requires pandas_gbq package and the following parameters:
    - PROJECT_ID = os.getenv("GCP_PROJECT")
    - BQ_TABLE = "test_dataset.bitCoinData2020"
    :param df:
    :return:
    """

    errors = pandas_gbq.to_gbq(df, destination_table=BQ_DATASET + "." + BQ_TABLE,
                               project_id=PROJECT_ID,
                               if_exists="fail"

                               )
    print("errors", errors)
    if errors != None:
        raise BigQueryTableError(errors)


def cloud_function_entry_point(request):
    """
    - Function cloud_function_entry_point is an entry-point in the cloud function
    - deploy the code as a cloud function
    :param baseURL:
    :return:
    """

    baseURL = "http://cf-code-challenge-40ziu6ep60m9.s3-website.eu-central-1.amazonaws.com/ohlcv-btc-usd-history-6min-2020.json"
    try:
        df = extract(baseURL)
    except:
        print("problem in extracting data as dataframe")

    try:
        df_transformed = transform(df)
    except:
        print("problem in tranforming data")

    try:
        load_into_BQ(df_transformed)

    except:
        print("problem in loading data to BigQuery Table")
    return "Process Completed!"


class BigQueryTableError(Exception):
    '''Exception raised whenever a BigQuery table gives error'''

    def __init__(self, errors):
        super().__init__(self._format(errors))
        self.errors = errors

    def _format(self, errors):
        err = []
        for error in errors:
            err.extend(error['errors'])
        return json.dumps(err)
