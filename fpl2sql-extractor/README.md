# fpl2sql-extractor

## Overview

The fpl2sql-extractor is a Python application which extracts data from the [Fantasy Premier League](https://fantasy.premierleague.com/) (FPL) API. 

This data is read to [Pydantic](https://docs.pydantic.dev/latest/) classes and written to an instance of [DuckDB](https://duckdb.org/).

The application then exports the database as Parquet files with data, and SQL scripts with DML actions to re-create the database. These are uploaded to a cloud storage bucket (currently [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/r2/)). The export is used by [fpl2sql-frontend](../fpl2sql-frontend/README.md), which loads this data as static files.

## Setup development environment

The following tools are required:

| Tool                                                          | Description                         |
|---------------------------------------------------------------|-------------------------------------|
| [Poetry](https://python-poetry.org/)                          | Dependency management and packaging |
| [pyenv](https://github.com/pyenv/pyenv)                       | Manage Python versions              |
| [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) | Manage Python virtual environments  |
| [direnv](https://direnv.net/)                                 | Manage local environment variables  |


- Create a Python virtual environment using `pyenv-virtualenv`
- Install dependencies with `poetry install`
- If using the upload functionality, populate relevant s3 client credentials in `.envrc`. See [.envrc_example](.envrc_example)
- Run the application to either extract, upload or query the data with the relevant flag using `python fpl2sql-extractor/main.py --extract/upload/query`

## Generate Pydantic models

Pydantic models are generated using `datamodel-code-generator`

```
datamodel-codegen --input api/dump/bootstrap.json --output api/models/bootstrap.py
```

## Deployment

The application is deployed as a [Vercel Function](https://vercel.com/docs/functions) and schedule to run daily at 0300 CET.  

### Application

Steps to deploy are as follow:  

1) Export the `requirements.txt`  
`poetry export --without-hashes --without dev --format=requirements.txt > requirements.txt`
2) Run `sed -i '' 's/ ;.*//' requirements.txt` to provide the file in a format Vercel can handle
3) Run `vercel --prod` to deploy
4) Set environment variables for the application in Vercel

### Scheduler
