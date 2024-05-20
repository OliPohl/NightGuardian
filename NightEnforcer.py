import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import subprocess
from datetime import datetime, timedelta
import sys
import random


class NightEnforcer():
    WINDOW_WIDTH = 650
    WINDOW_HEIGHT = 400
    
    FONT = "Arial"
    FONT_SIZE = 20
    BTN_FONT_SIZE = 25
    
    def __init__(self):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.title("Night Guardian")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        
        # Calculate the position for the window to be centered
        position_right = int(self.root.winfo_screenwidth() / 2 - self.WINDOW_WIDTH / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - self.WINDOW_HEIGHT / 2)
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{position_right}+{position_down}')
        
        self.activationTime = sys.argv[1]
        self.warningTime = int(sys.argv[2])
        self.snoozeTime = int(sys.argv[3])
        self.difficulty = int(sys.argv[4])
        
        self.deploy_enforcer()
        self.create_frame()
        self.root.mainloop()


    def create_frame(self):
        self.frame = ctk.CTkFrame(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, border_color="dodger blue4", border_width=5)
        self.frame.place(x=0, y=0)

        # create logo on side of the window
        logo = ctk.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")), size=(240, 240))
        logo_label = ctk.CTkLabel(self.frame, image=logo, text="")
        logo_label.place(x=160, y=160,  anchor="center")
        
        # create text outer frame
        text_frame = ctk.CTkFrame(self.frame, width=340, height=self.WINDOW_HEIGHT-80, fg_color="gray13")
        text_frame.place(relx=0.992, y=5, anchor="ne")
        
        # create math frame
        math_frame = ctk.CTkFrame(text_frame, width=300, height=130, fg_color="gray20", border_color="dodger blue4", border_width=5)
        math_frame.place(relx=0.5, y=170, anchor="n")
        
        # create text label
        text_label = ctk.CTkLabel(text_frame, text=f"Your computer will shutdown at {self.activationTime} o'clock.", font=(self.FONT, self.FONT_SIZE), wraplength=290)
        text_label.place(relx=0.5, y=20, anchor="n")
    
        # create math label
        text_math_label = ctk.CTkLabel(text_frame, text=f"Solve this math problem to extend your time by {self.snoozeTime} minutes.", font=(self.FONT, self.FONT_SIZE),wraplength=290)
        text_math_label.place(relx=0.5, y=110, anchor="n")
        
        # create math problem
        self.curMath = self.create_math_problem()
        self.math_label = ctk.CTkLabel(math_frame, text=self.curMath[0], font=(self.FONT, self.BTN_FONT_SIZE))
        self.math_label.place(relx=0.5, rely=0.3, anchor="center")
        
        # create math entry
        self.math_entry = ctk.CTkEntry(math_frame, font=(self.FONT, self.FONT_SIZE), width=130)
        self.math_entry.place(relx=0.1, rely=0.7, anchor="w")
        
        self.math_button = ctk.CTkButton(math_frame, text="Submit", font=(self.FONT, self.BTN_FONT_SIZE), width=100, command=self.solve_math_problem)
        self.math_button.place(relx=0.9, rely=0.7, anchor="e")
        
        
        # create button frame
        button_frame = ctk.CTkFrame(self.frame, width=self.WINDOW_WIDTH-10, height=75)
        button_frame.place(relx=0.5, y=self.WINDOW_HEIGHT-5, anchor="s")
        
        # create deploy button
        ok_button = ctk.CTkButton(button_frame, text="OK", font=(self.FONT, self.BTN_FONT_SIZE), command=self.root.destroy)
        ok_button.place(relx=0.27, rely=0.5, anchor="center")
        
        # create remove button
        self.extend_button = ctk.CTkButton(button_frame, text="Extend time", font=(self.FONT, self.BTN_FONT_SIZE), state="disabled", command=self.extend_time)
        self.extend_button.place(relx=0.73, rely=0.5, anchor="center")
        
        
    def create_math_problem(self):
        if self.difficulty == 0:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            return [f"{num1} + {num2} = ?", str(num1 + num2)]
        elif self.difficulty == 1:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            return [f"{num1} + {num2} = ?", str(num1 + num2)]
        elif self.difficulty == 2:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            return [f"{num1} * {num2} = ?", str(num1 * num2)]
        
    
    def solve_math_problem(self):
        curEntry = self.math_entry.get().strip()
        
        if self.curMath[1] == curEntry:
            self.extend_button.configure(state="normal")
            self.math_button.configure(state="disabled")
            self.math_entry.configure(state="disabled")
        elif not curEntry:
            pass
        else:
            self.curMath = self.create_math_problem()
            self.math_label.configure(text=self.curMath[0])

            
    def extend_time(self):
        self.deploy_guardian()
        
        try:
            subprocess.run(f'schtasks /delete /tn "Night Enforcer" /f', check=True, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Night Guardian", "Something went wrong.")
        
        self.root.destroy()
        
    
    def deploy_guardian(self):
        self.activationTime = datetime.strptime(self.activationTime, "%H:%M") + timedelta(minutes=self.snoozeTime)
        self.activationTime = self.activationTime.strftime("%H:%M")
        
        task_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "NightEnforcer.exe")
        
        task_time = datetime.strptime(self.activationTime, "%H:%M")
        task_time = task_time - timedelta(minutes=self.warningTime)
        task_time = task_time.strftime("%H:%M")
        
        task_args = f"{self.activationTime} {self.warningTime} {self.snoozeTime} {self.difficulty}"
        
        schtasks_command = f'schtasks /create /tn "Nightshift Guardian" /tr "{task_path} {task_args}" /sc once /st "{task_time}" /f'
        
        try:
            subprocess.run(schtasks_command, check=True, shell=True, capture_output=True, text=True)
            messagebox.showinfo("Success", f"Time extended by {self.snoozeTime} minutes.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Night Guardian", "Something went wrong.")
            
            
    def deploy_enforcer(self):
        shutdown_command = "shutdown.exe /s /f /t 0"
        schtasks_command = f'schtasks /create /tn "Night Enforcer" /tr "{shutdown_command}" /sc once /st "{self.activationTime}" /f'
        
        try:
            subprocess.run(schtasks_command, check=True, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            
            messagebox.showerror("Night Guardian", "Something went wrong." + str(e))




def main():
    NightEnforcer()


if __name__ == "__main__":
    main()