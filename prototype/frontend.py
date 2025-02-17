import tkinter as tk
import threading
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
from file_handling import create_excel
from assessment import ReadingAssessment


logo = Image.open('sample.png')
logo = logo.resize((300, 300))

class TessFrontEnd(tk.Tk, Student, ReadingAssessment):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.student = Student()
        self.test = ReadingAssessment()
        self.geometry("1000x700")
        self.minsize(1000, 700)
        self.maxsize(1000, 700)
        self.title("Tess Reading Assessment")
        self.configure(bg = "#012b09")

        self.old_frame = ttk.Frame()
        self.fetch_new_frame(self.old_frame, StartPage)  

    def fetch_new_frame(self, old, new):
        old.destroy()
        
        return new(self)

class StartPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        ttk.Frame.__init__(self, parent) 

        self.logo = ImageTk.PhotoImage(logo)

        style = ttk.Style()

        style.theme_use('classic')

        style.configure('TFrame', 
                        background = '#ffffff')

        style.configure('TButton', 
                        font = ('Arial', 15, 'bold'), 
                        borderwidth = 0, 
                        background = "#d4af37", 
                        foreground = "white")
        style.configure('TLabel',
                        font = ("Arial", 15),
                        background = "#ffffff",
                        foreground = "black")
        style.configure('TEntry',
                        font = ("Arial", 15),
                        borderwidth = 0,
                        fieldbackground = "#94bb86",
                        background = "#94bb86",
                        foreground = "black",
                        padding = 5)
        style.map('TButton',
                    highlightcolor = '#0000',
                    foreground = [('active', '!disabled', 'white'),
                                    ("disabled", 'grey')], 
                    background = [('active', '!disabled', '#012b09'),
                                    ('disabled' , '#f7ebe2')])

        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.schl = tk.StringVar()
        self.instructor_name = tk.StringVar()
        self.instructor_id = tk.StringVar()

        logo_label = tk.Label(self, image = self.logo, bg="#ffffff", anchor = tk.CENTER)
        banner_label = tk.Label(self, text="Input Student Information", bg = "#ffffff", font = ("Arial", 20, "bold"), anchor = tk.CENTER)
        fname_label = ttk.Label(self, text="Firstname : ", style = 'TLabel')
        self.fname_input = ttk.Entry(self, textvariable=self.fname, style = 'TEntry')
        lname_label = ttk.Label(self, text="Lastname : ", style = 'TLabel')
        self.lname_input = ttk.Entry(self, textvariable=self.lname, style = 'TEntry')
        school_label = ttk.Label(self, text="School : ", style = 'TLabel')
        self.school_input = ttk.Entry(self, textvariable=self.schl, style = 'TEntry')
        instructor_name_label = ttk.Label(self, text="Instructor Name: ", style='TLabel')
        self.instructor_name_input = ttk.Entry(self, textvariable=self.instructor_name, style='TEntry')
        instructor_id_label = ttk.Label(self, text="Instructor ID: ", style='TLabel')
        self.instructor_id_input = ttk.Entry(self, textvariable=self.instructor_id, style='TEntry')
        self.register_bttn = ttk.Button(self, text="REGISTER", style = 'TButton', state = 'disabled', command = lambda: [self.create_student_data(), parent.fetch_new_frame(self, PageOne)])

        logo_label.grid(row = 0, column = 0, columnspan = 4, rowspan = 3, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 10)
        banner_label.grid(row = 3, column = 0, columnspan = 4, sticky = tk.W+tk.E, pady = 5, padx = 10)
        fname_label.grid(row = 4, column = 0, sticky = tk.W+tk.E, pady = 5, padx = 10)
        self.fname_input.grid(row = 4, column = 1, sticky = tk.W+tk.E+tk.N+tk.S, pady = 5, padx = 10)
        lname_label.grid(row = 4, column = 2, sticky = tk.W+tk.E, pady = 5, padx = 10)
        self.lname_input.grid(row = 4, column = 3, sticky = tk.W+tk.E+tk.N+tk.S, pady = 5, padx = 10)
        school_label.grid(row = 6, column = 0, sticky = tk.W+tk.E, pady = 5, padx = 10)
        self.school_input.grid(row = 6, column = 1, columnspan = 3, sticky = tk.W+tk.E+tk.N+tk.S, pady = 5, padx = 10)
        instructor_name_label.grid(row=8, column=0, sticky=tk.W+tk.E, pady=5, padx=10)
        self.instructor_name_input.grid(row=8, column=1, columnspan = 3, sticky=tk.W+tk.E+tk.N+tk.S, pady=5, padx=10)
        instructor_id_label.grid(row=9, column=0, sticky=tk.W+tk.E, pady=5, padx=10)
        self.instructor_id_input.grid(row=9, column=1, columnspan = 3, sticky=tk.W+tk.E+tk.N+tk.S, pady=5, padx=10)
        self.register_bttn.grid(row = 10, column = 0, columnspan = 4, sticky = tk.W+tk.E, pady = 20, padx = 10)

        self.fname.trace('w', self.enable_button)
        self.lname.trace('w', self.enable_button)
        self.schl.trace('w', self.enable_button)
        self.instructor_name.trace('w', self.enable_button)
        self.instructor_id.trace('w', self.enable_button)

        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)

    def create_student_data(self):

        self.firstname = self.fname_input.get()
        self.lastname = self.lname_input.get()
        self.school = self.school_input.get()

        self.parent.student.set_student_info(self.firstname, self.lastname, self.school)

        return 

    def enable_button(self, firstname, lastname, school):
        if ((len(self.fname_input.get()) > 0) and (len(self.lname_input.get()) > 0) and (len(self.school_input.get()) > 0)):
            self.register_bttn.state(['!disabled'])
        else:
            self.register_bttn.state(['disabled'])


