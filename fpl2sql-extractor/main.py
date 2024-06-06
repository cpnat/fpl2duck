import argparse
import logging
import os
import sys

import boto3
import duckdb

from extractors.bootstrap_extractor import get_bootstrap_tables
from extractors.element_summary_extractor import get_element_summary_table
from extractors.fixtures_extractor import get_fixtures_table
from extractors.utils import pydantic_records_to_arrow_table


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def extract_data() -> None:
    bootstrap_tables_dict = get_bootstrap_tables()
    fixtures_table_dict = get_fixtures_table()
    element_summary_dict = get_element_summary_table()
    tables = {**bootstrap_tables_dict, **fixtures_table_dict, **element_summary_dict}

    logger.info("Creating a database connection")
    conn = duckdb.connect(database="fpl2duck.db", read_only=False)

    for table_name, records in tables.items():
        logger.info(f"Creating table: {table_name}")

        # Convert Pydantic records to Arrow table
        table = pydantic_records_to_arrow_table(records)

        # Register the table
        conn.register(table_name, table)

        # Execute SQL statement to create the table
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM {table_name}")

    conn.execute("EXPORT DATABASE 'db_export' (FORMAT PARQUET);")

    logger.info("Closing the connection")
    conn.close()


def query_data() -> None:
    logger.info("Creating a database connection")
    conn = duckdb.connect(database="fpl2duck.db", read_only=True)

    logger.info("Querying the database")

    logger.info("Closing the connection")
    conn.close()


def upload_data() -> None:
    """
    Upload data to the cloud storage
    """

    client_secret = os.getenv("CLIENT_SECRET")
    client_id = os.getenv("CLIENT_ID")
    endpoint_url = os.getenv("ENDPOINT_URL")
    bucket_name = os.getenv("BUCKET_NAME")

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=client_id,
        aws_secret_access_key=client_secret,
    )

    for file in os.listdir("db_export"):
        s3_client.upload_file(
            f"db_export/{file}", bucket_name, f"db_export/{file}"
        )

    logger.info("Data uploaded to the cloud storage")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true", help="Create a database and load data")
    parser.add_argument("--upload", action="store_true", help="Upload data to S3 storage")
    parser.add_argument("--query", action="store_true", help="Query data from the database")
    args = parser.parse_args()

    num_flags = sum([args.extract, args.upload, args.query])
    if num_flags == 0:
        logger.info("Please provide a flag to either extract, upload or query the data")
        sys.exit()
    if num_flags > 1:
        logger.info("Please provide only one flag to either extract, upload or query the data")
        sys.exit()

    if args.extract:
        extract_data()
    if args.upload:
        upload_data()
    if args.query:
        query_data()
