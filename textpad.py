from tkinter import *
from tkinter import filedialog
from tkinter import font

from soupsieve import select

root = Tk()
root.title("Text Editor using python (194018)")
root.geometry("1200x660")

global open_status_name
open_status_name = False

global selected
selected = False


# create file function
def new_file():
    my_text.delete("1.0", END)
    root.title('newfile')
    status_bar.config(text="New file        ")
    global open_status_name
    open_status_name = False


def open_file():
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="/home/", title="Open files", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    if text_file:
        global open_status_name
        open_status_name = text_file

    name = text_file
    status_bar.config(text=f'{name}     ')
    root.title(f'{name} -Text Editor')

    # opening file in reading mode
    text_file = open(text_file, 'r')
    content = text_file.read()

    my_text.insert(END, content)
    text_file.close()


def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="/home/jay", title="Save File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    if(text_file):
        name = text_file
        root.title(f'{name} -Text Editor')
        status_bar.config(text=f'Saved successfuly {name}     ')

        # save file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()


# save file function
def save_file():
    global open_status_name
    if open_status_name:
        # save file
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()
        status_bar.config(text=f'Saved successfuly {open_status_name}     ')
    else:
        save_as_file()


# cut text
def cut_text(e):
    global selected
    # check if we use keyboard shortcut
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            # delete text from text box
            my_text.delete("sel.first", "sel.last")

            root.clipboard_clear()
            root.clipboard_append(selected)


# copy text
def copy_text(e):
    global selected

    # check if we use keyboard shortcut
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


# paste text
def paste_text(e):
    global selected

    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# creatre main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# create scroll bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# create text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow",
               selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.pack()

# config scroll bar
text_scroll.config(command=my_text.yview)


# create menu
menu = Menu(root)
root.config(menu=menu)

# add file menu
file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# add Edit menu
edit_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Cut", command=lambda: cut_text(
    False), accelerator=("Ctrl+x"))
edit_menu.add_command(label="Copy", command=lambda: copy_text(
    False), accelerator=("Ctrl+c"))
edit_menu.add_command(label="Paste", command=lambda: paste_text(
    False), accelerator=("Ctrl+v"))
file_menu.add_separator()
edit_menu.add_command(
    label="Undo", command=my_text.edit_undo, accelerator=("Ctrl+z"))
edit_menu.add_command(
    label="Redo", command=my_text.edit_redo, accelerator=("Ctrl+y"))

# status bar st bottom
status_bar = Label(root, text='Ready     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)


# binding part
root.bind('<Control-x>', cut_text)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)


root.mainloop()
