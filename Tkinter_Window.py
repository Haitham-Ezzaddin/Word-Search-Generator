from tkinter import *  # tkinter module used for the overall basic GUI
from PIL import ImageTk, Image  # Pillow module used for image resizing
from tkinter import filedialog
from WordSearchGenerator import start_game, EmptyWordlist
from FileConversion import convert_svg_to_pdf
import os  # os module used to access the operating system functions
import tkinter.messagebox
from os import path

root = Tk()  # initialise the main program, root is the conventional name for the base window
root.title('Word Search Puzzle')  # sets the title of the window
root.resizable(False, False)  # disables the resizable function of the window as it causes glitches within the graphics

# Initialise dimension of window and then set the window size to be of the dimensions
dimension_x, dimension_y = 960, 540

# obtains the screen dimensions of the user
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

# sets the x,y position of the screen to the centre
screen_position_x = int((screen_width/2) - (dimension_x/2))
screen_position_y = int((screen_height/2) - (dimension_y/2))
# sets the dimensions of the window and the position to be that of centred
root.geometry(f"{str(dimension_x)}x{str(dimension_y)}+{screen_position_x}+{screen_position_y}")

# The executable has to unpack the images onto a temporary directory, this retrieves the file path of each image.
bg_image_path = path.abspath(path.join(path.dirname(__file__), 'images/Background.png'))
back_btn_path = path.abspath(path.join(path.dirname(__file__), 'images/back-arrow-icon.png'))

# opens the background image first, then resizes it to fit the dimensions of the window,
# then saves the image itself to a variable
background_image = Image.open(bg_image_path)
resized_background_image = background_image.resize((dimension_x, dimension_y), Image.LANCZOS)
new_background_image = ImageTk.PhotoImage(resized_background_image)

# sets the finalized background image as a label
background_image_label = Label(root, image=new_background_image)
# Places the background image label on the window
background_image_label.place(x=0, y=0)


# Does the same as above, however with the backbutton image
backbutton_icon = Image.open(back_btn_path)
resized_backbutton = backbutton_icon.resize((50, 50), Image.LANCZOS)
new_backbutton = ImageTk.PhotoImage(resized_backbutton)


def main_menu_window():
    main_title_label = Label(  # Sets the label to the desired title displayed on the window
        root,  # location of the label
        text="WORD SEARCH GENERATOR",  # the following is the desired attributes such as text, font size and color
        font=('Open Sans Extra Bold', 50),
        bg="#FF914D",  # background color is set to match the background, in cases where the background is a gradient
        fg="#43558D"   # a canvas is used, however it is not needed here.

    )
    main_title_label.place(relx=0.5, rely=0.1, anchor=CENTER)  # places the title on the label
    start_button = Button(  # creates the start button and sets all the desired attributes
        root,   # location of the button
        text='START',
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 35),
        fg="#43558D",
        command=lambda: [initiate_browse_window(), root.withdraw()]  # the button when pressed will execute this two
                                                                     # functions: open the browsing window, close the
                                                                     # window
    )
    start_button.place(relx=0.5, rely=0.4, anchor=CENTER)  # places the button

    help_button = Button(  # creates the help button and sets all the desired attributes
        root,
        text='HELP',
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 35),
        fg="#43558D",
        command=lambda: [help_menu_window(), root.withdraw()]  # executes the functions: open help window
    )                                                          # and close the root
    help_button.place(relx=0.5, rely=0.55, anchor=CENTER)

    quit_button = Button(  # creates the quit button and sets all the desired attributes
        root,
        text='QUIT',
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 25),
        fg="#43558D",
        command=root.destroy  # closes the app completely
    )

    quit_button.place(relx=0.925, rely=0.1, anchor=CENTER)  # places the quit button


