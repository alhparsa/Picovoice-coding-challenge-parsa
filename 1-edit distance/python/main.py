import sys
from typing import *
import unittest
import string


"""
Implementation of Levenshetein Algorithm.
It calculates the number of edits needed (Insertion, 
Substituion and Deletion) for two given strings.

Costs:
- Time: O(mxn) where m and n are the length of our strings
- Space: O(mxn) where m and n are the length of our strings

Method:
- Dynamic programming: We first fill in the first column and
row the 2D array (size m+1 x n+1) to be 0 to m and 0 to n for
the column and row. This is essentially the addition cost of 
each string had we had an empty string for the other one. We
then calculate the cost of addition, deletion and substitution
for each character and take the minimum cost. The last element
in the array reflects the minimum edit cost.
"""


def sub_eval(str_a: str,
             str_b: str,
             pos_i: int,
             pos_j: int,
             case_sensitive: bool = True) -> int:
    """
    Calculates the cost of substitution. If not case sensitive,
    then set `case_sensitive` flag to be False.
    """
    if pos_i < 0 or pos_j < 0:
        return 1
    if case_sensitive:
        if str_a[pos_i] == str_b[pos_j]:
            return 0
    else:
        if str_a[pos_i].lower() == str_b[pos_j].lower():
            return 0
    return 1


def eval_matrix(str_a: str,
                str_b: str,
                len_a: int,
                len_b: int) -> int:
    """
    Calculates the cost of each character within the strings,
    and returns the minimum edit cost.
    """

    matrix = []
    for i in range(len_a+1):
        # Row array that is going to be added to the main array
        row_ls = []
        for j in range(len_b+1):
            # if either i or j is empty then fill in the array
            # with number of insertion needed to construct the
            # string
            if i == 0:
                row_ls.append(j)
            elif j == 0:
                row_ls.append(i)
            else:
                # calculate each cost for the current chars
                deletionCost = matrix[i-1][j]+1
                insertionCost = row_ls[j-1]+1
                subtitutionCost = sub_eval(
                    str_a, str_b, i-1, j-1) + matrix[i-1][j-1]
                # add the minimum cost to the array
                row_ls.append(min(deletionCost, min(
                    insertionCost, subtitutionCost)))
        # append the row to the main 2d array
        matrix.append(row_ls)

    # return the last element which is the minimum edit cost
    return matrix[-1][-1]


def lev(str_a: str,
        str_b: str) -> int:
    """
    Calculates the minimum edit cost.
    """
    len_a = len(str_a)
    len_b = len(str_b)

    # if one of the strings is empty
    if min(len_a, len_b) == 0:
        return max(len_a, len_b)
    # else use the Levenshetein Algorithm
    else:
        return eval_matrix(str_a, str_b, len_a, len_b)


if __name__ == "__main__":
    """
    Takes in two strings from the CLI and returns 
    their minimum edit cost.
    """
    str_a = sys.argv[1]
    str_b = sys.argv[2]
    print(
        f'The minimum edit cost for words {str_a}\
             and {str_b} is {lev(str_a,str_b)}')
