import tkinter as tk
import subprocess
import json
import threading
import wmi
import sys
import pythoncom

from tkinter import messagebox

from typing import final

CHECK_INTERVAL: final = 1
NETWORK_ERROR: final = 10

if sys.platform == "win32":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("checkLocationTask")
    ctypes.windll.kernel32.SetDllDirectoryW(None)
    ctypes.windll.shell32.IsUserAnAdmin()

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
        status_text.set("Network Error")
        status_label.config(foreground="black", justify="center")
        root.after(CHECK_INTERVAL*1000, CheckLocationRegualarly)
    elif response == True:
        status_text.set("Ok")
        status_label.config(foreground="black", justify="center")
        root.after(CHECK_INTERVAL*1000, CheckLocationRegualarly)
    else :
        status_label.config(foreground="red", justify="center")
        disable_network_adapters()
        messagebox.showwarning("Alert", "Your Location is changed\n All your adapters are disabled")
        status_text.set("You are dangerous")

    # threading.Timer(CHECK_INTERVAL, CheckLocationRegualarly).start()

# start the timer event
def StartChecking():
    global continue_checking   # use the global flag
    continue_checking = True
    try:
        CheckLocationRegualarly()
    except KeyboardInterrupt:
        StopChecking()
        root.quit()

def StopChecking():
    global continue_checking   # use the global flag
    continue_checking = False

    # re-enable the input fields and update the status text
    StartButton.config(state=tk.NORMAL)
    City.config(state=tk.NORMAL)
    status_label.config(foreground="black", justify="center")
    status_text.set("Checking stopped")

def disable_network_adapters():
    adapters = get_network_adapter_names()
    for adapter in adapters:
        print(adapter)
        cmd = ['netsh', 'interface', 'set', 'interface', adapter, 'disable']
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print("Network adapter disabled successfully")
            else:
                print(f"Failed to disable network adapter: {result.stderr.decode('utf-8')}")
        except KeyboardInterrupt:
            StopChecking()
            root.quit()


def get_network_adapter_names():
    adapters = []
    pythoncom.CoInitialize()  # initialize pythoncom
    c = wmi.WMI()
    for adapter in c.Win32_NetworkAdapter():
        if adapter.NetConnectionID:
            adapters.append(adapter.NetConnectionID)
    return adapters

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

try:
    root.mainloop()
except KeyboardInterrupt:
    pass