def help_menu_window():
    global new_background_image, new_backbutton  # retrieves the global variables of the images

    help_menu = Toplevel()  # sets a new window within the root window main program(not a new program)
    # initializes the window dimensions etc... same as for the main window
    help_menu.geometry(f"{str(dimension_x)}x{str(dimension_y)}+{screen_position_x}+{screen_position_y}")
    help_menu.title("Upload text file")
    help_menu.resizable(False, False)
    # sets the background image as a label and places it
    help_menu_background = Label(help_menu, image=new_background_image)
    help_menu_background.place(x=0, y=0)

    # Creates a vertical scroll bar object for help menu
    scrollbar = Scrollbar(help_menu, orient='vertical')
    scrollbar.pack(side=RIGHT, fill=Y)  # packs it on the right side
    instructions_text = Text(help_menu,  # creates the text box that will contain the online help, sets attributes
                             width=50,
                             height=25,
                             wrap=NONE,
                             yscrollcommand=scrollbar.set,  # sets the command to the scroll bar
                             font=('Open Sans Extra Bold', 15),
                             fg="#43558D",
                             highlightthickness=2,
                             highlightbackground="black")

    instructions_text.insert(END,  # places the instruction text in the text box, START or END won't make a difference
                             '''
    Welcome to the Online Help Menu\n 

    This application is very easy to use and can be used for a \n 
    variety of activities that need a word search puzzle with a \n 
    solution provided separately. \n
    \n
    Scroll through instructions below: \n 
    \n
    1. Firstly, you need to create a text file with all the words you\n 
    need. Head to the application called “Text Edit”. Go to\n 
    “Format” then click “Make Plain Text”. Type in the words\n 
    you want (maximum characters 15) (Maximum 20 words)\n 
    each on a new line and save it\n 
    
    2. Head to the main menu, click “Start”, and then click\n 
    “Browse .txt Files”.\n
    
    3. Choose your designated file then click\n 
    “open”. Following that click “Done!”\n \n
    A pdf of the Word Search Puzzle and a separate solution\n 
    will be stored in the same folder as the text file.\n''')  # \n forces a new line
    instructions_text.place(rely=0.5, relx=0.5, anchor=CENTER)  # places the text box
    instructions_text.config(state=DISABLED)  # disables the ability to edit the text box(read only)

    scrollbar.config(command=instructions_text.yview)  # makes the scrollbar scrollable

    open_main_menu = Button(
        help_menu,
        image=new_backbutton,
        command=lambda: [help_menu.destroy(), root.deiconify()]
    )
    open_main_menu.place(relx=0.91, rely=0.85, anchor=CENTER)
    backbutton_label = Label(
        help_menu,
        text="Main Menu",
        font=('Open Sans Extra Bold', 20),
        bg="#FF914D",
        fg="#43558D"
    )
    backbutton_label.place(relx=0.91, rely=0.95, anchor=CENTER)


def initiate_browse_window():
    # function to initialise the browsing window
    global new_background_image, new_backbutton

    list_window = Toplevel()
    list_window.geometry(f"{str(dimension_x)}x{str(dimension_y)}+{screen_position_x}+{screen_position_y}")
    list_window.title("Upload text file")
    list_window.resizable(False, False)

    # sets the finalized background image as a label
    background_image_label_1 = Label(list_window, image=new_background_image)
    # Places the background image label on the window
    background_image_label_1.place(x=0, y=0)
    file_dialog_btn = Button(
        list_window,
        text='Browse .txt Files',
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 35),
        fg="#43558D",
        command=lambda: [open_filedialog()]
    )
    file_dialog_btn.place(relx=0.5, rely=0.45, anchor=CENTER)
    make_wordsearch_btn = Button(
        list_window,
        text="Done!",
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 35),
        fg="#43558D",
        command=lambda: [make_wordsearch_png(), initiate_wordsearch_window(), list_window.destroy()]
    )
    make_wordsearch_btn.place(relx=0.5, rely=0.6, anchor=CENTER)

    second_window_title = Label(
        list_window,
        text="WORD SEARCH GENERATOR",
        font=('Open Sans Extra Bold', 50),
        bg="#FF914D",
        fg="#43558D"

    )
    second_window_title.place(relx=0.5, rely=0.1, anchor=CENTER)

    txt_file_label = Label(
        list_window,
        text="Upload Your text File Here!",
        font=('Open Sans Extra Bold', 25),
        bg="#FF914D",
        fg="#43558D"
    )
    txt_file_label.place(relx=0.5, rely=0.35, anchor=CENTER)

    open_main_menu = Button(
        list_window,
        image=new_backbutton,
        command=lambda: [list_window.destroy(), root.deiconify()]
    )
    open_main_menu.place(relx=0.93, rely=0.85, anchor=CENTER)
    backbutton_label = Label(
        list_window,
        text="Main Menu",
        font=('Open Sans Extra Bold', 20),
        bg="#FF914D",
        fg="#43558D"
    )
    backbutton_label.place(relx=0.93, rely=0.95, anchor=CENTER)

    quit_button = Button(
        list_window,
        text='QUIT',
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 25),
        fg="#43558D",
        command=root.destroy
    )
    quit_button.place(relx=0.925, rely=0.1, anchor=CENTER)


