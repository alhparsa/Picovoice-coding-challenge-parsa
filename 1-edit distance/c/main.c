#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdlib.h>

/*
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
*/

int max(int a, int b)
{
    return a > b ? a : b;
}

int min(int a, int b)
{
    return a < b ? a : b;
}

int sub_eval(char *str_a, char *str_b, int pos_i, int pos_j, bool case_sensitive)
{
    /*
    Calculates the cost of substitution. If not case sensitive,
    then set `case_sensitive` flag to be False.
    */
    if (pos_i < 0 || pos_j < 0)
        return 1;
    if (case_sensitive)
    {
        if (str_a[pos_i] == str_b[pos_j])
            return 0;
    }
    else if (tolower(str_a[pos_i]) == tolower(str_b[pos_j]))
        return 0;
    return 1;
}

int eval_matrix(char *str_a, char *str_b, int len_a, int len_b)
{
    /*
    Calculates the cost of each character within the strings,
    and returns the minimum edit cost.
    */

    int matrix[len_a][len_b];
    for (int i = 0; i < len_a; i++)
    {
        // Row array that is going to be added to the main array
        for (int j = 0; j < len_b; j++)
        {
            // if either i or j is empty then fill in the array
            // with number of insertion needed to construct the
            // string
            if (i == 0)
                matrix[i][j] = j;
            else if (j == 0)
                matrix[i][j] = i;
            else
            {
                // calculate each cost for the current chars
                int deletionCost = matrix[i - 1][j] + 1;
                int insertionCost = matrix[i][j - 1] + 1;
                int subtitutionCost =
                    sub_eval(str_a, str_b, i - 1, j - 1, true) + matrix[i - 1][j - 1];
                // add the minimum cost to the array
                matrix[i][j] =
                    min(deletionCost, min(insertionCost, subtitutionCost));
            }
        }
    }

    // return the last element which is the minimum edit cost
    return matrix[len_a - 1][len_b - 1];
}

int lev(char *str_a, char *str_b)
{
    /*
    Calculates the minimum edit cost.
    */
    int len_a = strlen(str_a);
    int len_b = strlen(str_b);

    // if one of the strings is empty
    if (len_a == 0 || len_b == 0)
    {
        printf("min(%d, %d) = %d\n", len_a, len_b, min(len_a, len_b));
        return max(len_a, len_b);
    }
    // else use the Levenshetein Algorithm
    else
        return eval_matrix(str_a, str_b, len_a, len_b);
}

int main(int args, char *argv[])
{
    char *str_a = argv[1];
    char *str_b = argv[2];
    printf("The minimum edit cost for words %s and %s is %d. \n",
           str_a, str_b, lev(str_a, str_b));
    return 0;
}