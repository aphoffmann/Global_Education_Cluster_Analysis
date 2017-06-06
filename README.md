# Global_Education_Cluster_Analysis
Vector Support Model to analyze education data, obtained from the world bank, based on country. 

The 'data.csv' file is too big to upload, but as an example of how the program works:

After compiling the program, in the Python REPL commandline enter

  D = Dataset()
  
This will read in data from data.csv, definitions.csv, and codes.csv into a nested dictionary keyed by country then series code.

To represent these datapoints as vectors, enter:

  A = Analysis(D)
  
From here you can enter A.KNN('3-letter country code') to find the  "K nearest neighbors" or countries with the most similar education data.

For example

Input: A.KNN('ITA') #Italy

Output: [(0.22176569754073772, 'SMR', 'San Marino', 'Europe'), (0.32641356366071733, 'CZE', 'Czech Republic', 'Europe'), (0.35834790089150226, 'MKD', 'Macedonia, the former Yugoslav Republic of', 'Europe'), (0.3679861100113707, 'MNE', 'Montenegro', 'Europe'), (0.3884295503375777, 'PLW', 'Palau', 'Oceania')]

The output is a list of the 5 countries with the shortest euclidian distances between their vector representations
