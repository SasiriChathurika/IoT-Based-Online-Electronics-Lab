import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter
from numpy import dot, array, eye

# Kalman filter parameters
dt = 1.0  # Time step
kf = KalmanFilter(dim_x=2, dim_z=1)
kf.x = array([[0.0], [0.0]])  # Initial state (mean)
kf.F = array([[1, dt], [0, 1]])  # State transition matrix
kf.H = array([[1.0, 0.0]])  # Measurement function
kf.P *= 1000.0  # Covariance matrix
kf.R = 10  # Measurement noise covariance
kf.Q = eye(kf.dim_x) * 0.001  # Process noise covariance

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

# Loop to read the analog inputs continuously
while True:
    voltage0 = channel0.voltage
    voltage1 = channel1.voltage
    
    # Kalman filtering
    kf.predict()
    kf.update(voltage0)
    voltage0_filtered = kf.x[0, 0]
    
    kf.predict()
    kf.update(voltage1)
    voltage1_filtered = kf.x[0, 0]
    
    kf.predict()
    kf.update(voltage0 * voltage1-4.25)
    product_filtered = kf.x[0, 0]
    
    # Append filtered voltage values to the lists
    voltage0_values.append(voltage0_filtered)
    voltage1_values.append(voltage1_filtered)
    product_values.append(product_filtered)
    
    # Plot the values
    ax.clear()
    #ax.plot(voltage0_values, label='Voltage 0 (Filtered)')
    #ax.plot(voltage1_values, label='Voltage 1 (Filtered)')
    ax.plot(product_values, label='Product of Voltage 0 and Voltage 1 (Filtered)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Filtered Voltage (V)')
    ax.legend()
    plt.pause(0.000001)  # Update the plot every 0.1 seconds
    
    # Print the values to console
    print("Voltage 0 (Filtered): ", voltage0_filtered)
    print("Voltage 1 (Filtered): ", voltage1_filtered)
    print("Product of Voltage 0 and Voltage 1 (Filtered): ", product_filtered)
    
    # Delay for 1 second
    time.sleep(0.000001)
