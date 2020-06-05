import csv
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Client Database")
root.resizable(False, False)

def get_info():

	""" 
	Function reads each line in "client_data.csv" and organizes data on the main display.
		1. Read each line in "client_data.csv"
		2. Use a for-loop to create rows of displayable information
		3. Delete previous display and replace it with the new rows of information
	"""

	with open('client_data.csv', 'r') as csv_file:
		reader = csv.reader(csv_file)
		info = "No.\tName:\t\t\tPhone:\t\t\tEmail:\n"
		counter = 1
		
		for line in reader:
			temp_list = line[1]
			phone_num = '-'.join([temp_list[:3], temp_list[3:6], temp_list[6:]]) 			# Rewrites the phone number to have hashes in between groups of numbers.
			info = info + str(counter) + "\t" + line[0] + "\t\t\t" + phone_num + \
			"\t\t\t" + line[2] + "\n"
			counter = counter + 1
		
		text_display.delete("1.0", tk.END)													# Deletes information on the current display
		text_display.insert("1.0", info)													# Replaces deleted information with new information

def add_window():

	"""
	Creates a window for the "add" function. Includes a header, labels, entries,
	and a button.
	"""
	
	def add_info():
	
		"""
		Writes name, phone, and email entries into a row in "client_data.csv"
		and opens a window as confirmation.
		
		Variables:
		 - Name: stores input from the name entry box
		 - Phone: stores input from the phone entry box
		 - Email: stores input from the email entry box
		"""
		
		name = str(entry_name.get())
		phone = str(entry_phone.get())
		email = str(entry_email.get())
	
		client = [name, phone, email]														# Appends name, phone, and email into a list so that it may be written into the .csv file

		with open('client_data.csv', 'a') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(client)
		
		entry_name.delete(first = 0, last = 100)
		entry_phone.delete(first = 0, last = 100)
		entry_email.delete(first = 0, last = 100)
			
		temp_list = phone
		phone_num = '-'.join([temp_list[:3], temp_list[3:6], temp_list[6:]])				# Rewrites the phone number to have hashes in between groups of numbers.
			
		output = "Client Information" + "\n"
		output = output + "Name: " + client[0] + "\n"
		output = output + "Phone Number: " + phone_num + "\n"
		output = output + "Email: " + client[2]
		
		messagebox.showinfo('Client successfully added to database.', output)
		
		top.destroy()
		top.update()
		
		get_info()																			# Calls the get_info function to rewrite the information on the display
				
	top = tk.Toplevel()
	top.title("Add a Client")		
	top.resizable(False, False)

	# The "Add Window" Heading
	label_top = tk.Label(top, text = "Client Information")
	label_top.grid(row = 0, column = 0, columnspan= 4)

	# Labels and Entry Boxes for "Name"
	label_name = tk.Label(top, text = "Name")
	label_name.grid(column = 1, row = 1)
	entry_name = tk.Entry(top)
	entry_name.grid(column = 2, row = 1)

	# Labels and Entry Boxes for "Phone Number"
	label_phone = tk.Label(top, text = "Phone No.")
	label_phone.grid(column = 1, row = 2)
	entry_phone = tk.Entry(top)
	entry_phone.grid(column = 2, row = 2)

	# Labels and Entry Boxes for "Email"
	label_email = tk.Label(top, text = "Email")
	label_email.grid(column = 1, row = 3)
	entry_email = tk.Entry(top)
	entry_email.grid(column = 2, row = 3)

	# The "Add" Button
	button_add = tk.Button(top, text = "Add", command = add_info)
	button_add.grid(column = 0, row = 4, columnspan = 4)
	
	

