import csv
import os
import random
import heapq
import datetime

class Predict:
	def __init__(self):
		self.directory_name = "stock_price_data_files"


	'''
	Auxiliary function, used to write a list to a .csv file.
	The .csv files are created in the current folder.
	'''
	def print_to_file(self, filename, entries):
		with open(filename + '_output.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(entries)


	'''
	Auxiliary function, used to generate the next date based on the
	date received as parameter.
	'''
	def get_next_date(self, current_date):
		#todo compute next date from current one
		curr_date = datetime.datetime.strptime(current_date, '%d-%m-%Y').date()
		next_date = curr_date + datetime.timedelta(days=1)

		return next_date.strftime('%d-%m-%Y')


	'''
	This is the second API function.
	It receives as params a list with the 10 selected entries from file and also the filename
	which will be used to create the new .csv file for the output.

	'''
	def compute_next_values(self, entries, filename):

		#compute first value as the second highet value from the 10 ones
		values = []
		for element in entries:
			values.append(float(element[2]))
		value1 = heapq.nlargest(2, values)[1]
	
		#compute second value
		value2 = (float(entries[9][2]) - value1 ) / 2
   			
   		#compute third value
		value3 = (value1 - value2) / 4

		#compute timestamps for the next 3 stocks
		date1 = self.get_next_date(entries[9][1])
		date2 = self.get_next_date(date1)
		date3 = self.get_next_date(date2)

		#add new entries to the 10 ones with 2 decimals
		entries.append([entries[0][0], date1, f'{value1:.2f}'])
		entries.append([entries[0][0], date2, f'{value2:.2f}'])
		entries.append([entries[0][0], date3, f'{value3:.2f}'])

		#print old+new entries to the new .csv file
		self.print_to_file(filename, entries)


	'''
	This is the first API function.
	It receives a .csv file name and returns a list of 10 entries from the file,
	taken consecutively from a random timestamp.
	'''
	def process_csv_file(self, filename):

		#read data and save it in a simple list
		data = []
		with open(filename, newline='') as f:
			reader = csv.reader(f)

			try:
				for row in reader:
					data.append(row)

			except csv.Error as err:
				print('Error while reading csv ' + err)

		#generate random number between 0 and (number of rows - 10), both included
		start_pos = random.randint(0, len(data) - 10)

		#return 10 consecutive entries starting with that position
		return data[start_pos : start_pos + 10]


	'''
	This contains the overall logic of the solution.
	We check if the folders exist (the big one and the stock ones inside of it).
	In every stock folder we iterate for the required number of files or until we finish them.
	For every .csv file we found and considered for the solution we call the first API function
	that receives the file name as parameter, process_csv_file().
	The process_csv_file() returns a list with the 10 entries from a random timestamp.
	The list is then used by the second API function, compute_next_values() that creates
	the next 3 values, appends them to the 10 ones and prints them ina new csv file.
	'''
	def process_paths(self, stocks_file_no):

		#check if folder with stock folders exist

		is_folder = os.path.exists(self.directory_name)
		if is_folder is False:
			print("Folder with stock data does not exist!")
			return
		else:
			#iterate through map and make sure the specific stocks'folders exist
			for stock_name, file_no in stocks_file_no.items():
				
				is_folder = os.path.exists(self.directory_name + '/' + stock_name)
				if is_folder is False:
					#this folder does not exist, we continue to look for the remaining ones
					print('Stock folder ' + stock_name + ' does not exist!')
				else:
					#we have a valid stock folder where we can look for files
					path = self.directory_name + '/' + stock_name

					#iterate through list of files
					files_count = 0
					with os.scandir(path) as fs:
						for entry in fs:
							if entry.name.endswith(".csv") and entry.is_file():
								files_count += 1

								#when we completed the required number of files per stock, we go to the next stock
								if files_count > file_no:
									break

								#check if file in empty and ignore it in such a case
								filename = path + '/' + entry.name
								if  os.stat(filename).st_size == 0:
									print("File " + filename + " is empty!")
									continue

								#we can now process the csv file (we call the first and second API function, process_csv_file() and compute_next_values())
								data = self.process_csv_file(path + '/' + entry.name)
								self.compute_next_values(data, entry.name)

								
	'''
	Test method.
	We provide a map with the number of files we want from a stock and the name of the stock.
	'''
	def test_solution(self):

		test_data = {'LSE':3, 'NASDAQ':2, 'NYSE':2}
		self.process_paths(test_data)


p = Predict()
p.test_solution()
