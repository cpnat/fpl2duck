import argparse
import logging

import duckdb

from extractors.bootstrap_extractor import get_bootstrap_tables
from extractors.fixtures_extractor import get_fixtures_table
from extractors.element_summary_extractor import get_element_summary_table
from extractors.utils import pydantic_records_to_arrow_table


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_data():
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


def query_data():
    logger.info("Creating a database connection")
    conn = duckdb.connect(database="fpl2duck.db", read_only=True)

    logger.info("Querying the database")
    import pdb

    pdb.set_trace()

    logger.info("Closing the connection")
    conn.close()


# Flags for load and query can be passed in the command line
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", action="store_true", help="Load data into the database")
    parser.add_argument("--query", action="store_true", help="Query data from the database")
    args = parser.parse_args()

    if args.load and args.query:
        logger.info("Please provide only one flag to either load or query the data")
        exit()
    if not args.load and not args.query:
        logger.info("Please provide a flag to either load or query the data")
        exit()
    if args.load:
        load_data()
    if args.query:
        query_data()
