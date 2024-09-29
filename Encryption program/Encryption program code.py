# encryption app
# this app will allow two users to communicate encrypted messages, accessible only if they have the key file
# the program will allow a user to create a single randomized key file which they can share with the other user
#


from tkinter import *
from tkinter import messagebox
import random
import string
import os

# global list variable containing a list of characters. the order of the characters will remain constant
# this list has 95 objects, which is why a password may have to be a number with multiple of 5 character length
CHARS = list(string.punctuation+
		 string.ascii_letters+
		 string.digits+
		 ' ')

# copy of the chars list. this will be the key to unlock the encryption, and will change with each different encryption
key = CHARS.copy()

# define the window variable
window = Tk()

# this function will be responsible for randomizing the key for the encryption and create the file where it will be stored
def new_key():
	randomized_key = random.sample(key, len(key))
	key_string = ''
	for i in randomized_key:
		key_string += i
	try:
		key_file = open('recrypt key.txt', 'x')
		key_file.write(key_string)
		key_file.close()
	except FileExistsError:
		messagebox.showinfo(title=' ',
							message='A key already exists in this system. \nIf you wish to create a new one, press "Update key".')

def update_key():
	if os.path.exists('recrypt key.txt'):
		if messagebox.askyesno(title=' ',
							message='A key already exists in this system.\nThis action will rewrite it, and it cannot be undone.\nAre you sure you want to continue?'):
			key_file = open('recrypt key.txt', 'w')
			updated_key = random.sample(key, len(key))
			key_string = ''
			for i in updated_key:
				key_string += i
			key_file.write(str(key_string))
			key_file.close()
		else:
			pass
	else:
		messagebox.showinfo(title=' ', message='There is no key in this system.\nTo write a new one, press "Create new key".')



# this function will get the text introduced by the user, and encrypt it using the key file
def write_new_message():
	if os.path.exists('recrypt key.txt'):
		new_key_button.pack_forget()
		update_key_button.pack_forget()
		write_message_button.pack_forget()
		decrypt_message_button.pack_forget()

		# widget that will hold the text
		global text_area
		text_area = Text(window, font=('Arial', 12))
		# this window configuration will allow the text area to expand
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)
		text_area.grid(stick=N + W + E + S)  # this will stick the edges of the text widget to the edges of the window

		# configure a scrollbar
		scroll_bar = Scrollbar(text_area)
		scroll_bar.pack(side=RIGHT, fill=Y)
		scroll_bar.config(command=text_area.yview)
		text_area.config(yscrollcommand=scroll_bar.set)

		menu_button = Button(text_area, text='Return to menu', command=lambda : [text_area.grid_forget(), start_menu()])
		menu_button.pack(side='bottom')

		save_message_button = Button(text_area, text='Encrypt', command=encrypt_message)
		save_message_button.pack(side='bottom')

	else:
		messagebox.showerror(title='Error', message='There is no key file in the system.')

def encrypt_message():
	key_file = list(open('recrypt key.txt', 'r').read())
	message = str(text_area.get('1.0', END))
	cypher_text = ''  # this variable will store the encrypted text
	for i in CHARS:
		if i not in key_file:
			print(i)
	for letter in message:
		if letter != '\n':
			index = CHARS.index(letter)
			cypher_text += key_file[index]
		else:
			cypher_text += '\n'

	#the encrypted message will be saved in another .txt file
	messagebox.showinfo(title='', message='A file will be created with your encrypted message.\nPrevious messages will be deleted.\n'
									   'For your safety, copy the encrypted message, then delete the .txt file.')

	encrypted_message_file = open('encrypted message.txt', 'w')
	encrypted_message_file.write(str(cypher_text))
	encrypted_message_file.close()

def decrypt_message():
	if not os.path.exists('encrypted message.txt'):
		messagebox.showerror(title='Error', message='There is no encrypted message in this system to decode.')
	else:
		message = ''
		cypher_text = str(open('encrypted message.txt', 'r').read())
		key_file = list(open('recrypt key.txt', 'r').read())
		for letter in cypher_text:
			if letter != '\n':
				index = key_file.index(letter)
				message += CHARS[index]
			else:
				message += '\n'
		decrypt_window = Tk()
		decrypt_window.geometry("{}x{}+{}+{}".format(500, 500,
										 int(window.winfo_screenwidth()/2 - 230),
										 int(window.winfo_screenheight()/2 - 230)))
		decrypt_window.title('Message')

		message_text = Text(decrypt_window, font=('arial', 20))
		message_text.insert('1.0', message)
		decrypt_window.grid_rowconfigure(0, weight=1)
		decrypt_window.grid_columnconfigure(0, weight=1)
		message_text.grid(stick=N + W + E + S)

		scroll_bar = Scrollbar(message_text)
		scroll_bar.pack(side=RIGHT, fill=Y)
		scroll_bar.config(command=message_text.yview)
		message_text.config(yscrollcommand=scroll_bar.set)

		decrypt_window.mainloop()


# this function will open a start menu with different options when the app first opens
# the options will be:
# - Create new key
# - Update key
# - Encrypt a message
# - Decrypt a message
def start_menu():
	welcome_label.pack_forget()
	start_button.pack_forget()

	global new_key_button
	new_key_button = Button(window, text='Create new key',bg='#5cd160', activebackground='#5cd160', font=('Arial', 20),
							command=new_key)
	new_key_button.pack(pady=30)

	global update_key_button
	update_key_button = Button(window, text='Update key',bg='#5cd160', activebackground='#5cd160', font=('Arial', 20),
							   command=update_key)
	update_key_button.pack(pady=30)

	global write_message_button
	write_message_button = Button(window, text='Encrypt new message',bg='#5cd160', activebackground='#5cd160', font=('Arial', 20),
	 								command=write_new_message)
	write_message_button.pack(pady=30)

	global decrypt_message_button
	decrypt_message_button = Button(window, text='Decrypt a message',bg='#5cd160', activebackground='#5cd160', font=('Arial', 20),
									command=decrypt_message)
	decrypt_message_button.pack(pady=30)

def welcome():
	global welcome_label
	welcome_label = Label(window, text='Welcome to Recrypt. \nPress the following button to start.',
						  font=('Arial', 25), bg='#5a41d9', fg='pink', pady=150)
	welcome_label.pack()

	global start_button
	start_button = Button(window, text='START',bg='#5cd160', activebackground='#5cd160', font=('Arial', 10),
	 command=start_menu)
	start_button.pack()

def main():
	#window = Tk()
	icon = PhotoImage(file='Logo.png')
	window.iconphoto(True, icon)
	window.title('Recrypt')
	window.config(bg='#5a41d9')
	window.geometry("{}x{}+{}+{}".format(500, 500,
										 int(window.winfo_screenwidth()/2 - 250),
										 int(window.winfo_screenheight()/2 - 250)))

	welcome()

	window.mainloop()


if __name__ == '__main__':
	main()