#start_frame = ttk.Frame(root)
class PageOne(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ttk.Frame.__init__(self, parent)

        style = ttk.Style()

        style.theme_use('classic')

        style.configure('TFrame', 
                        background = '#ffffff')

        style.map('TButton',
                    highlightcolor = '#0000',
                    foreground = [('active', '!disabled', 'white'),
                                    ("disabled", 'grey')], 
                    background = [('active', '!disabled', '#012b09'),
                                    ('disabled' , '#f7ebe2')])

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.logo = ImageTk.PhotoImage(logo)

        fname = self.parent.student.get_firstname()

        logo_label = tk.Label(self, image = self.logo, bg="#ffffff", anchor = tk.CENTER)
        message_label = tk.Label(self, text=("hi " + fname + "!"), bg = "#94bb86", font = ("Arial", 20, "bold"), anchor = tk.CENTER)
        ins_label = tk.Label(self, text=("say \"START\" to begin assessment"), bg = "#94bb86", font = ("Arial", 20, "bold"), anchor = tk.CENTER)

        logo_label.grid(row = 0, column = 0, columnspan = 4, rowspan = 2, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 10)
        message_label.grid(row = 2, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 20)
        ins_label.grid(row = 3, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)
        
        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)

        que = threading.Thread(target = self.wait_for_command)
        que.start()

    def wait_for_command(self):
        self.parent.test.wait_for_start()
        self.parent.fetch_new_frame(self, PageTwo)
        return

class PageTwo(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ttk.Frame.__init__(self, parent)

        style = ttk.Style()

        style.theme_use('clam')

        style.configure('TFrame', 
                        background = '#ffffff')
        style.configure('TLabel',
                        bordercolor = "#012b09",
                        background = "#94bb86",
                        foreground = "black",
                        padding = 20)
        style.configure("yellow.Horizontal.TProgressBar",
                        troughcolor = "yellow",
                        background = "yellow")
        style.configure('Yellow.TButton', 
                        background='yellow', 
                        foreground='black')
        style.configure('Red.TButton', 
                        background='red', 
                        foreground='white')

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.logo = ImageTk.PhotoImage(logo)

        self.ins_label = ttk.Label(self, text = "Read the word below: ", font = ("Arial", 30), style = "TLabel")
        self.word = ttk.Label(self, text = "WORD", font = ("Arial", 50, "bold"), anchor = tk.CENTER, borderwidth = 10, style = "TLabel")
        self.progress = ttk.Progressbar(self, style = 'yellow.Horizontal.TProgressbar', orient = "horizontal", mode = "determinate", maximum=200, value=0)
        self.skip_button = ttk.Button(self, text="Skip", style='Yellow.TButton', command=self.skip_test)
        self.stop_button = ttk.Button(self, text="Stop", style='Red.TButton', command=self.stop_test)

        self.ins_label.grid(row = 0, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)
        self.word.grid(row = 1, column = 0, columnspan = 4, rowspan = 2, sticky = tk.W+tk.E+tk.N+tk.S, padx = 20)
        
        self.skip_button.grid(row=3, column=1, sticky=tk.W+tk.E, pady=10, padx=10)
        self.stop_button.grid(row=3, column=2, sticky=tk.W+tk.E, pady=10, padx=10)
        self.progress.grid(row = 4, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)

        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)

        self.display = threading.Thread(target = self.display_test_word)
        self.display.start()

    def display_test_word(self):
        result = self.parent.test.setup_test([self.ins_label, self.word, self.progress])
        self.parent.student.set_result(result)
        self.parent.fetch_new_frame(self, PageThree)
        return
    
    def skip_test(self):
        print("Test skipped.")
    
    def stop_test(self):
        print("Test stopped.")

class PageThree(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        ttk.Frame.__init__(self, parent)

        style = ttk.Style()

        style.theme_use('classic')

        style.configure('TFrame', 
                        background = '#ffffff')

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.logo = ImageTk.PhotoImage(logo)

        fname = self.parent.student.get_firstname()

        que = threading.Thread(target = create_excel(fname, self.parent.student.get_lastname(), self.parent.student.get_school(), self.parent.student.get_result()))
        que.start()

        logo_label = tk.Label(self, image = self.logo, bg="#ffffff", anchor = tk.CENTER)
        message_label = tk.Label(self, text=("Thank You " + fname + "!"), bg = "#94bb86", font = ("Arial", 20, "bold"), anchor = tk.CENTER)
        ins_label = tk.Label(self, text=("Assessment Completed!"), bg = "#94bb86", font = ("Arial", 20, "bold"), anchor = tk.CENTER)
        new_bttn = ttk.Button(self, text="Start New Test", style = 'TButton', command = lambda: parent.fetch_new_frame(self, StartPage))
        
        new_bttn.grid(row = 4, column = 1, columnspan = 2, sticky = tk.W+tk.E, pady = 20, padx = 10)
        logo_label.grid(row = 0, column = 0, columnspan = 4, rowspan = 2, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 10)
        message_label.grid(row = 2, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 20)
        ins_label.grid(row = 3, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)
        
        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)
