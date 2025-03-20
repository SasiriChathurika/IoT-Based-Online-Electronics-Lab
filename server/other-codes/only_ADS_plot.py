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

# Initialize a figure and axis for plotting
fig, ax = plt.subplots()

# Loop to read the analog inputs continuously
while True:
    voltage0 = channel0.voltage
    voltage1 = channel1.voltage
    
    # Append voltage values to the lists
    voltage0_values.append(voltage0)
    voltage1_values.append(voltage1)
    
    # Plot the values
    ax.clear()
    ax.plot(voltage0_values, label='Voltage 0')
    ax.plot(voltage1_values, label='Voltage 1')
    ax.set_xlabel('Time')
    ax.set_ylabel('Voltage (V)')
    ax.legend()
    plt.pause(0.000001)  # Update the plot every 0.1 seconds
    
    # Print the values to console
    print("Voltage 0: ", voltage0)
    print("Voltage 1: ", voltage1)
    
    # Delay for 1 second
    time.sleep(0.000001)
