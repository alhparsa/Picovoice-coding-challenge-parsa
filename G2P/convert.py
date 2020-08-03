import pandas as pd
import sys
from typing import *

"""
Usuage:
python convert.py cmudict.phones cmudict.dict phones.csv words.csv
"""


def main(phonems_filename: str, words_filename: str, phonems_output: str, words_output: str):
    """
    Given input and output filenames, it will do some preprocessing
    for compatibitlity.
    """
    phones = pd.read_csv(phonems_filename, sep='\t', header=None)
    phones[0].rename('Phonems').to_csv(phonems_output, index=False)
    dic = pd.read_csv(words_filename, header=None)
    dic = dic[0].str.split(" ", 1, expand=True)
    dic = dic.rename(columns={0: 'word', 1: 'phonem'})

    # We are going to ignore the lexcial stress
    def is_alpha(s): return ''.join([i for i in s if not i.isdigit()])
    dic.phonem = dic.phonem.apply(is_alpha,)

    # Making sure we don't have duplicates (some words may have two different
    # pronounciations, for simplicity we are going to ignore the other
    # pronounciations).
    dic = dic[~dic.word.str.contains('\(')]
    dic.to_csv(words_output, index=False)


if __name__ == "__main__":
    # Getting the input and output filenames
    phonems_filename = sys.argv[1]
    words_filename = sys.argv[2]
    phonems_output = sys.argv[3]
    words_output = sys.argv[4]
    main(phonems_filename, words_filename, phonems_output, words_output)
