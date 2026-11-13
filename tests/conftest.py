import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Fixture for a `SparkSession` for testing."""
    builder = (
        SparkSession.builder
        .master("local[2]")
        .appName("pytest-pyspark-tests")
        .config("spark.ui.enabled", "false")
    )

    session = builder.getOrCreate()

    yield session

    session.stop()