# Motor Control Interface - README

This document describes the Python code (`Motor_Control_Interface.py`) used to control the motor in the experimental setup for the research paper "非传统磁悬浮动力学和稳定性研究" (Dynamics and Stability of Nontrivial Inter-Magnetic Levitation)[cite: 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 54].

## Overview

The `Motor_Control_Interface.py` script provides a user interface to control the ODrive motor, which is a crucial component of the experimental setup described in Section 2.1.1 and 4.2 of the paper[cite: 54, 19]. The motor is used to control the rotation of the small magnet that induces levitation[cite: 54]. This script also handles data logging and visualization of motor performance.

## Functionality

The script performs the following main functions:

* **Motor Control:** Allows the user to set and control the motor's position, velocity, and torque using the ODrive library.
* **Data Acquisition:** Records motor data, including time, velocity, position, torque, and current.
* **Data Logging:** Saves the acquired data to an Excel file for further analysis.
* **Data Visualization:** Plots the motor data to provide a visual representation of its performance.

## Dependencies

The script requires the following Python libraries:

* `odrive`:  For controlling the ODrive motor.
* `pandas`: For data manipulation and saving to Excel.
* `matplotlib.pyplot`: For plotting data.
* `time`: For time-related functions.
* `os`: For interacting with the operating system (e.g., creating directories).

## Code Description

The script contains the following key functions:

* `save_data_to_excel(time_data, velocity_data, position_data, torque_data, current_data, folder_path)`: Saves the motor data to an Excel file.
* `input_float(prompt)`:  Takes user input and converts it to a float, with error handling.
* `input_int(prompt)`: Takes user input and converts it to an integer, with error handling.
* `plot_motor_data(time_data, velocity_data, position_data, torque_data, current_data)`:  Plots the motor data (velocity, position, torque, current) against time.
* The main program section initializes the ODrive connection, interacts with the user to get control parameters, controls the motor, acquires data, saves the data, and plots the results.

## Relationship to the Research Paper

The `Motor_Control_Interface.py` script is directly related to the experimental work described in the research paper "非传统磁悬浮动力学和稳定性研究".

* It is used to control the "795型号直流碳刷电机" mentioned in Section 2.1.1, which is a key part of the experimental setup[cite: 54].
* The accurate control of the motor's rotation speed is crucial for investigating the relationship between the rotor's rotation speed and the levitation height and precession angle of the floating magnet, as discussed in Section 2.4 and throughout the paper[cite: 58].
* The data acquisition and logging capabilities of the script are essential for obtaining the quantitative data needed to validate the theoretical model and analyze the system's dynamics.

##  Notes

* This script assumes that the ODrive is properly set up and connected.
* Users may need to modify the script to adjust control parameters or data analysis routines based on their specific experimental requirements.
* Refer to the ODrive documentation for details on the ODrive library and its functions.

## References

* Chen, J.Y., Fan, M.J., Ji, Y.Q., Li, L., & Ma, C.C. (2024). 非传统磁悬浮动力学和稳定性研究 (Dynamics and Stability of Nontrivial Inter-Magnetic Levitation).
* `Motor_Control_Interface.py` (This file)