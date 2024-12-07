import polars as pl
import polars.selectors as cs
from pathlib import Path
import re
import os

root_dir = Path(os.path.abspath('')).parents[0]
data_path = Path(rf'2024/data')
file_name = "day3.csv"
file_path = root_dir / data_path / file_name

# Save the modified content in a temporary file
with open(file_path, "r") as f:
    content = f.read()
    
    
# Part 1 ---
# It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46)
# Scan the corrupted memory for uncorrupted mul instructions. 
# What do you get if you add up all of the results of the multiplications?

data = pl.DataFrame([content])
data_clean_1 = (
    data
    .select(
        clean_mul = pl.col("column_0").str.extract_all(r"mul\(\d+,\d+\)")
    )
    .explode("clean_mul")
    .select(
        left  = pl.col("clean_mul").str.extract_all(r"\d+").list.get(0).cast(pl.Float64),
        right = pl.col("clean_mul").str.extract_all(r"\d+").list.get(1).cast(pl.Float64),
    )
    .with_columns(
        result = pl.col("left") * pl.col("right")
    )
)

print(data_clean_1["result"].sum())

# Part 2 ---
# There are two new instructions you'll need to handle:

# The do() instruction enables future mul instructions.
# The don't() instruction disables future mul instructions.
# Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

data_clean_2 = (
    data
    .select(
        clean_mul = pl.col("column_0").str.extract_all(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
    )
    .explode("clean_mul")
    .with_columns(
        multiply = (
            pl.when(pl.col("clean_mul").str.contains("mul"))
            .then(None)
            .when(pl.col("clean_mul") == "do()")
            .then(pl.lit("do"))
            .otherwise(pl.lit("dont"))
            .forward_fill()
            .fill_null("do")
            )
        )
    .filter(
        pl.col("clean_mul").str.contains("mul"),
        pl.col("multiply") == "do",
    )
    .with_columns(
        left  = pl.col("clean_mul").str.extract_all(r"\d+").list.get(0).cast(pl.Float64),
        right = pl.col("clean_mul").str.extract_all(r"\d+").list.get(1).cast(pl.Float64),
    )
    .with_columns(
        result = pl.col("left") * pl.col("right")
    )
)

print(data_clean_2["result"].sum())