# Project-Dead_Reckoning_Robot
This project includes a self-autonomous robot which uses dead-reckoning as a localization technique to identify its current position using pre-determined measures like speed, distance and time.

## Project Overview
This project aims to develop a probabilistic mapping system for a robot powered by an ESP32 microcontroller and equipped with a VL53L0X distance sensor. It facilitates real-time, interactive mapping of the robot's environment using a log-odds probability method, and visually tracks the robot's position and surroundings during operation.

# Hardware Requirements
ESP32 Microcontroller
VL53L0X Distance Sensor
DC Motors with Motor Driver
Wireless Connectivity

# Software Requirements
ESP32 Firmware
Enables the ESP32 to function as a Wi-Fi access point
Manages motor controls, sensor data acquisition, and command processing
Python Mapping Application
Displays a real-time interactive grid of the robot's environment
Performs probabilistic mapping of the surroundings
Allows robot movement via keyboard controls

# Key Features
Log-odds Mapping Algorithm: Uses probabilistic logic to represent the environment's state based on sensor data.
Interactive Grid Visualization: A real-time graphical representation of the robot's environment, with dynamic updates.
Real-Time Data Processing: Continuous updates to the robot's position and sensor readings.
Customizable Parameters: Allows users to adjust grid size, cell size, sensor settings, and mapping tolerances.
Visualized Robot Movement: Tracks the robot’s position on the grid as it moves.

# Prerequisites
Hardware
ESP32 Development Board
VL53L0X Distance Sensor
Motor Driver
DC Motors
Software
Python 3.7 or higher

# Required Libraries:
matplotlib
numpy
socket
keyboard

# Usage
Setting up the ESP32
Enter the Wi-Fi credentials in the ESP32 firmware.
Upload the firmware to the ESP32.
Ensure the ESP32 is broadcasting a Wi-Fi network.
Running the Mapping Program
Connect to the ESP32’s Wi-Fi network.
Execute the Python script:
bash
Copy
python robot_mapper.py
Follow the on-screen instructions to:
Configure mapping parameters
Control the robot’s movement
Visualize the mapping process
Keyboard Controls
Arrow Keys: Move the robot
'R': Capture a sensor reading
'ESC': Stop the robot and exit the program
Customizable Mapping Settings
The application provides options to configure:

Grid size and resolution
Sensor position
Initial probability values
Tolerance for measurement uncertainty
Probabilistic Mapping Process
The system applies log-odds transformation to:

Address sensor inaccuracies
Adjust cell probabilities based on readings
Represent the environment probabilistically
Visualization Features
Dynamic grid display
Color-coded probability heatmap for environment representation
Real-time position updates of the robot on the map
