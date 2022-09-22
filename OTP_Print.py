import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7735 # pylint: disable=unused-import

import RPi.GPIO as GPIO
from time import sleep

# First define some constants to allow easy resizing of shapes.
FONTSIZE = 24
# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D18)
reset_pin = digitalio.DigitalInOut(board.D23)
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()
disp = st7735.ST7735R(spi, rotation=0, # 1.8" ST7735R

 cs=cs_pin,
 dc=dc_pin,
 rst=reset_pin,
 baudrate=BAUDRATE,
)

class keypad():
    # CONSTANTS
    KEYPAD = [
        [1,   2,   3],
        [4,   5,   6],
        [7,   8,   9],
        ["*", 0, "#"]
    ]

    COLUMN      = [4,17,22]
    ROW         = [18,23,24,25]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def getKey(self):
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return

        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 3.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j

        # if colVal is not 0 thru 3 then no button was pressed and we can exit
        if colVal < 0 or colVal > 3:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]

    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()
def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 
# Getting digit 1, printing it, then sleep to allow the next digit press.
d1 = digit()
sleep(0.2)

d2 = digit()
sleep(0.2)

d3 = digit()
sleep(0.2)

d4 = digit()
sleep(0.2)

d5 = digit()
sleep(0.2)

d6 = digit()

if disp.rotation % 180 == 90:
 height = disp.width # we swap height/width to rotate it to landscape!
 width = disp.height
else:
 width = disp.width # we swap height/width to rotate it to landscape!
 height = disp.height
image = Image.new("RGB", (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
FONTSIZE)

# Draw Some Text
text = "%s%s%s%s%s%s"%(d1,d2,d3,d4,d5,d6)
(font_width, font_height) = font.getsize(text)
draw.text(
 (width // 2 - font_width // 2, height // 1.5 - font_height // 2),
 text,
 font=font,
 fill=(0, 0, 255),
)
# Display image.
disp.image(image)