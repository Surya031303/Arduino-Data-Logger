# Arduino Data Logger with Python GUI

This Python script provides a simple graphical user interface (GUI) for logging data from an Arduino or similar device via a serial connection. The GUI is implemented using the Tkinter library.

## Features:

1. **COM Port Selection:**
   - Users can select the COM port to which their Arduino or device is connected from a dropdown menu.

2. **Folder Selection:**
   - Users can choose a folder to save the log files. There is an option to browse and select the desired folder.

3. **File Name and Format:**
   - Users can specify the name of the log file and select its format (e.g., .dat, .txt, .xlsx, .csv) using dropdown menus.

4. **Start and Stop Logging Buttons:**
   - Two buttons are provided to start and stop the data logging process. The "Start Logging" button initiates a separate thread to continuously read data from the selected COM port and save it to the specified file.

5. **Data Preview:**
   - A text widget at the bottom of the GUI displays a real-time preview of the received data. Each word is displayed in a separate column, and a tab space is used as a separator between columns.

## Code Explanation:

- The code uses the `serial` library to establish communication with the Arduino via the selected COM port.
- Logging is done in a separate thread (`start_logging_thread`) to avoid blocking the main GUI thread.
- The `update_data_preview` function updates the data preview in the GUI as new data is received.
- The script provides functions to start and stop logging, update COM ports, update subfolders based on the selected folder, and select the folder for saving data.
- The GUI window is configured with labels, entry widgets, buttons, and a text widget for data preview.
- The script ensures proper closing of the serial port and stops the logging thread when the GUI window is closed.

## Usage:

1. Run the script.
2. Select the COM port, folder, enter the file name, and select the file format.
3. Click "Start Logging" to initiate data logging.
4. Real-time data preview is displayed in the GUI.
5. Click "Stop Logging" to stop the logging process.
6. Close the GUI window when done.

## Note:

- The script uses threads for logging to allow the GUI to remain responsive during data acquisition.
- Ensure that the required libraries (`serial`, `os`, `datetime`, `tkinter`) are installed before running the script.
