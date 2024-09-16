import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import matplotlib.pyplot as plt

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object
ads = ADS.ADS1115(i2c)

# Define the analog input channels
channel0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P1)

# Create lists to store voltage values
voltage0_values = []
voltage1_values = []
product_values = []  # New list to store product of voltage0 and voltage1

# Initialize a figure and axis for plotting
fig, ax = plt.subplots()

# Define the number of measurements to average
num_measurements = 10
measurement_window = []

# Loop to read the analog inputs continuously
while True:
    voltage0 = channel0.voltage
    voltage1 = channel1.voltage
    
    # Add the new measurement to the window
    measurement_window.append(voltage0 * voltage1 - 3.25)
    
    # Keep the window size constant
    if len(measurement_window) > num_measurements:
        measurement_window.pop(0)
    
    # Calculate the average of the measurements in the window
    product_filtered = sum(measurement_window) / len(measurement_window)
    
    # Append filtered voltage values to the lists
    voltage0_values.append(voltage0)
    voltage1_values.append(voltage1)
    product_values.append(product_filtered)
    
    # Plot the values
    ax.clear()
    ax.plot(product_values, label='Product of Voltage 0 and Voltage 1 (Filtered)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Filtered Voltage (V)')
    ax.legend()
    plt.pause(0.000001)  # Update the plot every 0.1 seconds
    
    # Print the values to console
    print("Product of Voltage 0 and Voltage 1 (Filtered): ", product_filtered)
    
    # Delay for a short time
    time.sleep(0.1)
