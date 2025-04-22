import time
import pandas as pd
import os
import matplotlib.pyplot as plt
import odrive
from odrive.enums import *

def save_data_to_excel(time_data, velocity_data, position_data, torque_data, current_data, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    df = pd.DataFrame({
        'Time (s)': time_data,
        'Velocity (counts/s)': velocity_data,
        'Position (counts)': position_data,
        'Torque (Nm)': torque_data,
        'Current (A)': current_data
    })
    
    filename = f"motor_data_{int(time.time())}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Data saved to {filename} at {file_path}")

def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def plot_motor_data(time_data, velocity_data, position_data, torque_data, current_data):
    plt.figure(figsize=(20, 10))

    plt.subplot(2, 2, 1)
    plt.plot(time_data, velocity_data, label='Velocity')
    plt.title('Motor Velocity Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (counts/s)')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(time_data, position_data, label='Position', color='red')
    plt.title('Motor Position Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (counts)')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(time_data, torque_data, label='Torque', color='green')
    plt.title('Motor Torque Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Torque (Nm)')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(time_data, current_data, label='Current', color='blue')
    plt.title('Motor Current Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ------------ Program Start ------------
print("------------- Designed and Powered By Jason Chen  -------------")
print("\n")
print("                 NONTRIVIAL MAGNETIC LEVITATION                ")
print("                 Motor Control Interface v4.0                  ")
print("\nSystem Initiating")

odrv0 = odrive.find_any()
odrv0.axis1.clear_errors()
print("Connecting...\n")

# Static Config (edit only if needed)
odrv0.axis0.motor.config.current_lim = 60
odrv0.axis0.controller.config.vel_limit = 40
odrv0.config.dc_bus_undervoltage_trip_level = 20
odrv0.config.dc_bus_overvoltage_trip_level = 26
odrv0.axis1.motor.config.pole_pairs = 7
odrv0.axis1.motor.config.torque_constant = 0.04
odrv0.axis1.encoder.config.cpr = 4000
odrv0.axis1.controller.config.pos_gain = 3
odrv0.axis1.controller.config.vel_gain = 0.08
odrv0.axis1.controller.config.vel_integrator_gain = 0.45
time.sleep(0.25)
odrv0.save_configuration()
time.sleep(1)
odrv0.axis1.clear_errors()
odrv0.save_configuration()

print("System Armed. Waiting for Instructions...\n")


# Check if system has error before entering loop
if odrv0.axis1.error != 0:
    print("System initiation failed! If this message persists, unplug and replug the battery.")
    exit()

# Optional motor calibration
motorCalibrate = input("Do you wish to calibrate the motor? You must calibrate the motor after a restart. (Y/N): ")
if motorCalibrate.upper() == "Y":
    print("The motor is being calibrated. Please wait.")
    odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while odrv0.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.2)
        print(".", end="")
    if odrv0.axis1.error != 0:
        print("Calibration Failed. If this message persists, unplug and replug the battery.")
        exit()


# === Experiment Loop ===
while True:
    try:
        print("\n---- Experiment Session Created ----")
        odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

        # User input
        velocity_limit = input_float("Enter the velocity (1-45 rev/s): ")
        run_time = input_float("Enter the run time (s): ")
        target_position_rev = velocity_limit * run_time

        odrv0.axis1.controller.config.vel_limit = velocity_limit
        odrv0.axis1.controller.input_pos = odrv0.axis1.encoder.pos_estimate + target_position_rev

        time.sleep(0.25)

        # Data containers
        velocity_data = []
        position_data = []
        torque_data = []
        current_data = []
        time_data = []
        start_time = time.time()

        print("\nData collection started. Press Ctrl+C to stop the session.")

        while True:
            current_time = time.time() - start_time
            current_position = odrv0.axis1.encoder.pos_estimate
            velocity = odrv0.axis1.encoder.vel_estimate 
            Iq_measured = odrv0.axis1.motor.current_control.Iq_measured
            torque = 8.27 * Iq_measured / 120

            print(f"Time: {current_time:.2f}s | Pos: {current_position:.0f} | Spd: {velocity:.2f} | Torque: {torque:.2f} Nm | Current: {Iq_measured:.2f} A")

            position_data.append(current_position)
            velocity_data.append(velocity)
            torque_data.append(torque)
            current_data.append(Iq_measured)
            time_data.append(current_time)

            if current_position >= odrv0.axis1.encoder.pos_estimate + target_position_rev:
                break

            time.sleep(0.005)  # Sampling rate

    except KeyboardInterrupt:
        print("\nData collection stopped.")
    
    finally:
        odrv0.axis1.requested_state = AXIS_STATE_IDLE
        folder_path = os.path.expanduser('~/Downloads/motor_data_logs')
        save_data_to_excel(time_data, velocity_data, position_data, torque_data, current_data, folder_path)
        print("\n Data has been saved to ~/Downloads/motor_data_logs")
        plot_motor_data(time_data, velocity_data, position_data, torque_data, current_data)

        restart = input("\n Press [Q] to quit. Press any key to proceed.")
        if restart.upper() == "Q":
            print("Exiting")
            print("Thank you for using Nontrivial Maglev Motor Control Interface")
            break
