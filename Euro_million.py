
import random
import copy
import winnings

#occurence is the dictionary of number triad (key) and their occurences. It is used in functions.
occurence = {}	

#Order dictionaries by values. Takes a dictionary as argument. Two lists are given with matching indexes.
class OrderedDict(object):
	def __init__(self, dict, reverse_sort=True):
		self.dict = dict
		self.order(reverse_sort)
	
	#Creates order in dictionary. val_d variable for values as a list and key_d variable for keys.
	#works by creating reverse dictionary (reverse key and values), then appends list of keys and values in order of values
	def order(self, reverse_sort=True):
		keys = list(self.dict.keys())
		self.key_d = []
		self.val_d = []
		dic_inv = reverse_dico(self.dict)
		n = 0
		max_val = max(self.dict.values())
		if reverse_sort == True:
			for n in range(max_val):
				x = max_val - n
				self.order_list(dic_inv, x)
		else:
			min_val = min(self.dict.values())
			for n in range(max_val):
				x = min_val + n
				self.order_list(dic_inv, x)
		
	#used by order function; creates the lists
	def order_list(self, dic_inv, x):
		try:
			len_x = len(dic_inv[x])
			#in case more than one value per key which corresponds in normal dict to many keys having the same value
			for i in range(len_x):
				self.val_d.append(x)
			for i in range(len_x):
				self.key_d.append(dic_inv[x][i])
		except KeyError:
			pass				
				
#Object that computes all permutation possible of N numbers within M numbers. Takes list of numbers (as str) and N_Triad as arguments.
class TriadsN(object):
	def __init__(self, list_numbers, N_Triad = 3):
		# -1 because counter starts at 0, but easier to count triads from 1.
		self.N_Triad = N_Triad - 1
		self.list_numbers = list_numbers
		self.key = []
		self.key_no = 0
		
	#generates the list of keys as a list of list of numbers (as str). Works as recursive function.
	#Arguments only necessary within recursive function; initiation does not require them.
	#Takes the starting and ending i values for the for loops. Equal to 0 and length of N_Triad.  
	#Level is to keep tract of the depth of recursive function.
	def key_gen(self, start_i = 0, end_i=None, level=-1):
		if end_i is None:
			end_i = len(self.list_numbers) - self.N_Triad
		level += 1
		for i in range(start_i, end_i):
			try:
				self.key[self.key_no].append(self.list_numbers[i])
			except IndexError:
				self.key.append([self.list_numbers[i]])
			#checks if key is complete and should move on to next one.
			if level == self.N_Triad:
				#shallow copy to prevent modification of previous keys. Needs to remember previous levels of keys.
				transit = copy.copy(self.key[self.key_no])
				self.key.append(transit)
				self.key_no += 1
				#deletes last level of key to change it for new one
				del self.key[self.key_no][level]
			#if not at last level of key generation, then reenters function to loop through the numbers, but always with +1 on starting and ending i (no duplicate values).
			if level < self.N_Triad:
				self.key_gen(i + 1, end_i + 1, level)	
			#if at the end of the for loop, must delete another level of key as recursion will occur at the next loop.
			if i == end_i - 1:
				try:
					del self.key[self.key_no][-1]
				#at the end of all loops, program creates an extra (shallow) key, then deletes all member before generating error. This is normal and means recursion should end.
				except IndexError:
					del self.key[-1]
					return

	#provides the dictionary (as part of main program) with the key/occurences for each number triad. 
	def triad(self):
		self.key_gen()
		for k in self.key: 
			key_str = "-".join(k) 
			try:
				occurence[key_str] += 1
			except KeyError:
				occurence[key_str] = 1

#reads csv file to get numbers; start at cell 'init' and ends reading after 'n' numbers. Returns a list of numbers as strings.
def read_stats_file(file, init = 4, n = 5):
	with open(file, 'r') as f:
		f.readline()
		list_numbers = []
		for line in f:
			number_as_str = []
			number = []
			line = line.split(';')
			number_as_str = line[init:init+n]
			#converts to numbers so they can be sorted. Must reconvert to str to concatenate later on.
			for num in number_as_str:
				number.append(int(num))
			number.sort()
			number_as_str = []
			for num in number:
				number_as_str.append(str(num))
			list_numbers.append(number_as_str)
	return list_numbers

#iterates through the list of number (as str); creates the triad and populates the occurence dictionary (which is a main variable). 
#Variables are a list of list of numbers (as str), output filename and length of chain if not 3.
def get_best_numbers(list_numbers, file, n_triad=3):
	for i in range(len(list_numbers)):
		triad_object = TriadsN(list_numbers[i], n_triad)
		triad_object.triad()
	
	occurence_formatted = "Combination"
	for i in range(n_triad):
		occurence_formatted += ";ball_"+str(i+1)
	occurence_formatted += ";frequency\n"

	file_write_dic(occurence, file, occurence_formatted, 'w')
	
