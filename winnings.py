#must add bunch of comments

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
		
def earnings(matching_n, pay_off):
	total = 0
	for n in range(len(matching_n)):
		total += matching_n[n] * pay_off[n]
	return total
	
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
				except ValueError:
					pass
	return pay_off

def costs(winning_n_list):
	invalid = True
	while invalid:
		try:
			ticket_cost = float(raw_input("How much is a ticket worth? "))
			invalid = False
		except ValueError:
			pass
	return ticket_cost * len(winning_n_list)

def winnings(input_n_list, winning_n_list):
	total_costs = costs(winning_n_list)
	total_winnings = calc_winning(input_n_list, winning_n_list, pay_off_grid(input_n_list))
	return total_winnings - total_costs

#winning_n_list = [[1,2,3,4,5], [4,5,6,7,8]]
#input_n_list = [3,4,5,9,10]

#print "bleu", winnings(input_n_list, winning_n_list)