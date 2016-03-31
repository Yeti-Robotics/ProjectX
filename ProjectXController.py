import time
import RPi.GPIO as GPIO
import socket

GPIO.setmode(GPIO.BCM)

data = None
timeout = 3 # timeout in seconds
host = "192.168.1.113"
print ("Connecting to " + host)
port = 23
s = socket(AF_INET, SOCK_STREAM)
print "Socket made"
ready = select.select([s],[],[],timeout)
s.connect((host,port))
print("Connection made")


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if ((adcnum > 7) or (adcnum < 0)):
		return -1
	GPIO.output(cspin, True)

	GPIO.output(clockpin, False)  # start clock low
	GPIO.output(cspin, False)     # bring CS low

	commandout = adcnum
	commandout |= 0x18  # start bit + single-ended bit
	commandout <<= 3    # we only need to send 5 bits here
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		commandout <<= 1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)

	adcout = 0
	# read in one empty bit, one null bit and 10 ADC bits
	for i in range(12):
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		adcout <<= 1
		if (GPIO.input(misopin)):
			adcout |= 0x1

	GPIO.output(cspin, True)

	adcout >>= 1       # first bit is 'null' so drop it
	return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK_1 = 18
SPIMISO_1 = 23
SPIMOSI_1 = 24
SPICS_1 = 25

SPICLK_2 = 18
SPIMISO_2 = 23
SPIMOSI_2 = 24
SPICS_2 = 25


# set up the SPI interface pins
GPIO.setup(SPIMOSI_1, GPIO.OUT)
GPIO.setup(SPIMISO_1, GPIO.IN)
GPIO.setup(SPICLK_1, GPIO.OUT)
GPIO.setup(SPICS_1, GPIO.OUT)

GPIO.setup(SPIMOSI_2, GPIO.OUT)
GPIO.setup(SPIMISO_2, GPIO.IN)
GPIO.setup(SPICLK_2, GPIO.OUT)
GPIO.setup(SPICS_2, GPIO.OUT)


# 10k trim pot connected to adc #0
left_joy_adc = 0
right_joy_adc = 1

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

while True:
	# read the analog pin
	left_joy_value = readadc(left_joy_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	right_joy_value = readadc(right_joy_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

	left_joy_sendable = (127 / 1023) | 128
	right_joy_sendable = (127 / 1023)

	if ready[0]:        #if data is actually available for you
		print("[INFO] Sending message...")
		s.sendall(chr(left_joy_sendable))
		s.sendall(chr(right_joy_sendable))
		print("[INFO] Message sent.")
		time.sleep(0.5)
