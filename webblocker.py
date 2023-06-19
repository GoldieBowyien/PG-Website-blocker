from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('500x450')
root.resizable(0, 0)
root.title("Surf Blocker | Browser Blocker")

Label(root, text='The Matrix Website Blocker', font='arial 20 bold', fg='#4a2140', pady=15).pack()

# Instructions label
instructions_label = Label(root, text='Enter the websites you want to block (separated by commas):', font='arial 11', fg='grey')
instructions_label.pack()

host_path = 'C:\Windows\System32\drivers\etc\hosts'
ip_address = '127.0.0.1'

Label(root, text='Enter Websites:', font='arial 13 bold').place(x=5, y=115)

Websites = Text(root, font='arial 11', height=2, width=40)
Websites.place(x=140, y=110)

status_label = Label(root, text="Status goes here", font='arial 12 bold')
status_label.place(x=210, y=240)

# Load image icons for import
import_icon = Image.open('importSVG.png')
import_icon = import_icon.resize((30, 30), Image.LANCZOS)
import_icon = ImageTk.PhotoImage(import_icon)
# Load image icons for export
export_icon = Image.open('exportSVG.png')
export_icon = export_icon.resize((30, 30), Image.LANCZOS)
export_icon = ImageTk.PhotoImage(export_icon)

# Create a frame for the footer line
footer_frame = Frame(root, bg='grey', height=2) # change height to 120
footer_frame.pack(side=BOTTOM, fill=X, pady=120) # remove pady

footer_text = Label(root, text='If you want to import the websites from a\ntext file. Click this button:', font='arial 10')
footer_text.place(x=70, y=350)
footer_text = Label(root, text='If you want to export the websites as a\ntext file. Click this icon:', font='arial 10')
footer_text.place(x=70, y=400)

def import_websites():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            websites = file.read().splitlines()
            Websites.delete(1.0, END)
            Websites.insert(END, '\n'.join(websites))
        status_label.config(text='Websites imported successfully.', fg='black')

def export_websites():
    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt')])
    if file_path:
        websites = Websites.get(1.0, END).splitlines()
        with open(file_path, 'w') as file:
            file.write('\n'.join(websites))
        status_label.config(text='Websites exported successfully.', fg='black')

def block_website():
    website_lists = Websites.get(1.0, END)
    Website = list(website_lists.split(","))

    with open(host_path, 'r+') as host_file:
        file_content = host_file.read()

        for web in Website:
            if web in file_content:
                status_label.config(text='Website(s) already blocked', fg='black')
            else:
                host_file.write(ip_address + " " + web + '\n')
                status_label.config(text='Website(s) blocked', fg='red')

def unblock_website():
    website_lists = Websites.get(1.0, END)
    Website = list(website_lists.split(","))

    with open(host_path, 'r+') as host_file:
        lines = host_file.readlines()
        host_file.seek(0)
        blocked = False

        for line in lines:
            if not any(web.strip() in line for web in Website):
                host_file.write(line)
            else:
                blocked = True
        host_file.truncate()

    if blocked:
        status_label.config(text='Website(s) unblocked', fg='green')
    else:
        status_label.config(text='Website(s) already unblocked', fg='black')

def clear_entry():
    Websites.delete(1.0, END)

def exit_app():
    root.destroy()

# Create Export button with icons and text
import_button = Button(root, image=import_icon, text="Import ", font='arial 10 bold', pady=5, compound="right", command=import_websites, bd=3) # bg='orange', activebackground='light yellow'
import_button.place(x=335, y=345)

# Create Export button with icons and text
export_button = Button(root, image=export_icon, text=" Export", font='arial 10 bold', pady=5, compound="left", command=export_websites, bd=3) # bg='yellow'
export_button.place(x=335, y=395)

# Create Block button
block = Button(root, text='Block', font='arial 12 bold', pady=5, command=block_website, width=8, bg='red', activebackground='pink')
block.place(x=210, y=170)

# Create Unblock button
unblock = Button(root, text='Unblock', font='arial 12 bold', pady=5, command=unblock_website, width=8, bg='green', activebackground='light green')
unblock.place(x=310, y=170)

# Create Clear button
clear = Button(root, text='Clear', font='arial 12 bold', pady=5, command=clear_entry, width=6, bg='royal blue', activebackground='sky blue')
clear.place(x=30, y=170)

# Create Exit button
exit_button = Button(root, text='Exit', font='arial 12 bold', pady=5, command=exit_app, width=6, bg='gray', activebackground='light gray')
exit_button.place(x=30, y=230)

root.mainloop()