
import random
import copy
import winnings

#occurence is the dictionary of number triad (key) and their occurences. It is used in functions.
occurence = {}	

#Order dictionnaries by values. Takes a dictionary as argument. Two lists are given with matching indexes.
class OrderedDict(object):
	def __init__(self, dict):
		self.dict = dict
		self.order()
	
	#Creates order in dictionary. val_d variable for values as a list and key_d variable for keys.
	def order(self, reverse_sort=True):
		keys = list(self.dict.keys())
		self.key_d = []
		for i in range(len(keys)):
			self.key_d.append(None)
		vals = list(self.dict.values())
		self.val_d = copy.copy(vals)
		self.val_d.sort(reverse=reverse_sort)
		for i, key in enumerate(keys):
			j = 0
			key_index = self.val_d.index(vals[i] + j)
			#in case there are two identical dictionary values, order will be the same and keys can be overriden.
			if self.key_d[key_index] != None:
				j = self.key_d[key_index:].index(None)
			self.key_d[key_index + j] = key			
	
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

	#dictionary is ordered by using custom class object. 
	ord_occ = OrderedDict(occurence)

	file_write_dic(ord_occ, file, occurence_formatted, 'w')
	
	
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
	#reverse_occ = reverse_dico(occurence)
	max_key = max(occurence.values())
	best_num_list = []
	#for i in range(n):
	try:
		best_num_list += reverse_occ[max_key-n] #i or n selon que for ou pas
	except NameError:
		reverse_occ = reverse_dico(occurence)
		best_num_list += reverse_occ[max_key-n] #i or n selon que for ou pas
	return max_key, best_num_list #, reverse_occ

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
	max_occ, best_num = max_occurence()
	best_list_numbers = list(set(split_numbers(best_num,False)))
	max_occ, best_num = max_occurence(n)
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
#takes OrderedDict object, the filename to write and the header as input. File opening mode (append or write) is optional.
def file_write_dic(ord_dic, file, dic_formatted, mode='a'):
	for i, key in enumerate(ord_dic.key_d):
		if '-' in key:
			key_num = ";".join(key.split('-'))
			dic_formatted += "'"+str(key)+";"+key_num+";"+str(ord_dic.val_d[i])+"\n"
		else:
			dic_formatted += key+";"+str(ord_dic.val_d[i])+"\n"
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
			
list_numbers = read_stats_file("nouveau_loto.csv",4,5)
best_num_first_level = get_best_numbers(list_numbers, "loto_stats_3.csv", 3)
reverse_occ = reverse_dico(occurence)

#print winnings.winnings(['23','36','39','49','17'],list_numbers)
"""
strategy is to use OrderedDict at this level instead of file_write_dic. Use OrderedDict object and/or max_occ (deeper_analysis runs this and returns it)
to get only the best one. Then use best_num_dic_next_level (OrderedDict) must ask for input n numbers to know how many to return. 

scratch that... 

just use reverse dico as shown below. Should try to get that from deeper_analysis() / max_occurence that run it.

Should reverse some changes using OrderedDict... do whatever is most efficient.

Also look into alternate way to sort dictionary using reverse_dico... by using 
for n in range(....):
	try:
		reverse_dico[max(dico.values())-n]
	except ValueError:
		pass

"""

best_num_dic = deeper_analysis()
best_num_ord_dic = OrderedDict(best_num_dic)

best_num_dic_next_level = deeper_analysis(1)
best_num_ord_dic_next_level = OrderedDict(best_num_dic_next_level)
#must rewrite add_dict so it works with OrderedDict object. then uncomment next line (and few lines down). Also deeper_analysis() should return OrderedDict to make things more simple.
#total_dic = add_dict(best_num_dic, best_num_dic_next_level)

#that's the principe... don't run reverse_dico, get it from when it was run
best_reverse = reverse_dico(best_num_dic)

print "the best numbers are: ", best_reverse[max(best_num_dic.values())]

pause()
file = "best_numbers.csv"


file_write_dic(best_num_ord_dic, file, "Number;Frequency\n", 'w')
file_write_dic(best_num_ord_dic_next_level, file, "Number;Frequency\n")
#file_write_dic(total_dic, file, "Number;Frequency\n")


"""
max_occ, best_num, reverse_occ = max_occurence()
#must reset occurence for second run
occurence = {}
list_numbers = split_numbers(best_num)
get_best_numbers(list_numbers, "loto_stats_2.csv", 2)

max_occ, best_num, reverse_occ = max_occurence(0)
occurence = {}
list_numbers = split_numbers(best_num)
get_best_numbers(list_numbers, "loto_stats_1.csv", 1)
"""
		
print "Done."