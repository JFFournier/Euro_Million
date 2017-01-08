"""This module serves to calculate if any given combination pays off (or more likely not) and how much. By providing a ticket price, a combination, a list of the history of winning 
loto numbers as a list of list and a payout grid (by default, the french loto numbers payout grid is used), the system calculates how much it would've cost
to participate in all drawings. It also creates a dictionary where the key is the number of matching numbers and the value is the number of times the combination would've had that many matching
numbers. From the latter and the payout grid, the earnings are calculated. Earnings - costs gives the total which is returned.
"""

#returns the gross earnings from a combination (list of numbers), the list of winning numbers (list of list) and the payout grid (dictionary)
#Done by making a dictionary of matchings numbers:number of times with that many matching numbers. Then uses earnings function to return total.
def calc_winning(input_n_list, winning_n_list, pay_off):
	matching_n = {}
	for i in range(len(input_n_list)):
		matching_n[i] = 0
	for win_number in winning_n_list:
		match = 0
		for number in input_n_list:
			if number in win_number:
				match += 1
		matching_n[match] += 1
	return earnings(matching_n, pay_off)
		
#Returns gross earnings from the matching numbers dictionary and pay_off grid.
#The n index from the matching_n and pay_off dictionary correspond to the value for n matching numbers.
def earnings(matching_n, pay_off):
	total = 0
	for n in range(len(matching_n)):
		total += matching_n[n] * pay_off[n]
	return total
	
#returns a pay_off dictionary (pay off for n matching numbers for all values of n). Default values are from French loto grid, but user can specify his own.
def pay_off_grid(input_n_list):
	source = ''
	while source not in ('y', 'n'):
		source = raw_input("Do you want to use the default grid (5 values only)? (y/n) ").lower()
	if source == 'y':
		pay_off = {0:0, 1:0, 2:5, 3:10, 4:1000, 5:100000}
	else:
		pay_off = {}
		for i in range(len(input_n_list)):
			invalid = True
			while invalid:
				try:
					pay_off[i] = float(raw_input("What is the pay off for %d matching numbers? " %i))
					invalid = False
				#loops while user does not enter a numeric (floatable) value.
				except ValueError:
					pass
	return pay_off

#calculatest the costs of participating in all loto drawings.
def costs(winning_n_list):
	invalid = True
	while invalid:
		try:
			ticket_cost = float(raw_input("How much is a ticket worth? "))
			invalid = False
		except ValueError:
			pass
	return ticket_cost * len(winning_n_list)

#main function that ties all of it together. Returns net total by subtracting costs from earnings. 
#Requires a combination to investigate (as a list) and a list of winning loto numbers as a list of list
def winnings(input_n_list, winning_n_list):
	total_costs = costs(winning_n_list)
	total_winnings = calc_winning(input_n_list, winning_n_list, pay_off_grid(input_n_list))
	return total_winnings - total_costs

#winning_n_list = [[1,2,3,4,5], [4,5,6,7,8]]
#input_n_list = [3,4,5,9,10]

#print "bleu", winnings(input_n_list, winning_n_list)