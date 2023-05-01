import tkinter as tk
import time as tm
import subprocess
import json
from typing import final

GREEN = '\033[32m'
RESET = '\033[0m'

CHECK_INTERVAL: final = 1
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
        return False
    
def CheckLocationRegualarly():
    TargetCity = City.get()
    while True:
        tm.sleep(CHECK_INTERVAL)
        if checkLocation(TargetCity):
            status_label.config(foreground="black", justify="center")
            status_text.set("Ok")
        else :
            status_label.config(foreground="red", justify="center")
            status_text.set("You are dangerous")

root = tk.Tk()

StartButton = tk.Button(root, text="My Location must be ", command=CheckLocationRegualarly)
StartButton.pack()

City = tk.Entry(root, width=30)
City.pack()


status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text)
status_label.pack()

status_text.set("You are dangerous")


root.mainloop()