#n is the number of numbers; max is range for random; returns number as a list of str; 
def loto_number(n, max):
	number = []
	for i in range(n):
		number.append(random.randint(1,max))
	number.sort()
	number_as_str = []
	for num in number:
		number_as_str.append(str(num))
	return number_as_str

def generate_fake_numbers():
	list_numbers = []
	#generates random loto numbers; should change to real data
	for i in range(5000):
		list_numbers.append(loto_number(5,49))
	return list_numbers

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

#reverses a dictionary so that keys can be looked up from values even when multiple keys have the same values
def reverse_dico(dico):
	reversed_dico = {}
	for key in dico:
		try:
			reversed_dico[dico[key]].append(key)
		except KeyError:
			reversed_dico[dico[key]] = [key]
	return reversed_dico

#Returns the max occurence frequency and the list of all combinations that are the most 'popular'. Also returns the reverse dico.
#n to offset the best_num_list from max
def max_occurence(n=0):
	reverse_occ = reverse_dico(occurence)
	max_key = max(occurence.values())
	best_num_list = []
	#for i in range(n):
	best_num_list += reverse_occ[max_key-n] #i or n selon que for ou pas
	return max_key, best_num_list, reverse_occ

#Returns list of list of numbers after splitting a list of joined numbers. If False is sent, then numbers as a list
def split_numbers(joined_numbers, list_of_list=True):
	list_numbers = []
	if list_of_list == True:
		for number in joined_numbers:
			list_numbers.append(number.split('-'))
	else:
		for number in joined_numbers:
			list_numbers += number.split('-')
	return list_numbers
	
#returns the numbers as a dictionary that occur the most often within the occurence dictionary at a specified occurence level from the max. Return is weighted by occurence.
#n to offset the best numbers from max occurence (1 looks at 2nd best and so on)
def deeper_analysis(n=0):
	best_num_dic = {}
	max_occ, best_num, reverse_occ = max_occurence()
	best_list_numbers = list(set(split_numbers(best_num,False)))
	max_occ, best_num, reverse_occ = max_occurence(n)
	second_best_list_numbers = split_numbers(best_num)
	for num in best_list_numbers:
		for num_list in second_best_list_numbers:
			if num in num_list:
				try:
					best_num_dic[num] += 1 * (max_occ -  n)
				except KeyError:
					best_num_dic[num] = 1 * (max_occ - n)
	return best_num_dic

#Returns the sum of two dictionaries as a dictionary where values are numeric only. All keys from both dictionaries are created. Values are added.
def add_dict(dic1, dic2):
	total_dic = {}
	for key in dic1:
		#if the same key exist in both dictionaries, then add values
		try:
			total_dic[key] = dic1[key] + dic2[key]
		#if key does not exist in second dictionary, then only use value from dic1.
		except KeyError:
			total_dic[key] = dic1[key]
	#must also add keys that only exist in the second dictionary. 
	#If they exist in dic1, then it is ignored (foo). If it doesn't, it will create an error which is caught and used to add the key/value pair to total_dic.
	for key in dic2:
		try:
			foo = dic1[key]
		except KeyError:
			total_dic[key] = dic2[key]
	return total_dic

#writes the content of dictionary to a csv file. dic_formatted provides the header, but then dictionary content is added into it.
#takes dictionary, the filename to write and the header as input. File opening mode (append or write) is optional.
def file_write_dic(dic, file, dic_formatted, mode='a'):
	#dictionary is ordered by using custom class object. 
	ord_dic = OrderedDict(dic)
	#Not the same no of columns depending on whether file writing occurs when writing combinations or best numbers
	if 'Combination' in dic_formatted:
		for i, key in enumerate(ord_dic.key_d):
			key_num = ";".join(key.split('-'))
			#' added otherwise some 3 numbers combinations are understood as dates in excel.
			dic_formatted += "'"+key+";"+key_num+";"+str(ord_dic.val_d[i])+"\n"
	else:
		for i, key in enumerate(ord_dic.key_d):
			dic_formatted += key+";"+str(ord_dic.val_d[i])+"\n"
	#4 tries to close file if opened. 
	for n in range(4):
		try:
			with open(file, mode) as loto_stats:
				loto_stats.write(dic_formatted)
			break
		except IOError:
			print "%s file is opened. Please close before continuing." %(file)
			pause()
	else:
		print "\nYou apparently did not close the file, so I didn't write anything."

