import time
import RPi.GPIO as GPIO
import spidev

# MCP4131 commands
WRITE_CMD = 0x00
SHUTDOWN_CMD = 0b00100000
POTENTIOMETER_0 = 0x00

class MCP4131:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0b00

    def set_resistance(self, resistance):
        # Calculate wiper position (0 to 255)
        wiper_position = int((resistance / 10000) * 255)
        wiper_position = max(0, min(wiper_position, 255))  # Clamp within 0-255 range

        # Send command to update potentiometer value
        self.spi.xfer2([WRITE_CMD, (POTENTIOMETER_0 << 4) | (wiper_position & 0x0F)])

    def shutdown(self, shutdown=True):
        # Send shutdown command
        cmd = SHUTDOWN_CMD | (not shutdown)
        self.spi.xfer2([cmd])

    def __del__(self):
        self.spi.close()

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings

# Create MCP4131 instance
mcp = MCP4131(bus=0, device=0)

try:
    while True:
        # Set initial frequency (1 kHz)
        #mcp.set_resistance(1000)

        # Wait for 5 seconds
        #time.sleep(5)

        # Set new frequency (2 kHz)
        mcp.set_resistance(10)

        # Wait for 5 seconds
        time.sleep(0.000001)

finally:
    # Clean up GPIO
    GPIO.cleanup()
    del mcp  # Clean up MCP4131 SPI communication
