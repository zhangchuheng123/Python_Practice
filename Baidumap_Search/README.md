## Description:

This script is for search for locations containing some keyword in a specified city.
All the results are written to output.txt.
Baidu Map API is used here.
Since it can only return 400 results per query, the possible region of interested city is divided nto grids, and each of the lattice points are detected and query for results if the point belongs o the interested city.
