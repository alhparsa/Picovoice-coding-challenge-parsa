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

function sub_eval(str_a, str_b, pos_i, pos_j, case_sensitive = true) {
  /*
    Calculates the cost of substitution. If not case sensitive,
    then set `case_sensitive` flag to be False.
    */
  if (pos_i < 0 || pos_j < 0) {
    return 1;
  }
  if (case_sensitive) {
    if (str_a[pos_i] === str_b[pos_j]) return 0;
  } else {
    if (str_a[pos_i].toLowerCase() == str_b[pos_j].toLowerCase()) return 0;
  }
  return 1;
}

function eval_matrix(str_a, str_b, len_a, len_b) {
  /*
  Calculates the cost of each character within the strings,
  and returns the minimum edit cost.
  */

  var matrix = [];
  for (var i = 0; i < len_a; i++) {
    // Row array that is going to be added to the main array
    var row_ls = [];
    for (var j = 0; j < len_b; j++) {
      // if either i or j is empty then fill in the array
      // with number of insertion needed to construct the
      // string
      if (i === 0) row_ls.push(j);
      else if (j === 0) row_ls.push(i);
      else {
        // calculate each cost for the current chars
        const deletionCost = matrix[i - 1][j] + 1;
        const insertionCost = row_ls[j - 1] + 1;
        const subtitutionCost =
          sub_eval(str_a, str_b, i - 1, j - 1) + matrix[i - 1][j - 1];
        // add the minimum cost to the array
        row_ls.push(
          Math.min(deletionCost, Math.min(insertionCost, subtitutionCost))
        );
      }
    }
    // append the row to the main 2d array
    matrix.push(row_ls);
  }

  // return the last element which is the minimum edit cost
  return matrix[len_a - 1][len_b - 1];
}

function lev(str_a, str_b) {
  /*
    Calculates the minimum edit cost.
    */
  const len_a = str_a.length;
  const len_b = str_b.length;

  // if one of the strings is empty
  if (Math.min(len_a, len_b) == 0) return Math.max(len_a, len_b);
  // else use the Levenshetein Algorithm
  else return eval_matrix(str_a, str_b, len_a, len_b);
}

console.log(lev("string A", "str b"));
