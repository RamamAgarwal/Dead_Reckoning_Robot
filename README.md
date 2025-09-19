# 🚗 **Project-Dead_Reckoning_Robot** 🤖

This project demonstrates a **self-autonomous robot** that uses **dead-reckoning** as its primary localization technique. By leveraging **speed, distance**, and **time**, the robot estimates its position and navigates in an environment. It's powered by an **ESP32** microcontroller and equipped with a **VL53L0X** distance sensor, all working together to build a **probabilistic mapping system**.

---

## 📜 **Project Overview**

This project aims to create an interactive and real-time mapping system for a robot, utilizing probabilistic methods to track its position and surroundings. By combining the **ESP32 microcontroller** and **VL53L0X sensor**, we use the **log-odds** probability technique to generate an **interactive environment map**. The robot's journey is visualized in real-time on a grid, giving users full control and insight into its movements and mapped surroundings.

---

## 🛠️ **Hardware Requirements**

- **ESP32 Microcontroller** - The brain of the robot!
- **VL53L0X Distance Sensor** - Measures distance for environment scanning.
- **DC Motors with Motor Driver** - Enables movement of the robot.
- **Wireless Connectivity** - For communication between the robot and the Python application.

---

## 💻 **Software Requirements**

- **ESP32 Firmware**  
  - Makes the ESP32 function as a Wi-Fi access point
  - Manages motor control, sensor data acquisition, and command processing

- **Python Mapping Application**  
  - Real-time interactive mapping of the robot’s environment
  - Visualizes robot's movement and surroundings

---

## ✨ **Key Features**

- **Log-odds Mapping Algorithm**  
  Uses probabilistic logic to represent the environment based on sensor data.

- **Interactive Grid Visualization**  
  A real-time graphical representation of the robot's environment, constantly updated.

- **Real-Time Data Processing**  
  Continuous updates for position tracking and sensor readings.

- **Customizable Parameters**  
  Adjust grid size, cell size, sensor settings, and mapping tolerances to suit your needs.

- **Visualized Robot Movement**  
  Track the robot’s position on the grid as it navigates in real time.

---

## 📋 **Prerequisites**

### Hardware
- **ESP32 Development Board**
- **VL53L0X Distance Sensor**
- **Motor Driver (L298N or equivalent)**
- **DC Motors**
  
### Software
- **Python 3.7+**
  
### Required Libraries
```bash
pip install matplotlib numpy socket keyboard
