import logging
from pyspark.sql import SparkSession

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

INPUT_TXT = "s3://input---emr-serverless-wordcount-example/shakespeare_input.txt"

logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Starting word count application...")

    spark = (
        SparkSession
        .builder
        .appName("WordCount")
        .getOrCreate()
    )

    logger.info(f"Loading text file from '{INPUT_TXT}'...")
    text_file = spark.sparkContext.textFile(INPUT_TXT)

    logger.info(f"Computing counts...")
    counts = (
        text_file
        .flatMap(lambda line: line.split(" "))
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
