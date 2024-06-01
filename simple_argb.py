import time
import board
import neopixel

# LED strip configuration
LED_COUNT = 30         # Number of LED pixels.
LED_PIN = board.D20    # GPIO pin connected to the pixels (18 uses PWM!).

# Create a NeoPixel object with appropriate configuration.
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write=False)

def color_wipe(color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(LED_COUNT):
        pixels[i] = color
        pixels.show()
        time.sleep(wait_ms / 1000.0)

def rainbow_cycle(wait_ms=20):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(255):
        for i in range(LED_COUNT):
            pixel_index = (i * 256 // LED_COUNT) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait_ms / 1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

if __name__ == '__main__':
    try:
        while True:
            print('Color wipe red')
            color_wipe((255, 0, 0))  # Red wipe
            print('Color wipe green')
            color_wipe((0, 255, 0))  # Green wipe
            print('Color wipe blue')
            color_wipe((0, 0, 255))  # Blue wipe
            print('Rainbow cycle')
            rainbow_cycle()  # Rainbow cycle
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("Program terminated and LEDs turned off.")
