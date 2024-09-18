import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox, simpledialog
import os
import watchdog.events
from shutil import move

alphabet= "qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM."

class Programme():
    def __init__(self):
        self.winH = 300
        self.winW= 600
        self.running = False
        self.background_thread = None
        self.input_folder_path= None
        
        
    def _exe_Win_Start(self, folder_exist = True):
        self.win = tk.Tk()
        self.win.title("Sortigo cleaner")
        self.win.minsize(self.winW, self.winH)
        self.win.maxsize(self.winW, self.winH)
        self.center_Window(self.win)
        if folder_exist:
            welcome_Lbl = ttk.Label(self.win, text="Welcome to Sortigo", font=("Verdana",16))
            welcome_Lbl.place(relx=0.5,rely=0.25, anchor='n')
        else:
            error_Lbl = ttk.Label(self.win, text="This folder does not exist or none were chosen", font=("Verdana",12))
            error_Lbl.place(relx=0.5, rely=0.25, anchor='n')
        
        start_Btn = ttk.Button(self.win, text="Chose foder to clean/sort" ,command=self.start_Button_Clicked, width=20, padding=5)
        
        start_Btn.place(relx=0.5,rely=0.40, anchor='n')
                
        self.win.mainloop()
        
    def start_Button_Clicked(self):
        for widget in self.win.winfo_children():
            widget.destroy()
        
        self.input_folder_path = filedialog.askdirectory(title="Choose folder to clean/sort")
        if self.input_folder_path == None or not os.path.exists(self.input_folder_path):
            self.win.destroy()
            self._exe_Win_Start(False)
            
        else:
            self._main_Option_Screen_UI()
            
    def _main_Option_Screen_UI(self):
        btn_Widht = 15
        option_Lbl= ttk.Label(self.win, text="Choose the option for files autoclean:", font=(("Verdana",16)))
        option_Lbl.place(relx=0.5,rely=0.2, anchor='n')
        
        warning_Lbl = ttk.Label(self.win, text="Warning: The Name- and Mixed cleaning may take a long time to execute and may not work properly")
        warning_Lbl.place(relx =0.5,rely=0.8,anchor='n')
        warning_Lbl.config(foreground ="red")
        
        file_cleaner= File_cleaner()
        name_Clean_Btn =ttk.Button(self.win,text="Clean by Name", command= lambda: file_cleaner.name_based_cleaning(self.input_folder_path), width=btn_Widht)
        name_Clean_Btn.place(relx=0.2, rely=0.4, anchor='n')
        
        file_Typ_Clean_Btn = ttk.Button(self.win, text="Clean by Filetype", command= lambda: file_cleaner.type_based_cleaning(self.input_folder_path) ,width=btn_Widht)
        file_Typ_Clean_Btn.place(relx=0.4,rely=0.4, anchor='n')
        
        mixed_Vlean_Btn =ttk.Button(self.win, text= "Mixed Cleaning", command=lambda: file_cleaner.mixed_cleaning(self.input_folder_path),width=btn_Widht)
        mixed_Vlean_Btn.place(relx=0.6, rely=0.4, anchor='n')
        
        name_Filter_Clean_Btn= ttk.Button(self.win, text="Adjustable name Clean", command =lambda:file_cleaner.adjustable_name_cleaning(self.input_folder_path, self.get_input_str()),width=btn_Widht)
        name_Filter_Clean_Btn.place(relx = 0.8, rely= 0.4, anchor='n')
        
                
    def center_Window(self,window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def programme_has_ended(self):
        messagebox.showinfo("Sortigo feedback", "The programme has ended with no error")
        exit()
    
    def get_input_str(self):
        user_input = simpledialog.askstring("Input desired filename", "Enter the name")
        return user_input
        
    
class Background_activity():
    def __init__(self):
        return None      
    
    def start():
        return None
    
    def stop():
        return None
    

    
class File_cleaner():
    def __init__(self):
        return None
    
    def find_file_with_string_in_name(self, folder_path, target_string):
        
        for file in os.listdir(folder_path):
            
            if os.path.isfile(os.path.join(folder_path, file)):
            
                if target_string in file:
                    
                    return os.path.join(folder_path, file)
    
    def get_files_in_directory(self, dir_path): # returns all the files in directory
        return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,f))]
    
    def name_based_cleaning(self, folder_path):
        files = self.get_files_in_directory(folder_path)
        separator ="    "
        files_string = separator.join(files)
        self.MINPATLEN = 7 #minimul lenght of pattern
        self.MINPATOCC = 4 #minimum number of occurences of pattern
        return_dict={}
        
        
        
        for sublen in range(self.MINPATLEN, int(len(files_string)/self.MINPATOCC)): # the loop represent pattern finder algorith
            for i in range(0,len(files_string)-sublen):
                sub = files_string[i:i+sublen]
                cnt = files_string.count(sub)
                if cnt >= self.MINPATOCC and len(sub.strip()) >= self.MINPATLEN and len(sub.replace("-","").replace(".","").replace(" ","").strip("_")) >= self.MINPATLEN and sub.replace("-","").replace(".","").replace(" ","").strip("_") not in return_dict and separator not in sub.replace("_","").replace("-","").replace(".","").replace(" ","") and "." not in sub:
                    return_dict[sub.replace("-","").replace(" ","").strip("_")] = cnt
        
        
        dict_items = list(return_dict.items())
        sorted_dict_items = sorted(dict_items,key=lambda x: (x[0][0].islower(), -len(x[0]), x))
        
        
        desired_path =os.path.join(folder_path, "Python_name_based_sorted_files")
        if  not os.path.exists(desired_path):
            os.mkdir(desired_path)
        
        for item in files:# am trying file moving system
            for thing in sorted_dict_items:
                dir_name = thing[0] 
                    
                path = self.find_file_with_string_in_name(folder_path, dir_name)
                    
                if not os.path.exists(os.path.join(desired_path, folder_path)):
                    os.mkdir(os.path.join(desired_path, folder_path))
                    
                if path != None and not os.path.exists(os.path.join(desired_path, folder_path, dir_name)):
                    
                    move(path, os.path.join(desired_path, folder_path, dir_name))
                    
        
        Programme().programme_has_ended()
                            
            

    def type_based_cleaning(self,folder_path):
        files = self.get_files_in_directory(folder_path)
        for file in files:
            file_extention = file[file.rfind('.'):]
            if not os.path.exists(os.path.join(folder_path, file_extention)):
                os.mkdir(os.path.join(folder_path, file_extention))
                
            move(os.path.join(folder_path, file),  os.path.join(folder_path, file_extention))
        
        Programme().programme_has_ended()
            
    def mixed_cleaning(self,folder_path):
        self.name_based_cleaning(folder_path)
        self.type_based_cleaning(folder_path)
        Programme().programme_has_ended()
    
    def adjustable_name_cleaning(self,folder_path, string_val):
      
        files = self.get_files_in_directory(folder_path)
        for file in files:
            if string_val in file:
                dir_name = string_val  # use string_val as the directory name
                dir_path = os.path.join(folder_path, dir_name)
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)  # create the directory
                move(os.path.join(folder_path, file), os.path.join(dir_path, file))  # move the file into the directory
        
        Programme().programme_has_ended()

def run_program():
    programme = Programme()
    programme._exe_Win_Start()

run_program()

    
