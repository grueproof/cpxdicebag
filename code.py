import audioio
import board
import digitalio
import neopixel
import random
import math
import time

# Colors
RED = 0x100000  # (0x10, 0, 0) also works
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)

# init the neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()

# enable the speaker
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True

# make the 2 input buttons
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.direction = digitalio.Direction.INPUT
buttonA.pull = digitalio.Pull.DOWN

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.direction = digitalio.Direction.INPUT
buttonB.pull = digitalio.Pull.DOWN

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

def play_file(filename):
    print("Playing file: " + filename)
    wave_file = open(filename, "rb")
    with audioio.WaveFile(wave_file) as wave:
        with audioio.AudioOut(board.A0) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    print("Finished")

def roll(max,times=1, each_roll=0,end_add=0):
    play_file('diceroll.wav')
    total = 0
    for index in range(0,times):
        total += random.randint(1, max) + each_roll
    return total

def init_pixels():
    pixels.fill((0, 0, 0))
    pixels.show()

def roll_to_hit():
    init_pixels()
    total = roll(20)

    print("Total: %s" % total)

    # do the math for showing a red light for 10, and green lights for 1
    tens = math.floor(total/10)
    remain = total%10

    for i in range(0,tens+remain):
        if i<=tens-1:
            #red light
            pixels[i]=RED
        else:
            pixels[i]=GREEN

    if total==1:
        pixels.fill(RED)
        play_file("laugh.wav")

    if total==20:
        play_file("fanfare.wav")
        rainbow_cycle(.001)



while True:
    if buttonA.value:
        roll_to_hit()
    if buttonB.value:
        init_pixels()
