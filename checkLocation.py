import tkinter as tk
import subprocess
import json
import threading
from typing import final

CHECK_INTERVAL: final = 1
NETWORK_ERROR: final = 10

def checkLocation(TargetCity):

    curl_cmd = ['curl', 'ipinfo.io']
    response = subprocess.run(curl_cmd, stdout=subprocess.PIPE)

    if response.returncode == 0:
        # print("Command ran successfully!")
        response_json = json.loads(response.stdout)
        CurrentCity = response_json["city"]

        if CurrentCity == TargetCity:
            return True
        else:
            return False
    else:
        # print(f"Command failed with return code {response.returncode}")
        return NETWORK_ERROR
    
def CheckLocationRegualarly():
    StartButton.config(state=tk.DISABLED)
    City.config(state=tk.DISABLED)
    TargetCity = City.get()

    if not continue_checking:   # check if the function should exit
        StartButton.config(state=tk.NORMAL)
        City.config(state=tk.NORMAL)
        return
    
    response = checkLocation(TargetCity);
    if response == NETWORK_ERROR:
        status_label.config(foreground="black", justify="center")
        status_text.set("Network Error")
    elif response == True:
        status_label.config(foreground="black", justify="center")
        status_text.set("Ok")
    else :
        status_label.config(foreground="red", justify="center")
        status_text.set("You are dangerous")

    threading.Timer(CHECK_INTERVAL, CheckLocationRegualarly).start()

# start the timer event
def StartChecking():
    global continue_checking   # use the global flag
    continue_checking = True
    CheckLocationRegualarly()

def StopChecking():
    global continue_checking   # use the global flag
    continue_checking = False

    # re-enable the input fields and update the status text
    StartButton.config(state=tk.NORMAL)
    City.config(state=tk.NORMAL)
    status_label.config(foreground="black", justify="center")
    status_text.set("Checking stopped")

root = tk.Tk()

StartButton = tk.Button(root, text="My Location must be", command=StartChecking)
StartButton.pack()

City = tk.Entry(root, width=30)
City.pack()

StopButton = tk.Button(root, text="Stop", command=StopChecking)
StopButton.pack()

status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text)
status_label.pack()

root.mainloop()