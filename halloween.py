from machine import Pin, I2C, ADC, I2S
from s2pico_oled import OLED
from time import sleep 
import time
import math
import struct

def speak():
    audio = I2S(0, # This must be either 0 or 1 for ESP32
            sck=sck_pin, ws=ws_pin, sd=sd_pin,
            mode=I2S.TX,
            bits=16,
            format=I2S.MONO,
            rate=88200, # This must match the sample rate of your file!
            ibuf=10000)

    # Let's play a clip in a .wav file
    # if the file is in a folder you need to include the folder name
    # example: "WAVFILE = "/soundFiles/fuzzy.wav"

    WAVFILE = "Get out cycle - 28_10_2024, 6.40 PM.wav"
    BUFFER_SIZE = 10000

    wav = open(WAVFILE, "rb") # Open the file to read its bytes
    pos = wav.seek(44) # Skip over the WAV header information and get to the data

    # Create a memory buffer to store the samples
    buf = bytearray(BUFFER_SIZE)
    # And create a "memoryview" (which is basically another window into the same data),
    # which will allow us to read the file directly into the buffer.
    wav_samples_mv = memoryview(buf)

    # Wrap the sound-playing in a try-except block
    # If something goes wrong in the middle (like the user pressing 'Stop'), we'll
    # run the "except" part and then clean up. Otherwise, we can end up with the I2S
    # device stuck playing, which is *really* annoying.
    
   
    timer = 7        
    try:
        while (timer > 0):
            # Try to read some bytes from the wave file into the buffer
            # The `readinto` function returns the number of bytes that it read
            bytes_read = wav.readinto(wav_samples_mv)
            print(bytes_read)

            
            # If the function didn't read anything, we must have reached the end of the file
            if bytes_read == 0:
                print("I'm in")
                break # Quit the loop and stop playing
               
            else:
                # If we did read some bytes, send them to the speaker
                num_written = audio.write(wav_samples_mv[:bytes_read])
                print("speaking...")
                sleep(0.001)
                timer = timer - 0.3
             

    except (KeyboardInterrupt) as e:
        pass

    audio.deinit()   
    
    
sck_pin = Pin(5) # Serial clock (BCLK on breakout)
ws_pin = Pin(6) # Word select (LRCLK on breakout)
sd_pin = Pin(4) # Serial data (DIN on breakout)

led1 = Pin(36, Pin.OUT)
led2 = Pin(38, Pin.OUT)
led3 = Pin(35, Pin.OUT)
led4 = Pin(37, Pin.OUT)

# bigger the number, closer object is.
distancesensor = ADC(Pin(7))

distancesensor.atten(ADC.ATTN_11DB)
#raw = 10000

while True:
    raw = distancesensor.read()
    sleep(0.2)
    if raw > 2000 :
        led1.on()
        led2.on()
        led3.on()
        led4.on()
        print(f"Read distance sensor {raw}")
        speak()
  
    else:
        led1.off()
        led2.off()
        led3.off()
        led4.off()
        print(f"Read distance sensor {raw}")    