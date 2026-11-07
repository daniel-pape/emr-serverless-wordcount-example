import os
from pyspark.sql import SparkSession

INPUT_TXT = "s3://input---emr-serverless-wordcount-example/input.txt"


def main() -> None:
    spark = (
        SparkSession
        .builder
        .appName("WordCount")
        .getOrCreate()
    )

    text_file = spark.sparkContext.textFile(INPUT_TXT)
    counts = (
        text_file
        .flatMap(lambda line: line.split(" "))
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
        .sortBy(lambda x: x[1], False)
    )

    counts_df = counts.toDF(["word", "count"])

    counts_df.show(10, False)
    print("WordCount job completed successfully.")

    spark.stop()

if __name__ == "__main__":
    main()
