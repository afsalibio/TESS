import tkinter as tk
import threading
import sys
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
from file_handling import create_excel
from assessment import ReadingAssessment
#from tkinter import Toplevel

global pause_screen
global logo

class TessFrontEnd(tk.Tk, Student, ReadingAssessment):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.student = Student()
        self.test = ReadingAssessment()
        self.geometry("1000x700")
        self.minsize(1000, 700)
        self.maxsize(1000, 700)
        self.title("TESS Reading Assessment")
        self.iconphoto(False, tk.PhotoImage(file="TESS.png"))
        self.iconbitmap("TESS.ico")
        self.configure(bg = "#012b09")

        self.logo = Image.open('TESS.png')
        self.logo = self.logo.resize((400, 400))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.old_frame = ttk.Frame()
        self.fetch_new_frame(self.old_frame, StartPage)  

    def fetch_new_frame(self, old, new):
        old.destroy()
        frame = new(self)
        frame.pack(fill=tk.BOTH, expand=True)  # This ensures the frame is displayed
        return frame
    
    def reset(self):
        self.student = Student()
        self.test = ReadingAssessment()
        return
    
    def on_closing(self):
        """Ensure complete shutdown on window close."""
        self.test.force_close()  # Stop the test process first

        # Wait for any running threads to finish before destroying the window
        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                thread.join(timeout=1)  # Give threads 1 second to finish

        self.quit()   # Stop Tkinter mainloop
        self.destroy()  # Destroy all Tkinter widgets safely

        sys.exit(0)  # Exit the program

class StartPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        ttk.Frame.__init__(self, parent) 

        self.logo = ImageTk.PhotoImage(self.parent.logo)

        style = ttk.Style()

        style.theme_use('classic')

        style.configure('TFrame', 
                        background = '#ffffff')

        style.configure('TButton', 
                        font = ('Comic Sans MS', 15, 'bold'), 
                        borderwidth = 0, 
                        background = "#d4af37", 
                        foreground = "white")
        style.configure('TLabel',
                        font = ("Comic Sans MS", 15),
                        background = "#ffffff",
                        foreground = "black")
        style.configure('TEntry',
                        font = ("Comic Sans MS", 15),
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
        self.ins = tk.StringVar()
        self.insID = tk.StringVar()

        logo_label = tk.Label(self, image = self.logo, bg="#ffffff", anchor = tk.CENTER)
        banner_label = tk.Label(self, text="Input Student Information", bg = "#ffffff", font = ("Comic Sans MS", 20, "bold"), anchor = tk.CENTER)
        fname_label = ttk.Label(self, text="Firstname : ", style = 'TLabel')
        self.fname_input = ttk.Entry(self, textvariable=self.fname, style = 'TEntry')
        lname_label = ttk.Label(self, text="Lastname : ", style = 'TLabel')
        self.lname_input = ttk.Entry(self, textvariable=self.lname, style = 'TEntry')
        school_label = ttk.Label(self, text="School : ", style = 'TLabel')
        self.school_input = ttk.Entry(self, textvariable=self.schl, style = 'TEntry')
        instructor_name_label = ttk.Label(self, text="Instructor Name: ", style='TLabel')
        self.instructor_name_input = ttk.Entry(self, textvariable=self.ins, style='TEntry')
        instructor_id_label = ttk.Label(self, text="Instructor ID: ", style='TLabel')
        self.instructor_id_input = ttk.Entry(self, textvariable=self.insID, style='TEntry')
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

        self.fname.trace_add('write', self.enable_button)
        self.lname.trace_add('write', self.enable_button)
        self.schl.trace_add('write', self.enable_button)
        self.ins.trace_add('write', self.enable_button)
        self.insID.trace_add('write', self.enable_button)

        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)

    def create_student_data(self):

        self.firstname = self.fname_input.get()
        self.lastname = self.lname_input.get()
        self.school = self.school_input.get()
        self.instructor_name = self.instructor_name_input.get()
        self.instructor_id = self.instructor_id_input.get()

        self.parent.student.set_student_info(self.firstname, self.lastname, self.school, self.instructor_name, self.instructor_id)

        return 

    def enable_button(self, *args):
        if ((len(self.fname_input.get()) > 0) and (len(self.lname_input.get()) > 0) and (len(self.school_input.get()) > 0) and (len(self.instructor_name_input.get()) > 0) and (len(self.instructor_id_input.get()) > 0)):
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

        self.logo = ImageTk.PhotoImage(self.parent.logo)

        fname = self.parent.student.get_firstname()

        logo_label = tk.Label(self, image = self.logo, bg="#ffffff", anchor = tk.CENTER)
        message_label = tk.Label(self, text=("hi " + fname + "!"), bg = "#94bb86", font = ("Comic Sans MS", 20, "bold"), anchor = tk.CENTER)
        ins_label = tk.Label(self, text=("say \"START\" to begin assessment"), bg = "#94bb86", font = ("Comic Sans MS", 20, "bold"), anchor = tk.CENTER)

        logo_label.grid(row = 0, column = 0, columnspan = 4, rowspan = 2, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 10)
        message_label.grid(row = 2, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 20)
        ins_label.grid(row = 3, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)
        
        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)

        que = threading.Thread(target = self.wait_for_command, daemon=True)
        que.start()

    def wait_for_command(self):
        self.parent.test.wait_for_start()  # Wait for "start" command
        self.parent.after(0, lambda: self.parent.fetch_new_frame(self, PageTwo))  # Safe Tkinter update

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
        style.configure("Yellow.Horizontal.TProgressbar",
                        troughcolor = "#d3d3d3",
                        background = "#d4af37")
        style.configure("Green.Horizontal.TProgressbar", 
                        troughcolor="#d3d3d3", 
                        background="#c6de70", 
                        thickness=20)
        style.configure('Green.TButton',
                        font = ('Comic Sans MS', 20, 'bold'),
                        highlightcolor = '#0000', 
                        background= 'green', 
                        foreground='black')
        style.configure('Yellow.TButton',
                        font = ('Comic Sans MS', 20, 'bold'),
                        highlightcolor = '#0000', 
                        background= '#d4af37', 
                        foreground='black')
        style.configure('Red.TButton',
                        font = ('Comic Sans MS', 20, 'bold'),
                        highlightcolor = '#0000', 
                        background='red', 
                        foreground='black')

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 1)
        self.columnconfigure(5, weight = 1)

        self.logo = ImageTk.PhotoImage(self.parent.logo)

        self.timer = ttk.Progressbar(self, mode="determinate", style = "Green.Horizontal.TProgressbar", maximum = 100, value = 100)
        self.word = ttk.Label(self, text = "WORD", font = ("Comic Sans MS", 50, "bold"), anchor = tk.CENTER, borderwidth = 10, style = "TLabel")
        self.progress = ttk.Progressbar(self, mode = "determinate", style = "Yellow.Horizontal.TProgressbar", maximum=200, value=0)
        self.skip_button = ttk.Button(self, text="SKIP", style='Green.TButton', command=self.skip_test)
        self.pause_button = ttk.Button(self, text="PAUSE", style='Yellow.TButton', command=self.pause_test)
        self.stop_button = ttk.Button(self, text="STOP", style='Red.TButton', command=self.stop_test)

        self.timer.grid(row = 0, column = 0, columnspan = 6, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)
        self.word.grid(row = 1, column = 0, columnspan = 6, rowspan = 3, sticky = tk.W+tk.E+tk.N+tk.S, padx = 20)
        
        self.skip_button.grid(row=4, column=0, columnspan = 2, sticky=tk.W+tk.E+tk.N+tk.S, pady=10, padx=20)
        self.pause_button.grid(row=4, column=2, columnspan = 2, sticky=tk.W+tk.E+tk.N+tk.S, pady=10, padx=0)
        self.stop_button.grid(row=4, column=4, columnspan = 2, sticky=tk.W+tk.E+tk.N+tk.S, pady=10, padx=20)
        self.progress.grid(row = 5, column = 0, columnspan = 6, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)

        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)

        self.display = threading.Thread(target = self.display_test_word, daemon=True)
        self.display.start()

    def show_pause_screen(self):
        # Create the pause screen
        self.pause_screen = tk.Toplevel(self)
        
        # Get the main window's position and size
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        width = self.winfo_width()
        height = self.winfo_height()

        self.pause_screen.geometry(f"{width}x{height}+{x}+{y}")
        self.pause_screen.overrideredirect(True)  # Removes title bar
        self.pause_screen.lift()
        self.pause_screen.focus_force()

        # Create a frame for UI elements
        frame = tk.Frame(self.pause_screen, bg="#94bb86")
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # UI Elements
        tess_label = tk.Label(frame, image=self.logo, bg="#94bb86")  
        word_label = ttk.Label(frame, text="PAUSED", font=("Comic Sans MS", 30, "bold"), background="#94bb86", foreground="black")
        
        # Button frame for side-by-side buttons
        button_frame = tk.Frame(frame, bg="#94bb86")

        resume_button = ttk.Button(button_frame, text="RESUME", style='Green.TButton', command=self.unpause_test)
        restart_button = ttk.Button(button_frame, text="RESTART", style='Yellow.TButton', 
                                    command=lambda: [self.parent.fetch_new_frame(self, StartPage), self.parent.reset()])

        # Pack elements
        tess_label.pack(pady=5)
        word_label.pack(pady=10)
        button_frame.pack(pady=10)  # Container for buttons
        resume_button.pack(side="left", padx=10, expand=True)
        restart_button.pack(side="left", padx=10, expand=True)

    def close_pause_screen(self):
        self.pause_screen.destroy()
        return

    def display_test_word(self):
        result = self.parent.test.setup_test([self.word, self.progress, self.timer])
        self.parent.student.set_result(result)
        self.parent.after(0, self.parent.fetch_new_frame, self, PageThree)
        return
    
    def skip_test(self):
        #print("Test skipped.")
        self.parent.test.force_skip()
        return
    
    def stop_test(self):
        #print("Test stopped.")
        self.parent.test.force_stop()
        return
    
    def pause_test(self):
        #print("Test paused.")
        self.parent.test.force_pause()
        self.show_pause_screen()
        return
    
    def unpause_test(self):
        #print("Test paused.")
        self.parent.test.force_unpause()
        self.close_pause_screen()
        return

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

        self.logo = ImageTk.PhotoImage(self.parent.logo)

        fname = self.parent.student.get_firstname()

        que = threading.Thread(target = create_excel(self.parent.student), daemon= True)
        que.start()

        logo_label = tk.Label(self, image = self.logo, bg="#ffffff", anchor = tk.CENTER)
        message_label = tk.Label(self, text=("Thank You " + fname + "!"), bg = "#94bb86", font = ("Comic Sans MS", 20, "bold"), anchor = tk.CENTER)
        ins_label = tk.Label(self, text=("Assessment Completed!"), bg = "#94bb86", font = ("Comic Sans MS", 20, "bold"), anchor = tk.CENTER)
        new_bttn = ttk.Button(self, text="Start New Test", style = 'TButton', command = lambda: [parent.fetch_new_frame(self, StartPage), parent.reset()])
        
        new_bttn.grid(row = 4, column = 1, columnspan = 2, sticky = tk.W+tk.E, pady = 20, padx = 10)
        logo_label.grid(row = 0, column = 0, columnspan = 4, rowspan = 2, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 10)
        message_label.grid(row = 2, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 10, padx = 20)
        ins_label.grid(row = 3, column = 0, columnspan = 4, sticky = tk.W+tk.E+tk.N+tk.S, pady = 20, padx = 20)
        
        self.pack(fill = tk.BOTH, expand = 1, padx = 20, pady = 20)