def remove_window():

	"""
	Creates a window for the "remove" function. Includes a header, labels, entries,
	and a button.
	"""

	def remove_info():
		
		"""
		Reads "client_data.csv" to determine whether an inputed value is in the file.
		If it is, the program removes the client associated with the entry from the file.
		"""
		
		with open('client_data.csv') as csv_file:
			reader = csv.reader(csv_file)

		entry = str(entry_remove.get())														# This is the entry that gets compared to the .csv file

		if entry == "" or entry == " ":														# Because there are blanks/spaces in the file, pass an error message when user inputs them
			messagebox.showerror('Error', "No such entry exists.")
		elif entry in open('client_data.csv').read():
			ok = messagebox.askokcancel('Remove Client', "Client has been found. Continue?")
			
			if not ok:
				pass
			else:
				
				with open('client_data.csv', 'r') as csv_file:								# Reads the .csv file to compare with the entry
					reader = csv.reader(csv_file)
					
					with open('temp.csv', 'w') as temp_file:								# Opens a new file, temp.csv, to write the new information with the entry removed from the list
						writer = csv.writer(temp_file)
						
						for line in reader:
							
							if entry not in line:											# Write all lines from reader EXCEPT the line that has the entry in it
								writer.writerow(line)
				
				with open('temp.csv', 'r') as temp_file:									# Now, opens the temp file to be read
					reader = csv.reader(temp_file)
					
					with open('client_data.csv', 'w') as csv_file:							# Rewrites the lines in the temp file to the original file
						writer = csv.writer(csv_file)
						
						for line in reader:
							writer.writerow(line)
														
				top2.destroy()
				top2.update()
				
				get_info()																	# Calls the get_info function to rewrite the information on the display
			
		else:
			messagebox.showerror('Error', "No such entry exists.")



	top2 = tk.Toplevel()
	top2.title("Remove a Client")
	top2.resizable(False, False)

	# The "Remove Window" Heading
	label_top2 = tk.Label(top2, text = "Please enter the name, phone number, or\nemail address of the client you wish to remove:")
	label_top2.pack()
	
	# Entry Box
	entry_remove = tk.Entry(top2)
	entry_remove.pack()
	
	# The "Enter" Button
	button_remove = tk.Button(top2, text = "Enter", command = remove_info)
	button_remove.pack()
	

def search_window():
	
	"""
	Creates a window for the "search" function. Includes a header, labels, entries,
	and a button.
	"""
	
	def search_info():
	
		"""
		Determines whether the user's input is in "client_data.csv".
		If it is, returns the information of the client associated with the input.
		"""
	
		entry = str(entry_search.get())														# This is the entry that gets compared to the .csv file
		
		if entry == "" or entry == " ":														# This if statement is here to avoid any blanks or spaces in the file
			messagebox.showerror('Error', "No such entry exists.")
		elif entry in open('client_data.csv').read(): 										# If the entry is in the file...
			with open('client_data.csv', 'r') as csv_file:									# Opens the file to find the exact line the entry was found
				reader = csv.reader(csv_file)
				
				for line in reader:
					
					if entry in line:														# Assigns each element in the list (in the line) to variables name, phone, and email
							
						name = line[0]
						phone = line[1]
						email = line[2]
						
						temp_list = phone
						phone_num = '-'.join([temp_list[:3], temp_list[3:6], temp_list[6:]])
							
						output = "Client Information" + "\n"
						output = output + "Name: " + name + "\n"
						output = output + "Phone Number: " + phone_num + "\n"
						output = output + "Email: " + email
						
						messagebox.showinfo('Search Results.', output)
						
						top3.destroy()
						top3.update()
				
		else:
			messagebox.showerror('Error', "No such entry exists.")
	
	top3 = tk.Toplevel()
	top3.title("Search for a Client")
	top3.resizable(False, False)
	
	# "Search Window" Heading
	label_top3 = tk.Label(top3, text = "Enter either a name, phone number, or email to\nretrieve the rest of the client's information:")	
	label_top3.pack()
	
	# Entry Box
	entry_search = tk.Entry(top3)
	entry_search.pack()
	
	# The "Enter" Button
	button_search = tk.Button(top3, text = "Enter", command = search_info)
	button_search.pack()

# "Root Window" Heading
label_root = tk.Label(master = root, text = "XX Company's Client Database")
label_root.grid(row = 0, column = 0, columnspan = 3)

# Display Client Information
text_display = tk.Text(master = root)
text_display.grid(row = 1, column = 0, columnspan = 3)
get_info()																					# When the program first runs, displays information from the .csv file

# Add a Client
button_addClient = tk.Button(master = root, text = "Add", command = add_window)
button_addClient.grid(row = 2, column = 0)

# Remove a Client
button_removeClient = tk.Button(master = root, text = "Remove", command = remove_window)
button_removeClient.grid(row = 2, column = 1)

# Search for a Client
button_left = tk.Button(text = "Search", command = search_window)
button_left.grid(row = 2, column = 2)

root.mainloop()