import pytest
from pyspark import SparkContext, RDD
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StringType, StructField, LongType
from pyspark.testing import assertDataFrameEqual

from emr_serverless_wordcount_example.main import wordcount


@pytest.mark.parametrize(
    ("line", "expected_data"),
    [
        pytest.param(
            [""],
            [],
            id="Empty string results in empty word count"
        ),
        pytest.param(
            [" "],
            [],
            id="Whitespace is ignored for word count."
        ),
        pytest.param(
            ["   "],
            [],
            id="Multiple whitespaces are ignored for word count."
        ),
        pytest.param(
            ["A  B"],
            [
                ("A", 1),
                ("B", 1),
            ],
            id="Wordcount works on simple input text with whitespace"
        ),
        pytest.param(
            ["AB"],
            [
                ("AB", 1),
            ],
            id="Wordcount works on simple input text without whitespace"
        ),
        pytest.param(
            ["hello world pyspark pyspark data science science data pyspark"],
            [
                ("hello", 1),
                ("world", 1),
                ("science", 2),
                ("pyspark", 3),
                ("data", 2),
            ],
            id="Wordcount works on input text with multiple words"
        )
    ]
)
def test_wordcount(spark: SparkSession, line: list[str], expected_data: list[tuple[str, int]]) -> None:
    sc = SparkContext.getOrCreate()
    words_rdd: RDD[str] = sc.parallelize(line)

    actual: DataFrame = wordcount(lines=words_rdd, spark=spark)
    expected: DataFrame = spark.createDataFrame(
        data=expected_data,
        schema=StructType(
            [
                StructField("word", StringType()),
                StructField("count", LongType()),
            ]
        )
    )

    assertDataFrameEqual(actual, expected)
