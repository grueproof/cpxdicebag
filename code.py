import random
import math
import time
from adafruit_circuitplayground.express import cpx

# Colors
RED = 0x100000  # (0x10, 0, 0) also works
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos * 3)), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int((i * 256 / len(pixels)) + j * 10)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)

def roll(max,times=1, each_roll=0,end_add=0):
    cpx.play_file('diceroll.wav')
    total = 0
    for index in range(0,times):
        total += random.randint(1, max) + each_roll
    return total

def display_roll_value(total):
    # do the math for showing a red light for 10, and green lights for 1
    tens = math.floor(total/10)
    remain = total%10

    for i in range(0,tens+remain):
        if i<=tens-1:
            #red light
            pixels[i]=RED
        else:
            pixels[i]=GREEN

def init_pixels():
    pixels.fill((0, 0, 0))
    pixels.show()

def roll_to_hit():
    init_pixels()
    total = roll(20)

    print("Total: %s" % total)

    display_roll_value(total)

    if total==1:
        pixels.fill(RED)
        cpx.play_file("laugh.wav")

    if total==20:
        cpx.play_file("fanfare.wav")
        rainbow_cycle(.001)

# init the neopixels
pixels = cpx.pixels
pixels.fill((0, 0, 0))
pixels.show()

while True:
    if cpx.shake(13):
       roll_to_hit()
    if cpx.button_a:
        roll_to_hit()
    if cpx.button_b:
        init_pixels()