def initiate_wordsearch_window():
    # function to initialise the wordsearch window
    global background_image, resized_background_image, new_background_image, background_image_label, new_backbutton

    wordsearch_window = Toplevel()
    wordsearch_window.geometry(f"{str(dimension_x)}x{str(dimension_y)}+{screen_position_x}+{screen_position_y}")
    wordsearch_window.title("third window")

    # sets the finalized background image as a label
    background_image_label_1 = Label(wordsearch_window, image=new_background_image)
    # Places the background image label on the window
    background_image_label_1.place(x=0, y=0)

    open_list_window = Button(
        wordsearch_window,
        text="Create Another!",
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 35),
        fg="#43558D",
        command=lambda: [wordsearch_window.destroy(), initiate_browse_window()]
    )
    open_list_window.place(relx=0.5, rely=0.6, anchor=CENTER)

    open_main_menu = Button(
        wordsearch_window,
        image=new_backbutton,
        command=lambda: [wordsearch_window.destroy(), root.deiconify()]
    )
    open_main_menu.place(relx=0.93, rely=0.85, anchor=CENTER)
    backbutton_label = Label(
        wordsearch_window,
        text="Main Menu",
        font=('Open Sans Extra Bold', 20),
        bg="#FF914D",
        fg="#43558D"
    )
    backbutton_label.place(relx=0.93, rely=0.95, anchor=CENTER)
    title = Label(
        wordsearch_window,
        text="WORD SEARCH GENERATOR",
        font=('Open Sans Extra Bold', 50),
        bg="#FF914D",
        fg="#43558D"

    )
    title.place(relx=0.5, rely=0.1, anchor=CENTER)

    quit_button = Button(
        wordsearch_window,
        text='QUIT',
        relief=FLAT,
        bg='#C0E4F4',
        highlightbackground="#C0E4F4",
        font=('Open Sans Extra Bold', 25),
        fg="#43558D",
        command=root.destroy
    )
    quit_button.place(relx=0.925, rely=0.1, anchor=CENTER)

    info_text = Label(
        wordsearch_window,
        text="Check the folder of the text file \n for your wordsearch and solution",
        font=('Open Sans Extra Bold', 27),
        bg="#FF914D",
        fg="#43558D"

    )
    info_text.place(relx=0.5, rely=0.45, anchor=CENTER)


def open_filedialog():
    # function that opens the file dialog and saves the filepath to a variable
    global filename_txt
    filename_txt = filedialog.askopenfilename(initialdir="/", title="Select a text file",
                                              filetypes=(("txt files", "*.txt"),))
    return filename_txt


def make_wordsearch_png():
    global wordsearch_window
    # try / except block to try the initial code and if any errors encountered to raise it to the user as a message box
    try:
        start_game(filename_txt, 15, 15)  # calls the word search generator program
        convert_svg_to_pdf(os.path.splitext(filename_txt)[0] + '.svg')  # converts the files to pdfs
        os.remove(os.path.splitext(filename_txt)[0] + '.svg')  # removes the svg files as the user does not need them
        os.remove(os.path.splitext(filename_txt)[0] + '-solution.svg')
    except NameError:
        tkinter.messagebox.showinfo("File Error", "Please browse and choose a .txt file first")
        wordsearch_window.destroy()
    except ValueError:
        tkinter.messagebox.showinfo("File Error", "Word contains too many characters, please amend the word list")
        wordsearch_window.destroy()
    except SystemError:
        tkinter.messagebox.showinfo("File Error", "We have failed to create a word search, \n "
                                                  "please try again or use a different wordlist")
        wordsearch_window.destroy()
    except EmptyWordlist:
        tkinter.messagebox.showinfo("File Error", "No words detected, please amend the word list")
        wordsearch_window.destroy()



main_menu_window()  # initialises the program

root.mainloop()
