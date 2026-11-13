import logging

from pyspark import RDD
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, LongType

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

INPUT_TXT = "s3://input---emr-serverless-wordcount-example/shakespeare_input.txt"

logger = logging.getLogger(__name__)

def wordcount(lines: RDD[str], spark: SparkSession) -> DataFrame:
    """
    Returns a `DataFrame` with columns `word` and `count` giving the
    wordcount of each word from the `lines` RDD.

    :param lines: An `RDD` of string where each string is a text line.
    :param spark: `SparkSession` used for the computation
    :return: The `DataFrame` of word counts.
    """
    counts = (
        lines
        .flatMap(lambda line: line.split(" "))
        .filter(lambda word: word != " " and word != "")
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
        .sortBy(lambda x: x[1], False)
    )

    if counts.isEmpty():
        return spark.createDataFrame(
            data=[],
            schema=StructType(
                [
                    StructField("word", StringType()),
                    StructField("count", LongType()),
                ]
            )
        )

    return counts.toDF(["word", "count"])


def main() -> None:
    """
    Computes word counts for the input text file and prints the
    top-10 word count pairs to the console.

    :rtype: None
    """
    logger.info("Starting word count application...")

    spark = (
        SparkSession
        .builder
        .appName("WordCount")
        .getOrCreate()
    )

    logger.info(f"Loading text file from '{INPUT_TXT}'...")
    text_file: RDD[str] = spark.sparkContext.textFile(INPUT_TXT)

    logger.info(f"Computing counts...")
    counts = (
        text_file
        .flatMap(lambda line:  line.split(" "))
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
        .sortBy(lambda x: x[1], False)
    )

    counts_df = counts.toDF(["word", "count"])

    logger.info("Top-10 word counts:")
    counts_df.show(10, False)
    logger.info("Word count job completed successfully.")

    spark.stop()

if __name__ == "__main__":
    main()
