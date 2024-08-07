import board  # type: ignore
import digitalio
from adafruit_hid.mouse import Mouse
import usb_hid
import asyncio
import random

# Define the onboard LED pin
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Define the external button pin
button = digitalio.DigitalInOut(board.GP22)  # External button is connected to GP22
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Initialize the mouse
mouse = Mouse(usb_hid.devices)

# Initial state of the LED
led_state = True
led.value = led_state

# Initial state of the mouse jiggler
jiggler_active = False

print(f"Initial LED status: {led_state}")
print(f"Initial mouse jiggler status: {jiggler_active}")

async def jiggle_mouse():
    # Move the mouse a random amount in both directions within the range [-10, 10]
    move_x = random.randint(-10, 10)
    move_y = random.randint(-10, 10)
    
    mouse.move(x=move_x, y=move_y)
    await asyncio.sleep(0.1)

    # Move the mouse back to its original position
    mouse.move(x=-move_x, y=-move_y)
    await asyncio.sleep(0.1)

# Define a flag to control the while loop
run_loop = False

async def loop():
    global run_loop
    while True:
        if run_loop:
            # Place the code to run in the loop here
            print("Loop is running...")
            await jiggle_mouse()
        else:
            await asyncio.sleep(0.1)  # Yield control to the main function

async def main():
    global run_loop
    print("Press the button to start/stop the loop.")
    last_button_state = button.value
    while True:
        button_state = button.value
        if button_state != last_button_state:
            if not button_state:  # Button pressed
                run_loop = not run_loop  # Toggle the loop flag
                if run_loop:
                    print("Starting the loop...")
                else:
                    print("Stopping the loop...")
            last_button_state = button_state
        
        await asyncio.sleep(0.1)  # Small delay to debounce the button

async def run_program():
    await asyncio.gather(main(), loop())

# Start the asyncio event loop
asyncio.run(run_program())

