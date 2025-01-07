from setuptools import setup, find_packages

setup(
    name="polymarket_schemas",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.19",
        "psycopg2-binary>=2.9.9",
    ],
) 