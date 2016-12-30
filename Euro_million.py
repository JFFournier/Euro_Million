
import random

#occurence is the dictionary of number triad (key) and their occurences. It is used in functions.
occurence = {}	

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
	
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
		triad(list_numbers[i], n_triad)
	
	occurence_formatted = "Combinaison"
	for i in range(n_triad):
		occurence_formatted += ";boule_"+str(i+1)
	occurence_formatted += ";frequence\n"

	for key in occurence:
		key_num = ";".join(key.split('-'))
		occurence_formatted += "'"+key+";"+key_num+";"+str(occurence[key])+"\n"

	with open(file, 'w') as loto_stats:
		loto_stats.write(occurence_formatted)
	
list_numbers = read_stats_file("nouveau_loto.csv",4,5)
get_best_numbers(list_numbers, "loto_stats.csv", 3)

		
print "All in Defs. Done."