#takes a dictionary and returns the reversed dictionary (keys become values and vice-versa) and the list of keys (numbers) that match the highest values (occurence)
def reverse_dico_max_list(dic):
	best_reverse_dico = reverse_dico(dic)
	best_reverse_list = best_reverse_dico[max(dic.values())]
	return best_reverse_dico, best_reverse_list

#gets the next iteration of best numbers from the current best numbers by looking at N-1 combinations.
def number_runs(file_i):
	max_occ, best_num, reverse_occ = max_occurence()
	#must reset global variable occurence dictionary
	global occurence
	occurence = {}
	file = "loto_stats_"+str(file_i)+".csv"
	new_list_numbers = split_numbers(best_num)
	get_best_numbers(new_list_numbers, file, file_i)


number_amount = 5 #raw_input("How many numbers should be guessed? ") #add error check

list_numbers = read_stats_file("nouveau_loto.csv",4,number_amount)

#ask if user as his own numbers he wants to run to see if you would've won. Run winnings. 


"""
Or better yet, make a menu asking 
a) Check if your combination would have won anything.
b) Determine best numbers
    --> Secondary question is how many numbers to look at
	--> This should then run winnings
	
don't just run winnings.winnings... avoid running costs() twice. use try on total_costs... sorta of
try:
	total_costs = total_costs
	total_winnings = winnings.calc_winning(input_n_list, winning_n_list, winnings.pay_off_grid(input_n_list))
	return total_winnings - total_costs	
except NameError:
	return winnings.winnings
"""

no_combination = 3 #raw_input("how many numbers do you want to look at?") #add error check
file = "loto_stats_"+str(no_combination)+".csv"
get_best_numbers(list_numbers, file, no_combination)

#get the best numbers and puts them in dictionnaries (combinations and their occurences)
best_num_dic = deeper_analysis()
best_num_dic_next_level = deeper_analysis(1)
total_dic = add_dict(best_num_dic, best_num_dic_next_level)

#write the best numbers from dictionaries into files
file = "best_numbers.csv"
file_write_dic(best_num_dic, file, "Number;Frequency\n", 'w')
file_write_dic(best_num_dic_next_level, file, "Number;Frequency\n")
file_write_dic(total_dic, file, "Number;Frequency\n")

#ask if user wants a breakdown; of the occurence of smaller sets within the best set; use a while and perhaps a def; filenames with variable

while no_combination > 1:
	no_combination -= 1
	number_runs(no_combination)


#This segment will get the final pick of numbers as a list. This is what should go into the winnings module. 
#best_reverse_list as the list of best numbers. This is the initial pick.
best_reverse_dico, best_reverse_list = reverse_dico_max_list(best_num_dic)
#number_amount = 12 this is just for debugging; number_amount is set at the beginning according to number of loto numbers in each draw
#loops through the very best numbers, picking them in order max occurence until there is as many numbers as are drawn in loto
while len(best_reverse_list) < number_amount:
	#if there is a single occurence/frequency, then don't eliminate that occurence ; instead re-run same dictionary in next step without trimming. 
	if len(reverse_dico(best_num_dic)) != 1:
		#remove max occurence (already in best_reverse_list) 
		best_num_dic = {k:v for k, v in best_num_dic.iteritems() if v != max(best_num_dic.values())}
	else:
		#removes numbers already picked to prevent infinite while. Sets best_num_dic_next_level to best numbers minus those picked for final pick.
		best_num_dic = {k:v for k, v in best_num_dic.iteritems() if k not in best_reverse_list}
		best_num_dic_next_level = best_num_dic
	#error generated when number_amount is less than total numbers from first pick. In that case, just return what we have.
	try: 
		second_best_list = best_reverse_dico[max(best_num_dic.values())]
	except ValueError:
		print "Not enough data to pull out enough best numbers."
		break
	#if necessary, go look in occurence from one level down to discriminate between identical occurence. Use OrderedDict to just get the right number of numbers.
	if len(second_best_list) + len(best_reverse_list) > number_amount:
		best_num_dic_next_level = {k:v for k, v in best_num_dic_next_level.iteritems() if k not in best_reverse_list and k in second_best_list}
		ordered_second_best = OrderedDict(best_num_dic_next_level)
		best_reverse_list += ordered_second_best.key_d[0:number_amount-len(best_reverse_list)]
	elif len(second_best_list) + len(best_reverse_list) == number_amount:
		best_reverse_list += second_best_list[0:number_amount-len(best_reverse_list)]
	else:
		best_reverse_list += second_best_list

#ask if user as his own numbers he wants to run to see if you would've won. Then publish best numbers according to program. Then compare results.		

print "the best numbers are: ", best_reverse_list #[max(best_num_dic.values())]

pause()
print winnings.winnings(best_reverse_list,list_numbers)	
print "Done."