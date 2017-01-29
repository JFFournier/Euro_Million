# Euro_Million
Find out what are the best loto numbers from previous winning numbers... assuming it's not completely random (which it is)

Main module is Euro_million.py.
Requires winnings.py module (provided).
Requires one CSV file with historical lotto data. Default example provided (nouveau_loto.csv)

This program will ask user what he wants to do, to provide his own data if he wants (otherwise default data is used).
It looks for the most frequent combinations as opposed to the the most paying ones or the most frequent numbers.
The best numbers, or any other combination, can be checked against historical data to see if how much that would've paid out.

Key coding features: Playing around dictionaries
 - Function to return a dictionary where the values have become keys and vice versa
 - Class object OrderedDict which takes a dictionary and transforms it into an ordered (by value) dictionary.

Assuming lotto machines are well calibrated, combinations are purely coincidental and a bell-shaped curve occurence
distribution is to be expected. It does not mean you'll beat the lotto using this program, quite the contrary: this is another
demonstration that the best way to win at the lottery... is to sell tickets.