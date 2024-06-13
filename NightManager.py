import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import subprocess
from datetime import datetime, timedelta

class NightManager():
    WINDOW_WIDTH = 550
    WINDOW_HEIGHT = 610
    
    FONT = "Arial"
    FONT_SIZE = 20
    BTN_FONT_SIZE = 25
    
    def __init__(self):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.title("Night Guardian")
        self.root.resizable(False, False)
        
        position_right = int(self.root.winfo_screenwidth() / 2 - self.WINDOW_WIDTH / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - self.WINDOW_HEIGHT / 2)
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{position_right}+{position_down}')
        
        self.create_frame()
        self.root.mainloop()
        

    def create_frame(self):
        # create the main frame
        self.frame = ctk.CTkFrame(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        self.frame.place(x=0, y=0)
        
        
        # create logo on top of window
        print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png"))
        logo = ctk.CTkImage(dark_image=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")), size=(240, 240))
        logo_label = ctk.CTkLabel(self.frame, image=logo, text="")
        logo_label.place(relx=0.5, y=10,  anchor="n")
        
        
        # create settings outer frame
        settingsFrame = ctk.CTkFrame(self.frame, width=self.WINDOW_WIDTH, height=240)
        settingsFrame.place(relx=0.5, y=375, anchor="center")
        
        
        # create settings inner frames (activation, warning, snooze, difficulty)
        activationFrame = ctk.CTkFrame(settingsFrame, width=self.WINDOW_WIDTH, height=60)
        activationFrame.place(relx=0.5, y=0, anchor="n")
        
        warningFrame = ctk.CTkFrame(settingsFrame, width=self.WINDOW_WIDTH, height=60)
        warningFrame.place(relx=0.5, y=60, anchor="n")
        
        snoozeFrame = ctk.CTkFrame(settingsFrame, width=self.WINDOW_WIDTH, height=60)
        snoozeFrame.place(relx=0.5, y=120, anchor="n")
        
        difficultyFrame = ctk.CTkFrame(settingsFrame, width=self.WINDOW_WIDTH, height=60)
        difficultyFrame.place(relx=0.5, y=180, anchor="n")
        
        
        # create settings items
        activationLabel = ctk.CTkLabel(activationFrame, text="Activation Time", font=(self.FONT, self.FONT_SIZE))
        activationLabel.place(relx=0.2, rely=0.5, anchor="w")
        self.activationOption = ctk.CTkOptionMenu(activationFrame, values=["20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30","00:00","00:30","01:00","01:30","02:00","02:30","03:00"], font=(self.FONT, self.FONT_SIZE))
        self.activationOption.place(relx=0.8, rely=0.5, anchor="e")
        
        # create warning items
        warningLabel = ctk.CTkLabel(warningFrame, text="Warning", font=(self.FONT, self.FONT_SIZE))
        warningLabel.place(relx=0.2, rely=0.5, anchor="w")
        self.warningOption = ctk.CTkOptionMenu(warningFrame, values=["5 min.","10 min.","15 min.","20 min.","25 min.","30 min."], font=(self.FONT, self.FONT_SIZE))
        self.warningOption.place(relx=0.8, rely=0.5, anchor="e")
        
        # create snooze items
        snoozeLabel = ctk.CTkLabel(snoozeFrame, text="Snooze", font=(self.FONT, self.FONT_SIZE))
        snoozeLabel.place(relx=0.2, rely=0.5, anchor="w")
        self.snoozeOption = ctk.CTkOptionMenu(snoozeFrame, values=["15 min.","30 min.","45 min.","60 min.","75 min.","90 min.","120 min."], font=(self.FONT, self.FONT_SIZE))
        self.snoozeOption.place(relx=0.8, rely=0.5, anchor="e")
        
        # create difficulty items
        difficultyLabel = ctk.CTkLabel(difficultyFrame, text="Difficulty", font=(self.FONT, self.FONT_SIZE))
        difficultyLabel.place(relx=0.2, rely=0.5, anchor="w")
        self.difficultyOption = ctk.CTkOptionMenu(difficultyFrame, values=["Easy","Medium","Hard"], font=(self.FONT, self.FONT_SIZE))
        self.difficultyOption.place(relx=0.8, rely=0.5, anchor="e")
        
        
        # create button frame
        buttonFrame = ctk.CTkFrame(self.frame, width=self.WINDOW_WIDTH, height=80)
        buttonFrame.place(relx=0.5, y=self.WINDOW_HEIGHT, anchor="s")
        
        # create deploy button
        deploy_button = ctk.CTkButton(buttonFrame, text="Deploy Guardian", font=(self.FONT, self.BTN_FONT_SIZE), command=self.deploy_guardian)
        deploy_button.place(relx=0.25, rely=0.5, anchor="center")
        
        # create remove button
        remove_button = ctk.CTkButton(buttonFrame, text="Remove Guardian", font=(self.FONT, self.BTN_FONT_SIZE), command=self.remove_guardian)
        remove_button.place(relx=0.75, rely=0.5, anchor="center")


    def deploy_guardian(self):
        task_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "NightEnforcer", "NightEnforcer.exe")
        
        task_time = datetime.strptime(self.activationOption._current_value, "%H:%M")
        task_time = task_time - timedelta(minutes=int(self.warningOption._current_value.strip(" min.")))
        task_time = task_time.strftime("%H:%M")
        
        match self.difficultyOption._current_value:
            case "Medium":
                difficulty = 1
            case "Hard":
                difficulty = 2
            case _:
                difficulty = 0
            
        task_args = f"{self.activationOption._current_value} {self.warningOption._current_value.strip(" min.")} {self.snoozeOption._current_value.strip(" min.")} {difficulty}"
                
        schtasks_command = f'schtasks /create /tn "Night Guardian" /tr "{task_path} {task_args}" /sc daily /st {task_time} /f'
        
        try:
            subprocess.run(schtasks_command, check=True, shell=True, capture_output=True, text=True)
            messagebox.showinfo("Night Guardian", "The Night Guardian is now active.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Night Guardian", "Something went wrong.")



    def remove_guardian(self):
        try:
            
            subprocess.run(f'schtasks /delete /tn "Night Guardian" /f', check=True, shell=True, capture_output=True, text=True)
            messagebox.showinfo("Night Guardian", "The Night Guardian is now taking a break.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Night Guardian", "Either someting went wrong or the Night Guardian is already inactive.")
            
        try:
            subprocess.run(f'schtasks /delete /tn "Nightshift Guardian" /f', check=True, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            pass

        try:
            subprocess.run(f'schtasks /delete /tn "Night Enforcer" /f', check=True, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            pass



def main():
    NightManager()

if __name__ == "__main__":
    main()