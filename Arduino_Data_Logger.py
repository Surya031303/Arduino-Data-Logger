"""
Surya's Arduino Data Logger

Author: Suryanarayana

This script logs data from an Arduino connected to the specified COM port.

"""

import serial
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox
from threading import Thread

# Global variable to track the logging state
logging_state = False

# Serial object for communication
ser = None

# Function to start data logging in a separate thread
def start_logging_thread():
    global logging_state
    global ser

    if logging_state:
        print("Logging is already in progress.")
        return

    # Define the serial port and baud rate
    selected_com_port = com_port.get()
    ser = serial.Serial(selected_com_port, 9600)

    # Create a file with the specified file path
    file_name = file_entry.get()
    file_format = format_dropdown.get()
    file_path = os.path.join(folder_path.get(), file_name + file_format)

    try:
        with open(file_path, 'w') as file:
            logging_state = True
            while logging_state:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip()

                # Print and write the received data to the file
                print(line)
                file.write(line + '\n')

                # Update the data preview in the GUI
                update_data_preview(line)

    except KeyboardInterrupt:
        stop_logging()

# Function to update the data preview in the GUI
def update_data_preview(line):
    data_preview.config(state=tk.NORMAL)

    # Display each word in a separate column if there's a space in the line
    words = line.split()
    for word in words:
        data_preview.insert(tk.END, word + '\t')  # Use '\t' for a tab space between columns
    data_preview.insert(tk.END, '\n')

    data_preview.see(tk.END)  # Scroll to the end
    data_preview.config(state=tk.DISABLED)

# Function to start logging in a new thread
def start_logging():
    global logging_thread
    logging_thread = Thread(target=start_logging_thread)
    logging_thread.start()

# Function to stop data logging
def stop_logging():
    global logging_state
    global ser

    if not logging_state:
        print("Logging is not in progress.")
        return

    logging_state = False

    # Close the serial port
    if ser:
        ser.close()
        print("Logging stopped. Serial port closed.")
    else:
        print("Logging stopped.")

# Function to retrieve available COM ports
def get_available_com_ports():
    ports = []
    for i in range(256):
        try:
            s = serial.Serial("COM" + str(i))  # Convert to string and add "COM" prefix
            ports.append(s.name)
            s.close()
        except serial.SerialException:
            pass
    return ports

# Function to update COM port dropdown with available ports
def update_com_ports():
    com_ports = get_available_com_ports()
    com_port_dropdown['values'] = com_ports

# Function to update Subfolder dropdown based on user's choice
def update_subfolders(event):
    selected_folder = folder_path.get()
    subfolder_dropdown['values'] = os.listdir(selected_folder)

# Function to select the folder for saving data
def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)
    update_subfolders(None)  # Update subfolders dropdown when the folder entry loses focus

# Create the main GUI window
root = tk.Tk()
root.title("Surya's Arduino Data Logger")

# Set the window size
root.geometry("1000x800")

# Variables
folder_path = tk.StringVar()
com_port = tk.StringVar()

# Widgets
label_com_port = tk.Label(root, text="Select COM Port:", fg="black")
label_com_port.grid(row=0, column=0, padx=10, pady=5, sticky="w")

com_port_dropdown = Combobox(root, textvariable=com_port, width=20)
com_port_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

update_com_ports()  # Initial update of available COM ports

label_folder = tk.Label(root, text="Select Folder:", fg="black")
label_folder.grid(row=1, column=0, padx=10, pady=5, sticky="w")

folder_entry = tk.Entry(root, textvariable=folder_path, width=30)
folder_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

browse_button = tk.Button(root, text="Browse", command=select_folder, width=10, bg="orange", fg="white")
browse_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

label_file = tk.Label(root, text="Enter File Name:", fg="black")
label_file.grid(row=2, column=0, padx=10, pady=5, sticky="w")

file_entry = tk.Entry(root, width=30)
file_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

label_format = tk.Label(root, text="Select/Type File Format:", fg="black")
label_format.grid(row=3, column=0, padx=10, pady=5, sticky="w")

formats = [".xls", ".dat", ".txt", ".xlsx", ".csv"]  # Add more formats as needed
format_dropdown = Combobox(root, values=formats, width=5)
format_dropdown.set(".dat")  # Set a default format
format_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

folder_entry.bind("<FocusOut>", update_subfolders)  # Update subfolders dropdown when the folder entry loses focus

# Data preview text widget at the bottom
data_preview = tk.Text(root, wrap=tk.WORD, width=120, height=25, state=tk.DISABLED, bg="lightgrey")
data_preview.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="w")

# Start and Stop Logging buttons centered at the bottom with smoothed edges
start_button = tk.Button(root, text="Start Logging", command=start_logging, bg="green", fg="white", width=15,
                         borderwidth=3, relief="raised")
start_button.grid(row=6, column=0, columnspan=3, pady=10, sticky="n", padx=10)

stop_button = tk.Button(root, text="Stop Logging", command=stop_logging, bg="red", fg="white", width=15,
                        borderwidth=3, relief="raised")
stop_button.grid(row=7, column=0, columnspan=3, pady=10, sticky="n", padx=10)

# Function to be called when the window is closed
def on_closing():
    stop_logging()
    root.destroy()

# Configure the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
root.mainloop()
