import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / 'day_1_data.txt'

# Read the text file into a DataFrame
df = pd.read_csv(FILE_PATH, delimiter='\t', header=None)

df.columns = ['text']

# Part 1 ---
# On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

df = (
    df
    .assign(**{
        'digits': lambda x: x['text'].str.extractall(r'(\d)').unstack().fillna('').sum(axis=1),
        'first_digit': lambda x: x['digits'].str[0],
        'last_digit': lambda x: x['digits'].str[-1],
        'combination': lambda x: x['first_digit'] + x['last_digit'],
    })
)

print(df.head(10))
print(df.shape)
print('Part 1. the sum of all of the calibration values is:')
print(df['combination'].astype('int64').sum())

# Part 2 ---
# It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

keymap = {
    'one':    '1',
    'two':    '2',
    'three':  '3',
    'four':   '4',
    'five':   '5',
    'six':    '6',
    'seven':  '7',
    'eight':  '8',
    'nine':   '9',
}

df = (
    df
    .assign(**{
        'digits': lambda x: (
            x['text']
            .str
            .extractall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))')
            .unstack()
            .fillna('')
            .replace(keymap)
            .sum(axis=1)
        ),
        'first_digit': lambda x: x['digits'].str[0],
        'last_digit': lambda x: x['digits'].str[-1],
        'combination': lambda x: x['first_digit'] + x['last_digit'],
    })
)

print(df.head(10))
print(df.shape)
print('Part 2. the sum of all of the calibration values is:')
print(df['combination'].astype('int64').sum())
