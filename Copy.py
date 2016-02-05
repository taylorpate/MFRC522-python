#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

continue_reading = True
write_mode = False
card_data = []

#populate card data w/ defaults
for x in range(0,16):
    card_data.append(0x00)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Capture each sector of the scanned card
        for x in range(0,16):
            card_data[x] = MIFAREReader.MFRC522_Read(x)

        # Stop
        MIFAREReader.MFRC522_StopCrypto1()

        # Switch to write mode
        continue_reading = False
        write_mode = True

for x in range(5, 1, -1):
    print 'Switching to write mode in ' + str(x) + ' seconds...'
    time.sleep(1)

while write_mode:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Fill data w/ captured result from previous read
        for x in range(0,16):
            MIFAREReader.MFRC522_Write(x, card_data[x])

        # Stop
        MIFAREReader.MFRC522_StopCrypto1()

        # Make sure to stop reading for cards
        write_mode = False

print 'Completed Copy'
