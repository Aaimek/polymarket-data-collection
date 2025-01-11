from setuptools import setup, find_packages

setup(
    name="polymarket_shared",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.19",
        "psycopg2-binary>=2.9.9",
        "SQLAlchemy-Utils>=0.41.2",
        "python-dotenv>=1.0.1",
    ],
) 