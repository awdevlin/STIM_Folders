import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


# Class to create a GUI used to input patient data
class folder_gui:
    def __init__(self):
        self.stim_info = {}
        self.__define_input_box()
        self.__create_fields()
        self.window.mainloop()

    # Shape, size, and title of the window
    def __define_input_box(self):
        self.window = tk.Tk()
        self.window.title("Create STIMULUS Folders")
        self.window.geometry("")  # This makes the window the smallest size that still contains all the elements

    # Creates entry regions for each data point and their labels
    def __create_fields(self):
        self.new_folder_path = InfoFields(self.window, 0)
        self.new_folder_path.create_button('Browse to STIMULUS DATA',
                                           lambda: self.__browse_files(self.new_folder_path))
        self.new_folder_path.create_entry(os.getcwd())

        self.mat_id = InfoFields(self.window, self.new_folder_path.next_row())
        self.mat_id.create_label("Maternal ID: ")
        self.mat_id.create_entry("STIM000")

        trim_row = self.mat_id.next_row()
        self.label = tk.Label(self.window, text="Trimester: ")
        self.label.grid(column=0, row=trim_row, pady=(15, 0), sticky="w", padx=15)

        self.trim_var = tk.StringVar(self.window)
        self.trim_var.set("Select an Option")
        trim_list = ["1st Trim", "2nd Trim", "3rd Trim", "Ex Vivo Plac"]
        self.trimester = tk.OptionMenu(self.window, self.trim_var, *trim_list)
        self.trimester.grid(column=1, row=trim_row, pady=15)

        self.folder_button = InfoFields(self.window, trim_row + 2)
        self.folder_button.create_button("Create New Folders", self.__folder_button)

    # Allows for browsing folders. This can make it much easier to find the folder of interest
    @staticmethod
    def __browse_files(info_fields):
        desktop_path = os.path.expanduser("~")
        info_fields.entry.delete(0, "end")
        info_fields.entry.insert(0, filedialog.askdirectory(initialdir=desktop_path))
        info_fields.entry.config(fg="black")
        info_fields.entry.unbind("<FocusIn>")

    @staticmethod
    def __grey_out(check_button, target):
        if check_button.get_cb():
            target.button.config(bg="black", fg="white", state="normal")
            target.entry.config(bg="white", state="normal")
        else:
            target.button.config(bg="grey", fg="grey", state="disabled")
            target.entry.config(bg="grey", state="disabled")

    # Reads all data entered into the data fields and return it to the function opening this GUI. It is designed to be
    # used at the press of a button .This function also closes the GUI.
    def __folder_button(self):
        # close the tkinter window if participant information was entered completely. Else send warning message
        if self.__check_stim_info():
            self.__create_folders()
            print("Folders created for " + self.mat_id.get_entry() + " " + self.trim_var.get())
        else:
            messagebox.showwarning(title='Data Entry Warning', message='All Information Fields Must Be Filled')

    def __create_folders(self):
        new_folder_path = self.new_folder_path.get_entry()
        stim_id = self.mat_id.get_entry().upper()
        trim = self.trim_var.get()
        trimester_path = os.path.join(new_folder_path, stim_id, trim)
        clarius_images = os.path.join(" " + "Annotated Clarius Images", "Unlabelled Clarius Images")
        clarius_videos = os.path.join(" " + "Annotated Clarius Images", "Clarius Videos")
        os.makedirs(os.path.join(trimester_path, stim_id + clarius_images))
        os.makedirs(os.path.join(trimester_path, stim_id + clarius_videos))
        os.makedirs(os.path.join(trimester_path, stim_id + " " + "RF Data"))
        if trim in ["1st Trim", "2nd Trim", "3rd Trim"]:
            os.makedirs(os.path.join(trimester_path, stim_id + " " + "Annotated GE Images"))
        if trim == "Ex Vivo Plac":
            os.makedirs(os.path.join(trimester_path, stim_id + " " + "Histology Photos"))
            os.makedirs(os.path.join(trimester_path, stim_id + " " + "Study Photos"))

    # Check if any values are left blank in the GUI when recording participant data
    def __check_stim_info(self):
        stim_info = [self.new_folder_path.get_entry(), self.mat_id.get_entry(), self.trim_var.get()]
        for field in stim_info:
            # Catches a blank entry in stim_info. If that entry is the calibration library path and the user is not
            # looking for calibration data, that is allowed to be blank
            if field == '' or field == "Select an Option":
                return False
        return True


class InfoFields:
    def __init__(self, window, row):
        self.window = window
        self.row = row
        self.row_increment = 0
        self.entry = tk.Entry
        self.label = tk.Label
        self.button = tk.Button
        self.cb_var = tk.IntVar()
        self.pady = 15
        self.padx = 15

    def create_label(self, text, col=0):
        self.label = tk.Label(self.window, text=text)
        self.label.grid(column=col, row=self.row + self.row_increment, pady=(self.pady, 0), sticky="w", padx=self.padx)
        self.row_increment += 1

    def create_entry(self, text="", col=0, col_span=3):
        self.entry = tk.Entry(self.window, width=75, justify="center", borderwidth=3)
        self.entry.grid(column=col, row=self.row + self.row_increment, columnspan=col_span, padx=self.padx, sticky="w")
        self.entry.insert(0, text)
        self.entry.config(fg="grey")  # Default text starts greyed out

        # Bind() passes the event that triggered it to the lambda function as the parameter e; it's not used for
        # anything, but it must be handled
        self.entry.bind("<FocusIn>", lambda e: self.__delete_text(self.entry))
        self.entry.bind("<FocusOut>", lambda e: self.__focusout_replace(self.entry, text))
        self.row_increment += 1

    def create_button(self, text, command, col=0, span=2):
        self.button = tk.Button(self.window, text=text, bg="black", fg="white", command=command, width=25)
        self.button.grid(column=col, row=self.row + self.row_increment, pady=(self.pady, 10), columnspan=span,
                         sticky="w", padx=self.padx)
        self.row_increment += 1

    # Creates a checkbox that will allow the user to choose whether to pull calibration data from the library
    def create_check_box(self, text, selected, command, col=0):
        self.cb_var = tk.IntVar()
        cb = tk.Checkbutton(self.window, text=text, variable=self.cb_var, command=command)
        cb.grid(column=col, row=self.row + self.row_increment, pady=(self.pady, 0))
        if selected:
            cb.select()
        self.row_increment += 1

    # Returns the next row after that last row used by this class.
    def next_row(self):
        return self.row + self.row_increment

    # Reads the value from an entry used in this class.
    def get_entry(self):
        return self.entry.get()

    def get_cb(self):
        return self.cb_var.get()

    # Use lambda function to delete text when first clicking on a box with grey template text. This delete happens once.
    # EG. event.bind("<FocusIn>", lambda e: self.__delete_text(event))
    # the 'e' in lambda e is required because bind() passes the event that triggers it.
    @staticmethod
    def __delete_text(entry):
        entry.delete(0, "end")
        entry.config(fg="black")
        entry.unbind("<FocusIn>")

    # If no information is found in the Entry, fill it with the default text
    def __focusout_replace(self, entry, old_text):
        if entry.get() == "":
            entry.insert(0, old_text)
            entry.config(fg="grey")
            entry.bind("<FocusIn>", lambda e: self.__delete_text(entry))


create_folders = folder_gui()
