import polars as pl
import polars.selectors as cs
from pathlib import Path
import csv

root_dir = Path(__file__).parents[1]
data_path = Path(rf'2024/data')
file_name = "day2.csv"
file_path = root_dir / data_path / file_name

with open(file_path, "r") as f:
    content = csv.reader(f, delimiter=' ', quotechar='|')
    rows = list(content)
    max_cols = max(len(row) for row in rows)
    
normalized_rows = [row + [""] * (max_cols - len(row)) for row in rows]

# Part 1 ---
# a report only counts as safe if both of the following are true:

# --> The levels are either all increasing or all decreasing.
# --> Any two adjacent levels differ by at least one and at most three.

data = (
    pl
    .DataFrame(
        normalized_rows,
        orient="row",
        infer_schema_length=1_000,
    )
    .with_columns(
        pl.all().replace("", None)
    )
    .with_columns(
        pl.all().cast(pl.Int64)
    )
)

data_1 = (
    data
    .with_columns(
        [
            pl.col(f"column_{i}").gt(pl.col(f"column_{i-1}")).alias(f"is_increasing_{i}")
            for i in range(1, len(data.columns))
        ]
    )
    .with_columns(
        [
            pl.col(f"column_{i}").lt(pl.col(f"column_{i-1}")).alias(f"is_decreasing_{i}")
            for i in range(1, len(data.columns))
        ],
    )
    .with_columns(
        [
            abs(pl.col(f"column_{i}") - pl.col(f"column_{i-1}")).is_between(1, 3, closed="both").alias(f"is_within_{i}")
            for i in range(1, len(data.columns))
        ],
    )
    .fill_null(True)
)

data_clean_1 = (
    data_1
    .select(
        is_monotonic = pl.all_horizontal(cs.matches("is_increasing")) | pl.all_horizontal(cs.matches("is_decreasing")),
        is_within = pl.all_horizontal(cs.matches("is_within")),
    )
    .with_columns(
        is_safe = pl.all_horizontal("is_monotonic", "is_within")
    )
    .sum()
)

print(data_clean_1)

# Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

n_cols = len(data.columns)
data_2_dict = {}
for i, col in enumerate(data.columns):
    
    # Exclude the column
    excluded_data = data.select(pl.exclude(col))
    
    # Rename columns to ensure consecutive numbering
    excluded_data = excluded_data.rename(
        {old_name: f"column_{j}" for j, old_name in enumerate(excluded_data.columns)}
    )
        
    data_2_dict[col] = (
        excluded_data
        .with_columns(
            col = pl.lit(col)
        )
        .with_columns(
            [
                pl.col(f"column_{i}").gt(pl.col(f"column_{i-1}")).alias(f"is_increasing_{i}")
                for i in range(1, len(data.columns) - 1 )
            ]
        )
        .with_columns(
            [
                pl.col(f"column_{i}").lt(pl.col(f"column_{i-1}")).alias(f"is_decreasing_{i}")
                for i in range(1, len(data.columns) - 1 )
            ],
        )
        .with_columns(
            [
                abs(pl.col(f"column_{i}") - pl.col(f"column_{i-1}")).is_between(1, 3, closed="both").alias(f"is_within_{i}")
                for i in range(1, len(data.columns) - 1 )
            ],
        )
        .fill_null(True)
    )

data_2 = (
    pl.concat(data_2_dict.values())
    .select(
        index = pl.arange(0, pl.len()).over('col'),
        col = pl.col("col"),
        is_monotonic = pl.all_horizontal(cs.matches("is_increasing")) | pl.all_horizontal(cs.matches("is_decreasing")),
        is_within = pl.all_horizontal(cs.matches("is_within")),
    )
    .with_columns(
        is_safe = pl.all_horizontal("is_monotonic", "is_within")
    )
    .group_by("index")
    .agg(pl.col("is_safe").max())
    ["is_safe"]
    .sum()
)
print(data_2)
