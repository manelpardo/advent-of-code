import polars as pl
from pathlib import Path
import os

root_dir = Path(__file__).parents[1]
data_path = Path(rf'2024/data')
file_name = "day1.csv"
temp_file_name = "temp_" + file_name
file_path = root_dir / data_path / file_name
temp_file_path = root_dir / data_path / temp_file_name

# Save the modified content in a temporary file
with open(file_path, "r") as f:
    content = f.read().replace("   ", ",")

with open(temp_file_path, "w") as temp_file:
    temp_file.write(content)
    
# Part 1 -------
data = pl.read_csv(
    temp_file_path,
    has_header=False,
    new_columns=["col1", "col2"]
)
os.remove(root_dir / data_path / temp_file_name)

print("Number of rows:", data.shape[0])
temp_series = {}
for col in data.columns:
    temp_series[col] = (
        data
        .select(col)
        .sort(col, descending=False)
    )
data_clean_1 = (
    pl.concat(temp_series.values(), how="horizontal")
    .with_columns(
        abs_diff = abs(pl.col("col1") - pl.col("col2"))
    )
)
print("Day 1, part 1.\nTotal distance between your lists:")
print(data_clean_1["abs_diff"].sum(), "\n")

# Part 2 ---
## Problem
problem_2 = fr'''
    This time, you'll need to figure out exactly how often each number from the left list appears in the right list. Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.
'''

data_clean_2 = data_clean_1
del data_clean_1

col1 = data_clean_2["col1"].to_list()
col2 = data_clean_2["col2"].to_list()

n_occurrences = []
for i, value in enumerate(col1):
    n_occurrences.append(col2.count(value))

similarity_score = (
    pl.DataFrame([
        col1,
        n_occurrences,
        ],
        schema=["col1", "n_occurrences"]
    )
    .with_columns(
        similarity_score = pl.col("col1") * pl.col("n_occurrences")
    )
)
print("Day 1, part 2.\nSimilarity score:")
print(similarity_score["similarity_score"].sum(), "\n")