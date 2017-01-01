
import random
import copy

#occurence is the dictionary of number triad (key) and their occurences. It is used in functions.
occurence = {}	

#Order dictionnaries by values. Takes a dictionary as argument. Two lists are given.
class OrderedDict(object):
	def __init__(self, dict):
		self.dict = dict
		self.order()
	
	def order(self):
		keys = list(self.dict.keys())
		self.key_d = []
		for i in range(len(keys)):
			self.key_d.append(None)
		vals = list(self.dict.values())
		self.val_d = copy.copy(vals)
		self.val_d.sort(reverse=True)
		for i, key in enumerate(keys):
			j = 0
			#in case there are two identical dictionary values, order will be the same and keys can be overriden.
			while self.key_d[self.val_d.index(vals[i]) + j] != None:
				j += 1
				self.key_d[self.val_d.index(vals[i]) + j]
			self.key_d[self.val_d.index(vals[i])+j] = key			
	
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
	
	occurence_formatted = "Combinaison"
	for i in range(n_triad):
		occurence_formatted += ";boule_"+str(i+1)
	occurence_formatted += ";frequence\n"

	for key in occurence:
		key_num = ";".join(key.split('-'))
		occurence_formatted += "'"+key+";"+key_num+";"+str(occurence[key])+"\n"

	with open(file, 'w') as loto_stats:
		loto_stats.write(occurence_formatted)					
					
	
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

#provides the dictionary (as part of main program) with the key/occurences for each number triad. Takes a list of numbers as str. n if not a triad is tested
def triad(list_numbers,n=3):
	#-(n-1) to stop at the last number (i+n lower)
	for i in range(len(list_numbers)-n+1):
		key = "-".join(list_numbers[i:i+n])
		try:
			occurence[key] += 1
		except KeyError:
			occurence[key] = 1

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

def add_dict(dic1, dic2):
	total_dic = {}
	for key in dic1:
		try:
			total_dic[key] = dic1[key] + dic2[key]
		except KeyError:
			total_dic[key] = dic1[key]
	for key in dic2:
		try:
			foo = dic1[key]
		except KeyError:
			total_dic[key] = dic2[key]
	return total_dic

def file_write_dic(dic, file):
	ord_dic = OrderedDict(dic)
	dic_format = "Number;Frequency\n"
	for i, key in enumerate(ord_dic.key_d):
		dic_format += str(key)+";"+str(ord_dic.val_d[i])+"\n"
	with open(file, 'a') as loto_stats:
		loto_stats.write(dic_format)

list_numbers = read_stats_file("nouveau_loto.csv",4,5)
get_best_numbers(list_numbers, "loto_stats_3.csv", 3)

best_num_dic = deeper_analysis()
best_num_dic_next_level = deeper_analysis(1)
total_dic = add_dict(best_num_dic, best_num_dic_next_level)

file = "best_numbers.csv"
with open(file, 'w') as loto_stats:
	pass

file_write_dic(best_num_dic, file)
file_write_dic(best_num_dic_next_level, file)
file_write_dic(total_dic, file)
"""
occurence_formatted = "Number;Frequency\n"
for key in best_num_dic:
	occurence_formatted += str(key)+";"+str(best_num_dic[key])+"\n"
occurence_formatted += "\n\nNext round of max occurence.\nNumber;Frequency\n"
for key in best_num_dic_next_level:
	occurence_formatted += str(key)+";"+str(best_num_dic_next_level[key])+"\n"

occurence_formatted += "\n\nTotal of max occurence.\nNumber;Frequency\n"
for key in total_dic:
	occurence_formatted += str(key)+";"+str(total_dic[key])+"\n"
	
file = "best_numbers.csv"
with open(file, 'w') as loto_stats:
	loto_stats.write(occurence_formatted)
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

		
print "Done."