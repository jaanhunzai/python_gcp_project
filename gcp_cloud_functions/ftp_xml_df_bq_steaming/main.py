from lxml import etree
from google.cloud import storage
import pandas as pd
import pandas_gbq
import os
import json

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/jaanhunzai_512/google_key2.json"
PROJECT_ID = os.getenv("GCP_PROJECT")
print("project ID:",PROJECT_ID)

source_bucket_name = "raw-zone-bucket"
source_object_name = "simple_set.xml"

BQ_DATASET = "test_dataset"
BQ_TABLE = "patentDocument"


storage_client = storage.Client()

def parse_classification_ipcr(exch_classifications_ipcr: str) -> list:
    """
    - function parses the classification_ipcr tag
    - under "exch:classifications-ipcr" tag there are multiple tags for text
    - for example:
    - <exch:classifications-ipcr>
	- 	<classification-ipcr sequence="1"><text>B01D  15/04        20060101AFI20051220RMJP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="2"><text>B01J  39/18        20170101AFI20200529BHEP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="3"><text>B01D  15/08        20060101ALI20051220RMJP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="4"><text>B01J  20/281       20060101ALI20051220RMJP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="5"><text>B01J  20/32        20060101ALI20200529BHEP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="6"><text>B01J  39/04        20170101ALI20200529BHEP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="7"><text>B01J  39/08        20060101ALI20051220RMJP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="8"><text>B01J  49/00        20060101ALI20051220RMJP        </text></classification-ipcr>
	- 	<classification-ipcr sequence="9"><text>C07K   1/18        20060101ALI20051220RMJP        </text></classification-ipcr>
    - </exch:classifications-ipcr>

    - I used list to store all the extracted  text from the tag
    - returns list
    :param exch_classifications_ipcr:
    :return:
    """
    class_ipcr_text = []

    for class_ipcr in exch_classifications_ipcr:
        # print(class_ipcr.tag, class_ipcr.attrib)
        for class_ipcr_sequance in class_ipcr:
            class_ipcr_text.append(class_ipcr_sequance[0].text)

    return class_ipcr_text


def parse_applicants_name(exch_applicant_tag: str) -> list:
    """
    - function parses applicants
    - there are multiple applicants for each document , therefore, i used list to store all applicants
    -<exch:applicants>
			<exch:applicant sequence="1" data-format="docdb">
				<exch:applicant-name><name>CYTIVA BIOPROCESS R&amp;D AB</name></exch:applicant-name>
				<residence><country>SE</country></residence>
			</exch:applicant>

			<exch:applicant sequence="1" data-format="docdba">
					<exch:applicant-name><name>Cytiva BioProcess R&amp;D AB</name></exch:applicant-name>
			</exch:applicant>
	- </exch:applicants>
    - returns list
    :param exch_applicant_tag:
    :return:
    """
    applicant_name = exch_applicant_tag[0][0][0].text
    return applicant_name


def parse_invention_title(exch_invention_title_tag: str) -> str:
    """
    - function returns title written in English
    - <exch:invention-title lang="de" data-format="docdba">ADSORPTIONSVERFAHREN UND LIGANDEN</exch:invention-title>
    - <exch:invention-title lang="en" data-format="docdba">ADSORPTION METHOD AND LIGANDS</exch:invention-title>
    - <exch:invention-title lang="fr" data-format="docdba">PROCEDE D&apos;ADSORPTION ET LIGANDS</exch:invention-title>
    -
    :param exch_invention_title_tag:
    :return:
    """

    for title in exch_invention_title_tag:
        if title.attrib['lang'] == "en":
            return title.text
    return title.text


def parse_abstract(exch_abstract_tag: str) -> str:
    """
    - function extracts abstract
    :param exch_abstract_tag:
    :return:
    """
    for abstracts in exch_abstract_tag:
        return abstracts[0].text


