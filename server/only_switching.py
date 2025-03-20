import time
import RPi.GPIO as GPIO

# Define GPIO pin mappings
pin_mappings = {f'{type}_{label}': pin for type, pins in [('L', [6, 19]), ('C', [16, 26]), ('R', [20, 21])] for label, pin in zip(['A', 'B'], pins)}

# Define switch configurations
switches = {
    'L1': (False, False), 'L2': (True, False), 'L3': (False, True), 'L4': (True, True),
    'C1': (False, False), 'C2': (True, False), 'C3': (False, True), 'C4': (True, True),
    'R1': (False, False), 'R2': (True, False), 'R3': (False, True), 'R4': (True, True)
}

def setup_gpio():
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Suppress GPIO warnings
    for pin_number in pin_mappings.values():
        GPIO.setup(pin_number, GPIO.OUT)

def configure_switch(switch_key):
    for switch_type in ['L', 'C', 'R']:
        switch_a, switch_b = switches[switch_key]
        GPIO.output(pin_mappings[f'{switch_type}_A'], switch_a)
        GPIO.output(pin_mappings[f'{switch_type}_B'], switch_b)

def main():
    setup_gpio()

    initial_config = ('L1', 'C3', 'R4')  # Example initial switch configuration

    try:
        while True:
            for switch in initial_config:
                configure_switch(switch)
                time.sleep(0.000001)

    finally:
        # Clean up GPIO
        GPIO.cleanup()

if __name__ == "__main__":
    main()