def merge_duplicated_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    - the function takes df as an argument and merges the duplicated record
    - groups by "family_id" and merges if records are duplicated
    - return unique records as new data frame
    :param df:
    :return:
    """
    aggreDict = {'doc-identifier': 'first',
                 'country': 'first',
                 'country': 'first',
                 'doc-number': 'first',
                 'kind': 'first',
                 'doc-id': 'first',
                 'date-publ': 'first',
                 'family-id': 'first',
                 'classification-ipcr': 'sum',
                 'exch:applicant-name': 'first',
                 "exch:invention-title": "first",
                 "exch:abstract": "first"

                 }
    df_new = df.groupby('family-id', as_index=False).aggregate(aggreDict).reindex(columns=df.columns)
    return df_new


def extract(path) -> str:
    """
    - the function extract give XML from source
    - the source can be cloud storage bucket or FTP
    - parse the file and creates xml data
    - it returns root element
    :param path:
    :return:
    """
    source_bucket = storage_client.bucket(source_bucket_name)

    source_object = source_bucket.blob(source_object_name)

    xml_bytes = source_object.download_as_string()
    root_element = etree.fromstring(xml_bytes)

    return root_element


def transform(root_element: str) -> pd.DataFrame:
    """
    - function parses child tags in the XML document
    - extract values
    - create dataframe, it also create new column by combining three columns kind, country, doc-number columns
    - checks for repeated documents and aggreggates document where family-id are repeated
    - return cleaned dataframe
    :param root_element:
    :return:
    """

    df_cols = ["country", "doc_number", "kind", "doc_id", "date_publ", "family_id", "classification_ipcr",
               "exch_applicant_name", "exch_invention_title", "exch_abstract"]

    namespace = {"exch": 'http://www.epo.org/exchange'}

    records = []

    for i in range(0, 5):  # len(root.getchildren())
        # print(root_element.getchildren()[i])
        child = root_element.getchildren()[i]
        country = child.attrib["country"]
        doc_number = child.attrib["doc-number"]
        kind = child.attrib["kind"]
        doc_id = child.attrib["doc-id"]
        date_publ = child.attrib["date-publ"]
        # print(date_publ)
        family_id = child.attrib["family-id"]

        # extract classifications_ipcr text
        exch_classifications_ipcr_tag = child.findall('.//exch:classifications-ipcr', namespace)
        class_ipcr_text = parse_classification_ipcr(exch_classifications_ipcr_tag)

        # extract applicants name
        exch_applicant_tag = child.findall('.//exch:applicant', namespace)
        applicant_name = parse_applicants_name(exch_applicant_tag)

        # extract invention title
        exch_invention_title_tag = child.findall('.//exch:invention-title', namespace)
        invention_title = parse_invention_title(exch_invention_title_tag)

        # extract document abstract
        exch_abstract_tag = child.findall('.//exch:abstract', namespace)
        abstract = parse_abstract(exch_abstract_tag)

        records.append(
            {
                "country": country,
                "doc_number": doc_number,
                "kind": kind,
                "doc_id": doc_id,
                "date_publ": date_publ,
                "family_id": family_id,
                "classification_ipcr": class_ipcr_text,
                "exch_applicant_name": applicant_name,
                "exch_invention_title": invention_title,
                "exch_abstract": abstract
            }
        )

    df = pd.DataFrame(records, columns=df_cols)

    # create new document identifier by combining colums
    doc_identifier = df["country"] + df["doc_number"] + df["kind"]
    df.insert(0, "doc_identifier", doc_identifier)

    # check for duplicated documents
    if df['family_id'].eq(df['family_id'].iloc[0]).all() == True:
        df_new = merge_duplicated_records(df)  # function aggreggates duplicated documents
    else:
        df_new = df.copy()

    return df_new


def load_into_BQ(df: pd.DataFrame):
    """
    - The function loads the transformed data frame in the BigQuery table. The function requires pandas_gbq package and the following parameters:
    - PROJECT_ID = os.getenv("GCP_PROJECT")
    - BQ_TABLE = "test_dataset.dataset"
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
    - cloud_function_entry_point is an entry-point in the cloud function
    - deploy the code as a cloud function
    :param file_path:
    :return:
    """

    file_path = "simple_set.xml"

    try:
       xml_elements = extract(file_path)
       print(xml_elements)
    except:
       print("problem in extracting data from given data source")

    try:
        df_cleaned = transform(xml_elements)
        print(df_cleaned)
    except:
        print("problem in parsing xml ")

    try:
        load_into_BQ(df_cleaned)

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
